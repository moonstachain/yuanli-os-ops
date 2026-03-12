#!/usr/bin/env python3
"""Render AI-da-guan-jia supervision artifacts for a content-race round."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from content_race_common import load_round_status, now_iso


DEFAULT_SUPERVISION_MODE = "全程督办"
DEFAULT_KNOWLEDGE_SOURCE_POLICY = "不允许临时替代知识源"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def gate_stage_summary(stage_name: str, stage_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage": stage_name,
        "status": stage_payload.get("status", "unknown"),
        "reason": stage_payload.get("reason", ""),
        "artifact": stage_payload.get("artifact", ""),
    }


def infer_current_phase(status_payload: dict[str, Any]) -> str:
    stages = status_payload.get("blocked_stages", {})
    knowledge = stages.get("knowledge_digest", {})
    xhs = stages.get("xhs_collection", {})
    workflows = stages.get("workflow_submissions", {})
    weekly = stages.get("weekly_scorecard", {})

    if knowledge.get("status") == "blocked":
        return "feishu_knowledge_source_gate"
    if knowledge.get("status") == "ready" and xhs.get("status") == "blocked":
        return "xhs_sampling_gate"
    if knowledge.get("status") == "ready" and xhs.get("status") == "ready" and workflows.get("status") != "ready":
        return "workflow_submission_gate"
    if workflows.get("status") == "ready" and weekly.get("status") != "ready":
        return "scorecard_gate"
    if weekly.get("status") == "ready":
        return "post_scorecard_closure_gate"
    if status_payload.get("closure_state") == "closed":
        return "closed"
    return status_payload.get("status", "initialized")


def build_evaluation(
    round_dir: Path,
    status_payload: dict[str, Any],
    supervision_mode: str,
    knowledge_source_policy: str,
) -> dict[str, Any]:
    stages = status_payload.get("blocked_stages", {})
    current_phase = infer_current_phase(status_payload)
    current_status = status_payload.get("status", "initialized")
    knowledge_stage = stages.get("knowledge_digest", {})
    knowledge_reason = str(knowledge_stage.get("reason", ""))
    pending_human_input = []
    most_important_next_action = "获取新的可访问飞书知识源 URL"
    main_distortion = "旧飞书 URL 已失效或不可达，继续使用会污染全部后续产物"
    if current_phase == "feishu_knowledge_source_gate":
        if "auth_required" in knowledge_reason or "login_required" in knowledge_reason:
            pending_human_input.append("在专用 Feishu 登录窗口完成登录")
            most_important_next_action = "在专用 Feishu 浏览器窗口完成登录并重跑提取"
            main_distortion = "把已经命中新知识源候选但仍需登录验证的状态，误判成还没有可用候选 URL。"
        else:
            pending_human_input.append("新的可访问飞书知识源 URL")

    return {
        "round_id": round_dir.name,
        "generated_at": now_iso(),
        "controller": "ai-da-guan-jia",
        "task_status": current_status,
        "phase": current_phase,
        "assessment": {
            "summary": "结构完成，真实闭环未完成",
            "strengths": [
                "没有伪完成，阻塞被真实留证",
                "工作区分层清楚，后续可继续推进",
            ],
            "problems": [
                "真实 round 仍卡在共享证据层，当前还不能算赛马已开始",
            ],
        },
        "completed": [
            "content-race-mvp 工作区骨架已成立",
            "四方赛马 runner 已可跑通 example regression",
            "real-round-20260310-01 已创建并留下 canonical 阻塞记录",
            "恢复脚本已补齐，可在拿到新知识源后直接继续推进",
        ],
        "unfinished": [
            "真实 knowledge_digest",
            "真实 xhs_evidence_pack",
            "四个 workflow 的真实 submission",
            "真实 weekly_scorecard",
        ],
        "main_distortion": main_distortion,
        "most_important_next_action": most_important_next_action,
        "supervision_mode": supervision_mode,
        "knowledge_source_policy": knowledge_source_policy,
        "pending_human_input": pending_human_input,
        "blocked_stages": [
            gate_stage_summary("knowledge_digest", stages.get("knowledge_digest", {})),
            gate_stage_summary("xhs_collection", stages.get("xhs_collection", {})),
            gate_stage_summary("workflow_submissions", stages.get("workflow_submissions", {})),
            gate_stage_summary("weekly_scorecard", stages.get("weekly_scorecard", {})),
        ],
    }


def build_supervision_status(
    status_payload: dict[str, Any],
    evaluation: dict[str, Any],
    supervision_mode: str,
    knowledge_source_policy: str,
) -> dict[str, Any]:
    current_phase = evaluation["phase"]
    next_transition = {
        "feishu_knowledge_source_gate": "knowledge_digest_ready",
        "xhs_sampling_gate": "xhs_evidence_ready",
        "workflow_submission_gate": "workflow_submissions_ready",
        "scorecard_gate": "weekly_scorecard_ready",
        "post_scorecard_closure_gate": "closure_review",
    }.get(current_phase, "maintain_truthful_block_state")

    return {
        "generated_at": evaluation["generated_at"],
        "round_id": evaluation["round_id"],
        "controller": "ai-da-guan-jia",
        "supervision_mode": supervision_mode,
        "knowledge_source_policy": knowledge_source_policy,
        "status": status_payload.get("status", "initialized"),
        "closure_state": status_payload.get("closure_state", "not_closed"),
        "current_phase": current_phase,
        "gate_order": [
            "feishu_knowledge_source_gate",
            "xhs_sampling_gate",
            "workflow_submission_gate",
            "scorecard_gate",
            "post_scorecard_closure_gate",
        ],
        "next_transition": next_transition,
        "ready_to_advance": current_phase not in {"feishu_knowledge_source_gate", "xhs_sampling_gate"},
        "canonical_sync": {
            "feishu_mirror": "deferred_until_real_weekly_scorecard",
            "github_governance": "deferred_until_real_weekly_scorecard",
            "full_evolution_run": "deferred_until_real_weekly_scorecard",
        },
        "pending_human_input": evaluation["pending_human_input"],
        "enforced_rules": [
            "不允许临时替代知识源",
            "共享证据缺失时不得提前做 Feishu/GitHub mirror",
            "不得把 example regression 说成真实闭环",
        ],
    }


def build_brief(
    evaluation: dict[str, Any],
    supervision_status: dict[str, Any],
    gate_files: dict[str, str],
) -> str:
    lines = [
        f"# AI大管家督办简报: {evaluation['round_id']}",
        "",
        f"- 任务状态: {evaluation['task_status']}",
        f"- 当前阶段: {evaluation['phase']}",
        f"- 评价结论: {evaluation['assessment']['summary']}",
        f"- 督办模式: {evaluation['supervision_mode']}",
        f"- 知识源策略: {evaluation['knowledge_source_policy']}",
        f"- 当前最重要动作: {evaluation['most_important_next_action']}",
        "",
        "## 已完成",
        "",
    ]
    lines.extend([f"- {item}" for item in evaluation["completed"]])
    lines.extend(["", "## 未完成", ""])
    lines.extend([f"- {item}" for item in evaluation["unfinished"]])
    lines.extend(
        [
            "",
            "## 主要失真",
            "",
            f"- {evaluation['main_distortion']}",
            "",
            "## 督办顺序",
            "",
            "1. 先解飞书知识源 gate。",
            "2. 知识源 ready 后，再解小红书采样 gate。",
            "3. 共享证据四件套齐全后，才启动 coze / dify / feishu / n8n 四方交卷。",
            "4. 四方真实交卷齐全后，才生成 weekly_scorecard。",
            "5. 只有 real weekly_scorecard 出现后，才允许做 AI大管家 的 Feishu/GitHub mirror。",
            "",
            "## 当前 Gate",
            "",
        ]
    )
    for blocked in evaluation["blocked_stages"]:
        artifact = blocked["artifact"] or "none"
        lines.append(
            f"- {blocked['stage']}: {blocked['status']} / {blocked['reason']} / artifact={artifact}"
        )
    lines.extend(
        [
            "",
            "## Gate 留证摘要",
            "",
            f"- Feishu gate artifact: {gate_files['knowledge_source_gate']}",
            f"- Xiaohongshu gate artifact: {gate_files['xhs_collection_gate']}",
            "",
            "## Canonical Sync Policy",
            "",
            f"- Feishu mirror: {supervision_status['canonical_sync']['feishu_mirror']}",
            f"- GitHub governance: {supervision_status['canonical_sync']['github_governance']}",
            f"- Full evolution run: {supervision_status['canonical_sync']['full_evolution_run']}",
        ]
    )
    return "\n".join(lines) + "\n"


def append_worklog(round_dir: Path, message: str) -> None:
    worklog_path = round_dir / "worklog.md"
    if not worklog_path.exists():
        return
    current = worklog_path.read_text(encoding="utf-8")
    if "## AI Da Guan Jia Supervision" not in current:
        current += "\n## AI Da Guan Jia Supervision\n\n"
    current += f"- {message}\n"
    worklog_path.write_text(current, encoding="utf-8")


def render_supervision_artifacts(
    round_dir: Path,
    supervision_mode: str = DEFAULT_SUPERVISION_MODE,
    knowledge_source_policy: str = DEFAULT_KNOWLEDGE_SOURCE_POLICY,
    append_worklog_entry: bool = False,
) -> Path:
    round_dir = round_dir.resolve()
    supervision_dir = ensure_dir(round_dir / "ai-da-guan-jia")
    status_payload = load_round_status(round_dir)
    evaluation = build_evaluation(
        round_dir,
        status_payload,
        supervision_mode=supervision_mode,
        knowledge_source_policy=knowledge_source_policy,
    )
    supervision_status = build_supervision_status(
        status_payload,
        evaluation,
        supervision_mode=supervision_mode,
        knowledge_source_policy=knowledge_source_policy,
    )
    gate_files = {
        "knowledge_source_gate": str(round_dir / "feishu-reader" / "knowledge_source_gate.json"),
        "xhs_collection_gate": str(round_dir / "collector" / "xhs_collection_gate.json"),
    }

    with (supervision_dir / "evaluation.json").open("w", encoding="utf-8") as handle:
        json.dump(evaluation, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with (supervision_dir / "supervision_status.json").open("w", encoding="utf-8") as handle:
        json.dump(supervision_status, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    (supervision_dir / "supervision_brief.md").write_text(
        build_brief(evaluation, supervision_status, gate_files),
        encoding="utf-8",
    )

    if append_worklog_entry:
        append_worklog(
            round_dir,
            (
                f"{evaluation['generated_at']}: AI大管家已刷新督办状态，当前 phase="
                f"{evaluation['phase']}，最重要动作={evaluation['most_important_next_action']}。"
            ),
        )

    return supervision_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-dir", required=True, type=Path)
    parser.add_argument("--supervision-mode", default=DEFAULT_SUPERVISION_MODE)
    parser.add_argument("--knowledge-source-policy", default=DEFAULT_KNOWLEDGE_SOURCE_POLICY)
    parser.add_argument("--append-worklog", action="store_true")
    args = parser.parse_args()

    supervision_dir = render_supervision_artifacts(
        round_dir=args.round_dir,
        supervision_mode=args.supervision_mode,
        knowledge_source_policy=args.knowledge_source_policy,
        append_worklog_entry=args.append_worklog,
    )
    print(supervision_dir)


if __name__ == "__main__":
    main()
