#!/usr/bin/env python3
"""Validate the content race workspace and the four-way runner loop."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = WORKSPACE_ROOT / "scripts"
REQUIRED_FILES = [
    "README.md",
    "AGENTS.md",
    "SOUL.md",
    "USER.md",
    "IDENTITY.md",
    "TOOLS.md",
    "HEARTBEAT.md",
    "RULES.md",
    "MEMORY.md",
    "GENOME.md",
    "SKILL_STRATEGY.md",
    "EVOLUTION_RULES.md",
    "CLOSURE_STANDARD.md",
    "GROWTH_LOG_POLICY.md",
    "WORK_LOG_POLICY.md",
    "contracts/knowledge_digest.schema.json",
    "contracts/xhs_evidence_pack.schema.json",
    "contracts/viral_pattern_digest.schema.json",
    "contracts/claw_topic_bridge.schema.json",
    "contracts/workflow_race_submission.schema.json",
    "contracts/weekly_scorecard.schema.json",
    "skills/ai-ling-shou-core/SKILL.md",
    "skills/xhs-viral-evidence-collector/SKILL.md",
    "skills/force-claw-workflow-race-judge/SKILL.md",
    "hooks/manifest.json",
    "hooks/session-start.md",
    "hooks/major-execution-preflight.md",
    "hooks/pre-close-truth-gate.md",
    "hooks/post-close-promotion-review.md",
    "templates/query_plan.json",
    "templates/knowledge_digest.template.json",
    "templates/workflow_submission.template.json",
    "examples/knowledge_digest.example.json",
    "examples/coze_submission.example.json",
    "examples/dify_submission.example.json",
    "examples/feishu_submission.example.json",
    "examples/n8n_submission.example.json",
    "examples/weekly_scorecard.example.json",
    "scripts/bootstrap_content_race_round.py",
    "scripts/apply_knowledge_source.py",
    "scripts/update_round_status.py",
    "scripts/update_supervision_status.py",
    "scripts/normalize_xhs_evidence.py",
    "scripts/score_content_race_round.py",
    "references/real-round-recovery.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(f"command failed: {' '.join(cmd)}\nstdout={result.stdout}\nstderr={result.stderr}")
    return result.stdout.strip()


def check_required_files() -> None:
    missing = [path for path in REQUIRED_FILES if not (WORKSPACE_ROOT / path).exists()]
    if missing:
        fail(f"missing files: {missing}")
    print(f"OK: {len(REQUIRED_FILES)} required files present")


def check_json_files() -> None:
    for path in sorted((WORKSPACE_ROOT / "contracts").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
    for path in sorted((WORKSPACE_ROOT / "examples").glob("*.json")):
        json.loads(path.read_text(encoding="utf-8"))
    print("OK: contracts and top-level examples parse as JSON")


def run_round_regression() -> None:
    with tempfile.TemporaryDirectory(prefix="content-race-validate-") as temp_dir_name:
        temp_root = Path(temp_dir_name)
        rounds_root = temp_root / "runs"
        round_id = "validation-round"
        round_dir = Path(
            run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "bootstrap_content_race_round.py"),
                    "--workspace-root",
                    str(WORKSPACE_ROOT),
                    "--round-id",
                    round_id,
                    "--output-root",
                    str(rounds_root),
                ]
            )
        )

        shutil.copy2(WORKSPACE_ROOT / "examples" / "knowledge_digest.example.json", round_dir / "knowledge_digest.json")
        raw_dir = round_dir / "collector" / "raw_samples"
        for sample in sorted((WORKSPACE_ROOT / "examples" / "raw-samples").glob("*.json")):
            shutil.copy2(sample, raw_dir / sample.name)

        run([sys.executable, str(SCRIPTS_DIR / "normalize_xhs_evidence.py"), "--round-dir", str(round_dir)])

        fake_feishu_json = temp_root / "feishu-source.json"
        fake_text_lines = [
            "CLAW 是 evidence-first 的内容流程运行时，用来把复杂内容生产和复盘做成闭环。",
            "目标用户是想把复杂内容流程沉淀成工作流的主理人和运营团队。",
            "不要把热点当成事实，要先保留真实帖子证据与验证步骤。",
            "表达要锋利，但不能离开验证路径和复盘机制。",
            "适合需要把知识库、证据包、评分卡串起来的内容系统。",
            "系统优先追求真实完成，而不是表面上把任务推进了一步。",
            "任何阶段性结论都必须能被下一轮复训或回看验证。",
            "热点只是输入，不是目标，目标是留下可复用的复杂流程。",
            "知识库负责提供世界观和禁区，证据包负责提供真实样本和传播结构。",
            "工作流赛马的核心不是谁最会写，而是谁最适合成为长期主调用面。",
        ]
        fake_feishu_json.write_text(
            json.dumps(
                {
                    "status": "ok",
                    "title": "CLAW AI 原理总览",
                    "metadata": {
                        "document_title": "CLAW AI 原理总览",
                        "top_lines": [
                            "CLAW 是 evidence-first 的内容流程运行时",
                            "目标用户是想把复杂内容流程沉淀成工作流的主理人",
                            "不要把热点当成事实，要先保留证据",
                            "表达要锋利，但不能离开验证路径",
                        ],
                    },
                    "text": "\n".join(
                        fake_text_lines
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "apply_knowledge_source.py"),
                "--round-dir",
                str(round_dir),
                "--source-url",
                "https://example.feishu.cn/wiki/claw-source",
                "--source-json",
                str(fake_feishu_json),
                "--min-text-length",
                "100",
            ]
        )
        status_after_knowledge = json.loads((round_dir / "round_status.json").read_text(encoding="utf-8"))
        if status_after_knowledge["blocked_stages"]["knowledge_digest"]["status"] != "ready":
            fail("knowledge_digest stage was not marked ready")

        run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "update_round_status.py"),
                "--round-dir",
                str(round_dir),
                "--stage",
                "xhs_collection",
                "--status",
                "ready",
                "--reason",
                "xhs_evidence_pack_generated",
                "--artifact",
                str(round_dir / "collector" / "xhs_evidence_pack.json"),
            ]
        )
        supervision_dir = Path(
            run(
                [
                    sys.executable,
                    str(SCRIPTS_DIR / "update_supervision_status.py"),
                    "--round-dir",
                    str(round_dir),
                ]
            )
        )
        supervision_status = json.loads((supervision_dir / "supervision_status.json").read_text(encoding="utf-8"))
        evaluation = json.loads((supervision_dir / "evaluation.json").read_text(encoding="utf-8"))
        if evaluation.get("assessment", {}).get("summary") != "结构完成，真实闭环未完成":
            fail("supervision evaluation summary drifted")
        if supervision_status.get("controller") != "ai-da-guan-jia":
            fail("supervision status controller missing")

        submissions_map = {
            "coze": WORKSPACE_ROOT / "examples" / "coze_submission.example.json",
            "dify": WORKSPACE_ROOT / "examples" / "dify_submission.example.json",
            "feishu": WORKSPACE_ROOT / "examples" / "feishu_submission.example.json",
            "n8n": WORKSPACE_ROOT / "examples" / "n8n_submission.example.json",
        }
        for workflow, source in submissions_map.items():
            shutil.copy2(source, round_dir / "submissions" / workflow / "submission.json")

        scorecard_path = Path(
            run([sys.executable, str(SCRIPTS_DIR / "score_content_race_round.py"), "--round-dir", str(round_dir)])
        )
        scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
        if len(scorecard.get("workflow_scores", [])) != 4:
            fail("weekly_scorecard does not contain four workflow scores")
        if len(scorecard.get("selection_outlook", {}).get("leaderboard", [])) != 4:
            fail("leaderboard does not contain four entries")
        print("OK: four-way bootstrap -> normalize -> score regression passed")


def main() -> None:
    check_required_files()
    check_json_files()
    run_round_regression()
    print("OK: content race workspace validation completed")


if __name__ == "__main__":
    main()
