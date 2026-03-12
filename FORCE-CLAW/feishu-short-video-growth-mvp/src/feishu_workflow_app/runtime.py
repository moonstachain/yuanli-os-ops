"""Local runtime helpers for the short-video growth MVP."""

from __future__ import annotations

import json
import re
from hashlib import sha1
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .adapters.example_short_video_chain import (
    CsvAnalyticsImportAdapter,
    JsonTopicSourceAdapter,
    LocalDocDraftGenerator,
    LocalPublishPackageAdapter,
    SimpleEvolutionRuleExtractor,
    WeightedTopicRanker,
)


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if slug:
        return slug
    return f"topic-{sha1(value.encode('utf-8')).hexdigest()[:10]}"


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


@dataclass(frozen=True)
class ProjectPaths:
    project_root: Path
    workflow_pack: Path
    runtime_root: Path
    docs_dir: Path
    publish_dir: Path
    state_dir: Path

    @classmethod
    def for_project_root(cls, project_root: Path, runtime_dir: str | None = None) -> "ProjectPaths":
        runtime_root = Path(runtime_dir).expanduser().resolve() if runtime_dir else project_root / "runtime-artifacts"
        workflow_pack = project_root / "workflow-pack" / "short-video-growth"
        return cls(
            project_root=project_root,
            workflow_pack=workflow_pack,
            runtime_root=runtime_root,
            docs_dir=runtime_root / "docs",
            publish_dir=runtime_root / "publish",
            state_dir=runtime_root / "state",
        )

    def ensure(self) -> None:
        for path in (self.runtime_root, self.docs_dir, self.publish_dir, self.state_dir):
            path.mkdir(parents=True, exist_ok=True)


