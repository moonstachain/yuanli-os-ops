#!/usr/bin/env python3
"""Shared helpers for the FORCE-CLAW content race workspace."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WORKFLOWS = ["coze", "dify", "feishu", "n8n"]
QUERY_BUCKETS = ["OpenAI/模型热点", "AI 工作流/工具链", "CLAW 邻近表达"]
SURFACES = ["hot", "recent"]

WORKFLOW_DEFAULTS: dict[str, dict[str, Any]] = {
    "coze": {
        "declared_path": "content-first workflow",
        "why_this_platform": "Coze 适合把内容判断和交互式工作流组合成快速验证面。",
        "known_limits": [
            "复杂状态回写与长期主承载仍需额外验证",
            "跨系统治理能力不应靠平台想象补齐",
        ],
        "non_fit_warning": "",
    },
    "dify": {
        "declared_path": "content-first workflow",
        "why_this_platform": "Dify 适合把研究、结构化生成和阶段性 workflow 快速拼装起来验证。",
        "known_limits": [
            "长期主系统承载边界需要额外验证",
            "复杂状态治理仍可能依赖外部系统",
        ],
        "non_fit_warning": "",
    },
    "feishu": {
        "declared_path": "knowledge-centric workflow",
        "why_this_platform": "Feishu 适合承载知识库、状态流、回写和组织协同闭环。",
        "known_limits": [
            "外部生态灵活度不如 n8n",
            "某些集成仍需 webhook 或补脚本",
        ],
        "non_fit_warning": "",
    },
    "n8n": {
        "declared_path": "event/webhook orchestration",
        "why_this_platform": "n8n 适合做采集、归一化、通知、回写和多系统编排的确定性自动化。",
        "known_limits": [
            "不适合把整段内容脑力推理硬塞进自动化画布",
            "凭证、触发和回写链路需要更严格验真",
        ],
        "non_fit_warning": "不适合单独承载完整内容推理，但适合作为编排底座。",
    },
}

FIT_PATTERN_LABELS = {
    "认知升级",
    "边界判断",
    "原理翻转",
    "反常识",
    "流程拆解",
    "实操模板",
    "避坑",
    "选型省错",
    "效率承诺",
}
AVOID_PATTERN_LABELS = {"娱乐八卦", "夸张承诺", "情绪煽动", "纯鸡汤"}
ALIGNMENT_KEYWORDS = ["CLAW", "AI", "工作流", "知识库", "OpenAI", "Agent", "飞书", "自动化"]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def dedupe_samples(samples: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    notes: list[str] = []
    for sample in samples:
        dedupe_key = sample.get("post_id") or sample.get("post_url") or sample.get("sample_id")
        if not dedupe_key:
            notes.append(f"sample {sample.get('sample_id', 'unknown')} 缺少 dedupe key")
            continue
        if dedupe_key in seen:
            notes.append(f"duplicate skipped: {dedupe_key}")
            continue
        seen.add(dedupe_key)
        deduped.append(sample)
    return deduped, notes


def ratio_counter(values: list[str]) -> float:
    if not values:
        return 1.0
    counts = Counter(values)
    return max(counts.values()) / len(values)


def keyword_hit(text: str) -> bool:
    return any(keyword.lower() in text.lower() for keyword in ALIGNMENT_KEYWORDS)


def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return numerator / denominator


def limit(value: float, upper: float) -> float:
    return max(0.0, min(value, upper))


def round_stage_defaults() -> dict[str, dict[str, str]]:
    return {
        "knowledge_digest": {"status": "pending", "reason": "awaiting_knowledge_source"},
        "xhs_collection": {"status": "pending", "reason": "awaiting_xhs_collection"},
        "workflow_submissions": {
            "status": "pending_shared_evidence",
            "reason": "cannot_start_until_knowledge_and_evidence_exist",
        },
        "weekly_scorecard": {
            "status": "pending_shared_evidence",
            "reason": "score_requires_real_shared_inputs",
        },
    }


def default_round_status(round_id: str) -> dict[str, Any]:
    return {
        "round_id": round_id,
        "generated_at": now_iso(),
        "status": "initialized",
        "closure_state": "not_closed",
        "blocked_stages": round_stage_defaults(),
        "completion_checks": {
            "artifact_exists": False,
            "goal_reached": False,
            "boundary_safe": True,
            "result_verified": False,
        },
        "next_actions": [],
    }


def load_round_status(round_dir: Path) -> dict[str, Any]:
    status_path = round_dir / "round_status.json"
    if status_path.exists():
        return load_json(status_path)
    return default_round_status(round_dir.name)


def compute_round_top_status(status: dict[str, Any]) -> str:
    stages = status.get("blocked_stages", {})
    knowledge = stages.get("knowledge_digest", {}).get("status")
    xhs = stages.get("xhs_collection", {}).get("status")
    workflows = stages.get("workflow_submissions", {}).get("status")
    weekly = stages.get("weekly_scorecard", {}).get("status")
    closure_state = status.get("closure_state", "not_closed")

    if closure_state == "closed":
        return "closed"
    if any(stage.get("status") == "blocked" for stage in stages.values()):
        return "blocked_auth_or_access_gate"
    if knowledge == "ready" and xhs == "ready" and workflows in {"pending_shared_evidence", "pending"}:
        return "shared_evidence_ready"
    if workflows == "ready" and weekly in {"pending", "pending_shared_evidence"}:
        return "submissions_ready"
    if weekly == "ready":
        return "scored_not_closed"
    return status.get("status", "initialized")


def refresh_completion_checks(status: dict[str, Any]) -> None:
    stages = status.get("blocked_stages", {})
    artifact_exists = all(
        stages.get(stage, {}).get("status") == "ready"
        for stage in ("knowledge_digest", "xhs_collection", "workflow_submissions", "weekly_scorecard")
    )
    status["completion_checks"] = {
        "artifact_exists": artifact_exists,
        "goal_reached": status.get("closure_state") == "closed",
        "boundary_safe": True,
        "result_verified": stages.get("weekly_scorecard", {}).get("status") == "ready"
        or any(stage.get("status") == "blocked" for stage in stages.values()),
    }
