#!/usr/bin/env python3
"""Score a content race round across four workflow surfaces."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from content_race_common import (
    ALIGNMENT_KEYWORDS,
    WORKFLOWS,
    compute_round_top_status,
    dump_json,
    keyword_hit,
    limit,
    load_json,
    load_round_status,
    now_iso,
    refresh_completion_checks,
    safe_div,
)
from update_supervision_status import render_supervision_artifacts


def score_collector(evidence_pack: dict[str, Any], pattern_digest: dict[str, Any], claw_bridge: dict[str, Any]) -> dict[str, Any]:
    samples = evidence_pack.get("samples", [])
    coverage = evidence_pack.get("coverage", {})
    sample_count = len(samples)
    post_url_ratio = safe_div(sum(1 for sample in samples if sample.get("post_url")), sample_count)
    screenshot_ratio = safe_div(
        sum(1 for sample in samples if sample.get("screenshots")),
        sample_count,
    )
    bucket_ratio = safe_div(len(set(evidence_pack.get("query_buckets", []))), 3)
    surface_ratio = safe_div(len(set(coverage.get("surfaces", []))), 2)
    author_penalty = 0 if coverage.get("author_concentration", 1) <= 0.2 else 4
    query_penalty = 0 if coverage.get("query_concentration", 1) <= 0.25 else 4
    pattern_count = len(pattern_digest.get("patterns", []))
    fit_count = len(claw_bridge.get("fit_patterns", []))

    breakdown = {
        "evidence_authenticity": round(limit((post_url_ratio * 0.6 + screenshot_ratio * 0.4) * 30, 30), 2),
        "sampling_coverage": round(limit(bucket_ratio * 10 + surface_ratio * 10 - author_penalty - query_penalty, 20), 2),
        "pattern_explanation": round(limit(pattern_count * 3 + fit_count * 2, 20), 2),
        "claw_alignment": round(limit(fit_count * 4 + (3 if claw_bridge.get("translation_rules") else 0), 15), 2),
        "downstream_utility": round(limit((1 if samples else 0) * 5 + pattern_count * 1.5 + fit_count * 1.5, 15), 2),
    }

    redlines = []
    if sample_count == 0:
        redlines.append("没有真实小红书帖子样本")
    if post_url_ratio < 1:
        redlines.append("存在缺少 post_url 的样本")
    if not evidence_pack.get("negative_notes"):
        redlines.append("缺少 negative_notes")

    total = round(sum(breakdown.values()), 2)
    training_backlog = []
    if bucket_ratio < 1:
        training_backlog.append("补齐三类 query buckets，避免样本主题偏斜。")
    if surface_ratio < 1:
        training_backlog.append("同时覆盖 hot 和 recent，避免只看单一表面。")
    if screenshot_ratio < 0.8:
        training_backlog.append("提升截图留证率，至少让大部分样本有可回看截图。")
    if pattern_count < 3:
        training_backlog.append("补足 3 个以上 pattern，避免归因结论过薄。")
    return {
        "total": total,
        "breakdown": breakdown,
        "redlines": redlines,
        "training_backlog": training_backlog[:2],
    }


def submission_redlines(submission: dict[str, Any]) -> list[str]:
    redlines = []
    candidates = submission.get("topic_candidates", [])
    if not candidates:
        redlines.append("没有 topic_candidates")
    if not any(candidate.get("evidence_refs") for candidate in candidates):
        redlines.append("没有真实 evidence refs 却给出选题")
    combined_text = " ".join(
        [
            candidate.get("title", "") + " " + candidate.get("claw_angle", "")
            for candidate in candidates
        ]
    )
    if not keyword_hit(combined_text):
        redlines.append("选题偏离 CLAW/AI 主轴")
    rankings = submission.get("reasoned_ranking", [])
    if not any(item.get("why_it_may_win") for item in rankings):
        redlines.append("只模仿标题，没有解释为什么火")
    return redlines


def score_platform_fit(workflow_name: str, platform_fit: dict[str, Any]) -> tuple[float, dict[str, Any], bool]:
    declared_path = platform_fit.get("declared_path", "")
    why = platform_fit.get("why_this_platform", "")
    known_limits = platform_fit.get("known_limits", [])
    non_fit_warning = platform_fit.get("non_fit_warning", "")
    score = 0.0
    if declared_path:
        score += 4
    if why:
        score += 4
    if known_limits:
        score += 4
    if non_fit_warning:
        score += 3
    cap_to_sixty = "non-fit" in declared_path.lower() or "non-n8n" in non_fit_warning.lower()
    if workflow_name == "n8n" and "event" in declared_path.lower():
        score = min(15.0, score + 1.0)
    return (
        min(15.0, score),
        {
            "declared_path": declared_path,
            "assessment_note": f"{workflow_name} 当前声明为 {declared_path or 'unknown'}，边界说明{'充分' if known_limits else '偏弱'}。",
        },
        cap_to_sixty,
    )


def score_submission(submission: dict[str, Any], evidence_pack: dict[str, Any]) -> dict[str, Any]:
    candidates = submission.get("topic_candidates", [])
    rankings = submission.get("reasoned_ranking", [])
    sample_plan = submission.get("sample_post_plan", {})
    verification = submission.get("verification_plan", {})
    platform_fit = submission.get("platform_fit", {})

    candidate_evidence_ratio = safe_div(
        sum(1 for candidate in candidates if candidate.get("evidence_refs")),
        len(candidates),
    )
    ranking_evidence_ratio = safe_div(
        sum(1 for item in rankings if item.get("evidence_refs")),
        len(rankings),
    )
    evidence_usage = limit((candidate_evidence_ratio * 10) + (ranking_evidence_ratio * 10), 20)

    alignment_hits = sum(
        1
        for candidate in candidates
        if keyword_hit(candidate.get("title", "") + " " + candidate.get("claw_angle", ""))
    )
    topic_judgment = limit(
        safe_div(alignment_hits, len(candidates)) * 12 + (4 if len(rankings) >= 3 else 0) + (4 if len(candidates) >= 5 else 0),
        20,
    )

    pattern_ratio = safe_div(
        sum(1 for candidate in candidates if candidate.get("pattern_refs")),
        len(candidates),
    )
    slide_count = len(sample_plan.get("slide_outline", []))
    translation_quality = limit(pattern_ratio * 10 + (5 if slide_count >= 3 else 0), 15)

    executability = limit(
        (5 if sample_plan.get("cover_hook") else 0)
        + (5 if slide_count >= 3 else 0)
        + (5 if sample_plan.get("cta") and sample_plan.get("visual_notes") else 0),
        15,
    )

    verification_score = limit(
        (5 if verification.get("success_signals") else 0)
        + (5 if verification.get("failure_signals") else 0)
        + (5 if verification.get("review_method") else 0),
        15,
    )

    platform_fit_score, platform_fit_assessment, cap_to_sixty = score_platform_fit(
        submission.get("workflow_name", ""),
        platform_fit,
    )
    breakdown = {
        "evidence_usage": round(evidence_usage, 2),
        "topic_judgment": round(topic_judgment, 2),
        "translation_quality": round(translation_quality, 2),
        "executability": round(executability, 2),
        "verification": round(verification_score, 2),
        "platform_fit": round(platform_fit_score, 2),
    }
    redlines = submission_redlines(submission)
    total = round(sum(breakdown.values()), 2)
    if redlines:
        total = min(total, 50)
    if cap_to_sixty:
        total = min(total, 60)

    training_backlog = []
    if evidence_usage < 16:
        training_backlog.append("提高 topic_candidates 和 TOP 3 对 evidence refs 的覆盖率。")
    if topic_judgment < 16:
        training_backlog.append("增强选题与 CLAW/AI 主轴的贴合度，不要泛化成通用 AI 内容。")
    if translation_quality < 12:
        training_backlog.append("补强从 pattern 到图文结构的转译解释。")
    if verification_score < 12:
        training_backlog.append("把 success/failure/review 写成可执行的验真步骤。")
    if submission.get("workflow_name") == "n8n" and platform_fit_score < 13:
        training_backlog.append("讲清 webhook/sub-workflow/回写链路的边界，避免把自动化平台写成内容脑力平台。")

    return {
        "workflow_name": submission.get("workflow_name", ""),
        "total": total,
        "breakdown": breakdown,
        "platform_fit_assessment": platform_fit_assessment,
        "redlines": redlines,
        "training_backlog": training_backlog[:2],
    }


def require_real_shared_inputs(round_dir: Path) -> None:
    status_payload = load_round_status(round_dir)
    stages = status_payload.get("blocked_stages", {})
    if stages.get("knowledge_digest", {}).get("status") != "ready":
        raise SystemExit("knowledge_digest is not ready; scorecard cannot run before the Feishu knowledge gate is cleared")
    if stages.get("xhs_collection", {}).get("status") != "ready":
        raise SystemExit("xhs_collection is not ready; scorecard cannot run before the Xiaohongshu evidence gate is cleared")

    digest = load_json(round_dir / "knowledge_digest.json")
    if not digest.get("brand_truths") or not digest.get("principle_cards"):
        raise SystemExit("knowledge_digest.json is still placeholder-like; rebuild it from a real Feishu source before scoring")


def append_worklog(round_dir: Path, message: str) -> None:
    worklog_path = round_dir / "worklog.md"
    if not worklog_path.exists():
        return
    current = worklog_path.read_text(encoding="utf-8")
    if "## Scorecard Updates" not in current:
        current += "\n## Scorecard Updates\n\n"
    current += f"- {message}\n"
    worklog_path.write_text(current, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-dir", required=True, type=Path, help="round directory")
    args = parser.parse_args()

    round_dir = args.round_dir.resolve()
    require_real_shared_inputs(round_dir)
    collector_dir = round_dir / "collector"
    evidence_pack = load_json(collector_dir / "xhs_evidence_pack.json")
    pattern_digest = load_json(collector_dir / "viral_pattern_digest.json")
    claw_bridge = load_json(collector_dir / "claw_topic_bridge.json")

    collector_score = score_collector(evidence_pack, pattern_digest, claw_bridge)
    workflow_scores = []
    for workflow in WORKFLOWS:
        submission = load_json(round_dir / "submissions" / workflow / "submission.json")
        workflow_scores.append(score_submission(submission, evidence_pack))

    workflow_scores.sort(key=lambda item: item["total"], reverse=True)
    leaderboard = [item["workflow_name"] for item in workflow_scores]
    notes = []
    if workflow_scores:
        notes.append(f"{workflow_scores[0]['workflow_name']} 当前领先。")
    if any(item["workflow_name"] == "n8n" and item["breakdown"]["platform_fit"] >= 14 for item in workflow_scores):
        notes.append("n8n 在平台边界说明上表现强，但仍需证明内容转译质量。")

    weekly_scorecard = {
        "round_id": round_dir.name,
        "generated_at": now_iso(),
        "collector_score": collector_score,
        "workflow_scores": workflow_scores,
        "selection_outlook": {
            "leaderboard": leaderboard,
            "current_leader": leaderboard[0] if leaderboard else "",
            "notes": notes,
        },
    }
    dump_json(round_dir / "scorecards" / "weekly_scorecard.json", weekly_scorecard)
    status_payload = load_round_status(round_dir)
    status_payload["generated_at"] = weekly_scorecard["generated_at"]
    status_payload.setdefault("blocked_stages", {})
    status_payload["blocked_stages"]["workflow_submissions"] = {
        "status": "ready",
        "reason": "four_workflow_submissions_scored",
        "artifact": str(round_dir / "submissions"),
    }
    status_payload["blocked_stages"]["weekly_scorecard"] = {
        "status": "ready",
        "reason": "weekly_scorecard_generated",
        "artifact": str(round_dir / "scorecards" / "weekly_scorecard.json"),
    }
    status_payload["status"] = compute_round_top_status(status_payload)
    refresh_completion_checks(status_payload)
    dump_json(round_dir / "round_status.json", status_payload)
    append_worklog(
        round_dir,
        (
            f"{weekly_scorecard['generated_at']}: 已生成真实 weekly_scorecard，当前 leader="
            f"{weekly_scorecard['selection_outlook']['current_leader'] or 'unknown'}。"
        ),
    )
    render_supervision_artifacts(round_dir)
    print(round_dir / "scorecards" / "weekly_scorecard.json")


if __name__ == "__main__":
    main()
