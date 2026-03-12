"""Runnable example adapter chain for the short-video growth workflow."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .contracts import (
    AnalyticsImportAdapter,
    AnalyticsSnapshot,
    DraftGenerator,
    DraftPackage,
    EvolutionRuleCandidate,
    EvolutionRuleExtractor,
    NormalizedTopicLead,
    PublishPackage,
    PublishPackageAdapter,
    TopicRanker,
    TopicScore,
    TopicSourceAdapter,
)


class JsonTopicSourceAdapter(TopicSourceAdapter):
    """Load normalized topic leads from a JSON file."""

    def __init__(self, source_path: str) -> None:
        self.source_path = Path(source_path)

    def collect(self) -> list[NormalizedTopicLead]:
        payload = json.loads(self.source_path.read_text(encoding="utf-8"))
        return [NormalizedTopicLead(**item) for item in payload]


class WeightedTopicRanker(TopicRanker):
    """Score topics using weighted metadata hints when available."""

    def score(self, lead: NormalizedTopicLead, notes: str = "") -> TopicScore:
        metadata = lead.metadata
        curiosity = float(metadata.get("curiosity_signal", self._fallback_signal(lead.title)))
        substance = float(metadata.get("substance_signal", self._fallback_signal(lead.summary)))
        relevance = float(metadata.get("relevance_signal", self._fallback_relevance(lead)))
        final_score = round((curiosity * 0.35) + (substance * 0.30) + (relevance * 0.35), 2)
        shortlisted = final_score >= 8.6
        if notes:
            shortlisted = shortlisted or "强推" in notes
        return TopicScore(
            curiosity=curiosity,
            substance=substance,
            relevance=relevance,
            final_score=final_score,
            shortlisted=shortlisted,
        )

    @staticmethod
    def _fallback_signal(text: str) -> float:
        return min(9.5, 6.5 + (len(text.strip()) / 60.0))

    @staticmethod
    def _fallback_relevance(lead: NormalizedTopicLead) -> float:
        haystack = " ".join([lead.title, lead.summary, " ".join(lead.topic_tags)])
        return 9.0 if "创业" in haystack or "原力" in haystack else 7.6


class LocalDocDraftGenerator(DraftGenerator):
    """Create a local markdown doc artifact for a selected topic."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, topic_row: dict[str, Any]) -> DraftPackage:
        draft_id = topic_row.get("draft_id", "draft-001")
        title = topic_row.get("title", "未命名选题")
        document_path = self.output_dir / f"{draft_id}.md"
        lines = [
            f"# {title}",
            "",
            "## Story Angle",
            topic_row.get("story_angle", ""),
            "",
            "## Anti-Consensus Insight",
            topic_row.get("anti_consensus_insight", ""),
            "",
            "## Hook",
            topic_row.get("hook", ""),
            "",
            "## 原力创业收束",
            topic_row.get("force_tie_back", ""),
            "",
        ]
        document_path.write_text("\n".join(lines), encoding="utf-8")
        return DraftPackage(
            draft_id=draft_id,
            doc_url=str(document_path),
            status="researching",
            payload={"document_path": str(document_path)},
        )


class LocalPublishPackageAdapter(PublishPackageAdapter):
    """Write a publish package JSON file for human confirmation."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, draft_row: dict[str, Any]) -> PublishPackage:
        draft_id = draft_row["draft_id"]
        platforms = draft_row.get("platforms", ["视频号", "小红书"])
        payload = {
            "draft_id": draft_id,
            "title_options": draft_row.get("title_options", []),
            "hook": draft_row.get("hook", ""),
            "summary": draft_row.get("summary", ""),
            "tags": draft_row.get("tags", []),
            "cover_prompt": draft_row.get("cover_prompt", ""),
            "suggested_publish_time": draft_row.get("suggested_publish_time", ""),
            "platforms": platforms,
            "status": "pending_human_confirmation",
        }
        package_path = self.output_dir / f"{draft_id}-publish-package.json"
        package_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return PublishPackage(draft_id=draft_id, platforms=platforms, payload=payload)


class CsvAnalyticsImportAdapter(AnalyticsImportAdapter):
    """Import one metrics export CSV into normalized snapshots."""

    def import_metrics(self, source_path: str) -> list[AnalyticsSnapshot]:
        snapshots: list[AnalyticsSnapshot] = []
        with Path(source_path).open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                metrics = {
                    "plays": int(row["plays"]),
                    "completion_rate": float(row["completion_rate"]),
                    "engagement_rate": float(row["engagement_rate"]),
                    "likes": int(row["likes"]),
                    "comments": int(row["comments"]),
                    "shares": int(row["shares"]),
                    "saves": int(row["saves"]),
                    "new_followers": int(row["new_followers"]),
                    "leads": int(row["leads"]),
                    "qualitative_diagnosis": row["qualitative_diagnosis"],
                    "repeat": row["repeat"],
                    "avoid": row["avoid"],
                    "rule_candidate": row["rule_candidate"],
                }
                snapshots.append(
                    AnalyticsSnapshot(
                        draft_id=row["draft_id"],
                        platform=row["platform"],
                        metrics=metrics,
                        import_status="imported",
                    )
                )
        return snapshots


class SimpleEvolutionRuleExtractor(EvolutionRuleExtractor):
    """Lift one structured rule from an imported review row."""

    def extract(self, review_row: dict[str, Any]) -> list[EvolutionRuleCandidate]:
        rule_statement = review_row.get("rule_candidate", "").strip()
        if not rule_statement:
            return []
        return [
            EvolutionRuleCandidate(
                draft_id=review_row["draft_id"],
                platform=review_row["platform"],
                rule_statement=rule_statement,
                rule_type="story",
                evidence_strength="single-review",
                metadata={
                    "repeat": review_row.get("repeat", ""),
                    "avoid": review_row.get("avoid", ""),
                },
            )
        ]
