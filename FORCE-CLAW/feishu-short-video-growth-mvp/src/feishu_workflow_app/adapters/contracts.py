"""Replaceable adapter contracts for workflow-specific integrations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class NormalizedTopicLead:
    title: str
    source: str
    reference: str
    summary: str
    topic_tags: list[str]
    trend_reason: str
    captured_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TopicScore:
    curiosity: float
    substance: float
    relevance: float
    final_score: float
    shortlisted: bool


@dataclass
class DraftPackage:
    draft_id: str
    doc_url: str
    status: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class PublishPackage:
    draft_id: str
    platforms: list[str]
    payload: dict[str, Any]
    human_confirmation_required: bool = True


@dataclass
class AnalyticsSnapshot:
    draft_id: str
    platform: str
    metrics: dict[str, Any]
    import_status: str


@dataclass
class EvolutionRuleCandidate:
    draft_id: str
    platform: str
    rule_statement: str
    rule_type: str
    evidence_strength: str
    metadata: dict[str, Any] = field(default_factory=dict)


class TopicSourceAdapter(Protocol):
    def collect(self) -> list[NormalizedTopicLead]:
        """Collect and normalize topic leads from one source."""


class TopicRanker(Protocol):
    def score(self, lead: NormalizedTopicLead, notes: str = "") -> TopicScore:
        """Score one normalized topic lead."""


class DraftGenerator(Protocol):
    def generate(self, topic_row: dict[str, Any]) -> DraftPackage:
        """Create the linked draft record and Doc artifact."""


class PublishPackageAdapter(Protocol):
    def build(self, draft_row: dict[str, Any]) -> PublishPackage:
        """Build a semi-automatic publish package."""


class AnalyticsImportAdapter(Protocol):
    def import_metrics(self, source_path: str) -> list[AnalyticsSnapshot]:
        """Import one exported metrics batch."""


class EvolutionRuleExtractor(Protocol):
    def extract(self, review_row: dict[str, Any]) -> list[EvolutionRuleCandidate]:
        """Extract reusable lessons from one review row."""