class ShortVideoMvpRuntime:
    """Drive the local short-video workflow without external dependencies."""

    def __init__(self, project_root: Path, runtime_dir: str | None = None) -> None:
        self.paths = ProjectPaths.for_project_root(project_root, runtime_dir)
        self.paths.ensure()
        self.ranker = WeightedTopicRanker()
        self.draft_generator = LocalDocDraftGenerator(str(self.paths.docs_dir))
        self.publish_adapter = LocalPublishPackageAdapter(str(self.paths.publish_dir))
        self.analytics_adapter = CsvAnalyticsImportAdapter()
        self.rule_extractor = SimpleEvolutionRuleExtractor()

    def _read_json(self, path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _state_path(self, name: str) -> Path:
        return self.paths.state_dir / name

    def ingest_topics(
        self,
        source_path: str | None = None,
        manual_notes: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        notes = manual_notes or {}
        source = Path(source_path).expanduser().resolve() if source_path else self.paths.workflow_pack / "sample-topic-leads.json"
        leads = JsonTopicSourceAdapter(str(source)).collect()
        ranked: list[dict[str, Any]] = []
        for lead in leads:
            note = notes.get(lead.title, "")
            score = self.ranker.score(lead, notes=note)
            ranked.append(
                {
                    "title": lead.title,
                    "source": lead.source,
                    "reference": lead.reference,
                    "summary": lead.summary,
                    "topic_tags": lead.topic_tags,
                    "trend_reason": lead.trend_reason,
                    "captured_at": lead.captured_at,
                    "manual_note": note,
                    "curiosity_score": score.curiosity,
                    "substance_score": score.substance,
                    "relevance_score": score.relevance,
                    "final_score": score.final_score,
                    "status": "ranked",
                }
            )

        ranked.sort(key=lambda item: item["final_score"], reverse=True)
        shortlist = []
        for index, item in enumerate(ranked):
            if index < 3:
                item["status"] = "shortlisted"
                shortlist.append(item["title"])

        payload = {
            "generated_at": _now(),
            "source_path": str(source),
            "topic_count": len(ranked),
            "shortlist": shortlist,
            "topics": ranked,
        }
        self._write_json(self._state_path("topic_candidates_ranked.json"), payload)
        return payload

    def _load_ranked_topics(self) -> dict[str, Any]:
        path = self._state_path("topic_candidates_ranked.json")
        if not path.exists():
            return self.ingest_topics()
        return self._read_json(path)

    def create_draft(self, selected_title: str | None = None, selected_rank: int = 1) -> dict[str, Any]:
        ranked = self._load_ranked_topics()
        topics = ranked["topics"]
        if selected_title:
            selected = next((item for item in topics if item["title"] == selected_title), None)
        else:
            shortlist = [item for item in topics if item["status"] == "shortlisted"]
            selected = shortlist[max(0, selected_rank - 1)] if shortlist else topics[0]
        if selected is None:
            raise ValueError("selected topic not found")

        draft_id = f"draft-{_slugify(selected['title'])[:32]}"
        title_options = [
            selected["title"],
            f"为什么{selected['title'].split('，')[0]}",
            f"{selected['title'].split('，')[0]}，给创业者的一记反常识提醒",
        ]
        draft_row = {
            "draft_id": draft_id,
            "topic_title": selected["title"],
            "title": selected["title"],
            "summary": selected["summary"],
            "story_angle": selected["summary"],
            "anti_consensus_insight": selected["trend_reason"],
            "original_evidence_clues": selected["reference"],
            "hook": title_options[1],
            "story_arc": "人物/事件切入 -> 冲突升级 -> 反认知揭示 -> 回收至原力创业",
            "key_beats": [
                "开场给冲突",
                "补一个猎奇细节",
                "揭示被忽视的结构性原因",
                "回收到原力创业相关性",
            ],
            "payoff": "把表层热闹翻译成底层判断力",
            "force_tie_back": "把故事中的结构优势、慢变量或判断偏差自然回收至原力创业。",
            "platforms": ["视频号", "小红书"],
            "title_options": title_options,
            "tags": selected["topic_tags"],
            "cover_prompt": f"人物故事感，强冲突，突出关键词：{selected['topic_tags'][0] if selected['topic_tags'] else '创业'}",
            "suggested_publish_time": "20:00",
            "status": "drafting",
        }
        generated = self.draft_generator.generate(draft_row)
        payload = {
            **draft_row,
            "doc_url": generated.doc_url,
            "draft_status": generated.status,
            "generated_at": _now(),
            "source_topic": selected,
        }
        self._write_json(self._state_path("content_draft.json"), payload)
        return payload

    def _load_draft(self) -> dict[str, Any]:
        path = self._state_path("content_draft.json")
        if not path.exists():
            return self.create_draft()
        return self._read_json(path)

    def build_publish_package(self) -> dict[str, Any]:
        draft = self._load_draft()
        package = self.publish_adapter.build(draft)
        payload = {
            "generated_at": _now(),
            "draft_id": draft["draft_id"],
            "doc_url": draft["doc_url"],
            "payload": package.payload,
        }
        self._write_json(self._state_path("publish_package.json"), payload)
        return payload

    def import_metrics(self, source_path: str | None = None) -> dict[str, Any]:
        source = Path(source_path).expanduser().resolve() if source_path else self.paths.workflow_pack / "sample-platform-metrics.csv"
        snapshots = self.analytics_adapter.import_metrics(str(source))
        rows = []
        for snapshot in snapshots:
            row = {
                "draft_id": snapshot.draft_id,
                "platform": snapshot.platform,
                **snapshot.metrics,
                "import_status": snapshot.import_status,
            }
            rows.append(row)
        payload = {
            "generated_at": _now(),
            "source_path": str(source),
            "review_count": len(rows),
            "reviews": rows,
        }
        self._write_json(self._state_path("performance_reviews.json"), payload)
        return payload

    def extract_rules(self) -> dict[str, Any]:
        reviews = self._read_json(self._state_path("performance_reviews.json")) if self._state_path("performance_reviews.json").exists() else self.import_metrics()
        rules = []
        for review in reviews["reviews"]:
            rules.extend(self.rule_extractor.extract(review))
        payload = {
            "generated_at": _now(),
            "rule_count": len(rules),
            "rules": [
                {
                    "draft_id": rule.draft_id,
                    "platform": rule.platform,
                    "rule_statement": rule.rule_statement,
                    "rule_type": rule.rule_type,
                    "evidence_strength": rule.evidence_strength,
                    "metadata": rule.metadata,
                }
                for rule in rules
            ],
        }
        self._write_json(self._state_path("evolution_rules.json"), payload)
        return payload

    def full_run(self, selected_title: str | None = None, selected_rank: int = 1) -> dict[str, Any]:
        ingest = self.ingest_topics()
        draft = self.create_draft(selected_title=selected_title, selected_rank=selected_rank)
        publish = self.build_publish_package()
        reviews = self.import_metrics()
        rules = self.extract_rules()
        summary = {
            "generated_at": _now(),
            "shortlist": ingest["shortlist"],
            "selected_topic": draft["topic_title"],
            "doc_url": draft["doc_url"],
            "publish_platforms": publish["payload"]["platforms"],
            "review_count": reviews["review_count"],
            "rule_count": rules["rule_count"],
            "artifacts_dir": str(self.paths.runtime_root),
        }
        self._write_json(self._state_path("full_run_summary.json"), summary)
        return summary
