"""Short-video growth workflow blueprint and domain constants."""

from __future__ import annotations

from dataclasses import dataclass


TOPIC_CANDIDATE_STATES = [
    "captured",
    "ranked",
    "shortlisted",
    "selected",
    "rejected",
    "archived",
]

CONTENT_DRAFT_STATES = [
    "researching",
    "drafting",
    "ready_for_publish",
    "published",
    "review_pending",
    "reviewed",
    "evolved",
]

NOTIFICATION_NODES = [
    "shortlist_ready",
    "selected_topic_created_draft",
    "draft_stalled",
    "publish_package_ready",
    "review_overdue",
    "evolution_rule_added",
]


@dataclass(frozen=True)
class ShortVideoGrowthBlueprint:
    platforms: tuple[str, str]
    metrics_focus: tuple[str, str]
    topic_ingest_mode: str
    publish_mode: str
    analytics_mode: str


def build_blueprint() -> ShortVideoGrowthBlueprint:
    return ShortVideoGrowthBlueprint(
        platforms=("视频号", "小红书"),
        metrics_focus=("completion_rate", "engagement_rate"),
        topic_ingest_mode="scheduled-ai-plus-manual",
        publish_mode="semi-automatic-human-confirmed",
        analytics_mode="semi-automatic-import",
    )
