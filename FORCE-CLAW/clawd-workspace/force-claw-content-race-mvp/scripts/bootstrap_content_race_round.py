#!/usr/bin/env python3
"""Bootstrap a content race round with the standard directory structure."""

from __future__ import annotations

import argparse
from pathlib import Path

from content_race_common import WORKFLOW_DEFAULTS, WORKFLOWS, default_round_status, dump_json, ensure_dir, load_json, now_iso
from update_supervision_status import render_supervision_artifacts


def write_initial_worklog(round_dir: Path, round_id: str, generated_at: str) -> None:
    content = "\n".join(
        [
            f"# Real Round Work Log: {round_id}",
            "",
            f"- Generated at: {generated_at}",
            "- Current status: initialized",
            "- Closure state: not_closed",
            "",
            "## What Happened",
            "",
            "- Round bootstrap 已完成，当前进入飞书知识源 gate。",
            "",
            "## What This Means",
            "",
            "- 当前只完成了结构初始化，还没有真实知识源和真实小红书证据。",
            "- 在共享证据形成前，不允许把本轮视为真实赛马开始。",
            "",
            "## Immediate Next Actions",
            "",
            "1. 提供新的可访问飞书知识源 URL，并重建 knowledge_digest。",
            "2. 知识源 ready 后，再切到可靠网络环境做小红书采样。",
            "3. 共享证据齐全后，再启动四方 submission 和 weekly_scorecard。",
            "",
        ]
    )
    (round_dir / "worklog.md").write_text(content, encoding="utf-8")


def build_round(workspace_root: Path, round_id: str, output_root: Path) -> Path:
    templates_dir = workspace_root / "templates"
    round_dir = output_root / round_id
    collector_dir = ensure_dir(round_dir / "collector")
    ensure_dir(collector_dir / "raw_samples")
    ensure_dir(collector_dir / "screenshots")
    submissions_dir = ensure_dir(round_dir / "submissions")
    ensure_dir(round_dir / "scorecards")
    generated_at = now_iso()

    query_plan = load_json(templates_dir / "query_plan.json")
    dump_json(round_dir / "query_plan.json", query_plan)

    knowledge_digest = load_json(templates_dir / "knowledge_digest.template.json")
    knowledge_digest["captured_at"] = ""
    dump_json(round_dir / "knowledge_digest.json", knowledge_digest)

    submission_template = load_json(templates_dir / "workflow_submission.template.json")
    for workflow in WORKFLOWS:
        submission = dict(submission_template)
        submission["workflow_name"] = workflow
        submission["round_id"] = round_id
        submission["platform_fit"] = WORKFLOW_DEFAULTS[workflow]
        workflow_dir = ensure_dir(submissions_dir / workflow)
        dump_json(workflow_dir / "submission.json", submission)

    dump_json(
        round_dir / "round_manifest.json",
        {
            "round_id": round_id,
            "generated_at": generated_at,
            "collector_dir": str(collector_dir),
            "submission_workflows": WORKFLOWS,
        },
    )
    round_status = default_round_status(round_id)
    round_status["generated_at"] = generated_at
    round_status["next_actions"] = [
        "提供新的可访问飞书知识源 URL。",
        "知识源 ready 后切换小红书采样网络环境并重试公开页采样。",
        "共享证据四件套齐全后，再启动四方 submission。",
    ]
    dump_json(round_dir / "round_status.json", round_status)
    write_initial_worklog(round_dir, round_id, generated_at)
    render_supervision_artifacts(round_dir)
    return round_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workspace-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="content-race workspace root",
    )
    parser.add_argument("--round-id", required=True, help="round identifier")
    parser.add_argument(
        "--output-root",
        type=Path,
        help="parent directory of rounds; defaults to <workspace-root>/runtime-artifacts/runs",
    )
    args = parser.parse_args()

    workspace_root = args.workspace_root.resolve()
    output_root = (args.output_root or (workspace_root / "runtime-artifacts" / "runs")).resolve()
    ensure_dir(output_root)
    round_dir = build_round(workspace_root, args.round_id, output_root)
    print(round_dir)


if __name__ == "__main__":
    main()
