#!/usr/bin/env python3
"""Normalize raw XHS samples into race artifacts."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from content_race_common import (
    AVOID_PATTERN_LABELS,
    FIT_PATTERN_LABELS,
    QUERY_BUCKETS,
    SURFACES,
    dedupe_samples,
    dump_json,
    load_json,
    now_iso,
    ratio_counter,
)


def load_samples(raw_samples_dir: Path) -> list[dict[str, Any]]:
    return [load_json(path) for path in sorted(raw_samples_dir.glob("*.json"))]


def build_method_log(round_id: str, raw_samples: list[dict[str, Any]], samples: list[dict[str, Any]], notes: list[str]) -> dict[str, Any]:
    return {
        "round_id": round_id,
        "generated_at": now_iso(),
        "raw_sample_count": len(raw_samples),
        "deduped_sample_count": len(samples),
        "query_buckets": sorted({sample.get("bucket", "") for sample in samples if sample.get("bucket")}),
        "queries": sorted({sample.get("query", "") for sample in samples if sample.get("query")}),
        "surfaces": sorted({sample.get("surface", "") for sample in samples if sample.get("surface")}),
        "dedupe_rule": "post_id > post_url > sample_id",
        "sampling_rules": {
            "author_concentration_cap": 0.2,
            "query_concentration_cap": 0.25,
            "required_surfaces": SURFACES,
            "required_buckets": QUERY_BUCKETS,
        },
        "anomalies": notes,
    }


def build_evidence_pack(round_id: str, samples: list[dict[str, Any]]) -> dict[str, Any]:
    negative_notes = [sample["negative_note"] for sample in samples if sample.get("negative_note")]
    return {
        "round_id": round_id,
        "generated_at": now_iso(),
        "query_buckets": sorted({sample.get("bucket", "") for sample in samples if sample.get("bucket")}),
        "coverage": {
            "sample_count": len(samples),
            "surfaces": sorted({sample.get("surface", "") for sample in samples if sample.get("surface")}),
            "author_concentration": round(ratio_counter([sample.get("author", "unknown") for sample in samples]), 3),
            "query_concentration": round(ratio_counter([sample.get("query", "unknown") for sample in samples]), 3),
        },
        "samples": samples,
        "negative_notes": negative_notes,
    }


def infer_pattern_explanation(dimension: str, label: str) -> str:
    if label in {"认知升级", "原理翻转"}:
        return "通过打破旧前提、给出新框架，提高收藏和转述概率。"
    if label in {"边界判断", "选型省错"}:
        return "帮助读者做平台与流程判断，天然适合收藏。"
    if label in {"避坑", "效率承诺"}:
        return "把风险和收益说清，能提升实际决策价值。"
    if dimension == "format_type":
        return "固定格式降低理解成本，更容易被快速消费。"
    return "这是当前样本中反复出现的高频传播结构。"


def build_pattern_digest(round_id: str, samples: list[dict[str, Any]]) -> dict[str, Any]:
    counters: Counter[tuple[str, str]] = Counter()
    refs: dict[tuple[str, str], list[str]] = {}
    for sample in samples:
        sample_id = sample.get("sample_id", "")
        for dimension in ("hook_type", "promise_type", "format_type"):
            label = sample.get(dimension)
            if not label:
                continue
            key = (dimension, label)
            counters[key] += 1
            refs.setdefault(key, []).append(sample_id)

    patterns = []
    for index, ((dimension, label), count) in enumerate(counters.most_common(7), start=1):
        patterns.append(
            {
                "pattern_id": f"pattern-{index}",
                "label": label,
                "dimension": dimension,
                "count": count,
                "evidence_refs": refs[(dimension, label)],
                "explanation": infer_pattern_explanation(dimension, label),
            }
        )
    return {
        "round_id": round_id,
        "generated_at": now_iso(),
        "patterns": patterns,
    }


def build_claw_bridge(round_id: str, pattern_digest: dict[str, Any]) -> dict[str, Any]:
    fit_patterns = []
    avoid_patterns = []
    for pattern in pattern_digest.get("patterns", []):
        label = pattern["label"]
        if label in FIT_PATTERN_LABELS:
            fit_patterns.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "reason": "该模式更容易转成 CLAW 的流程原理和证据导向表达。",
                }
            )
        elif label in AVOID_PATTERN_LABELS:
            avoid_patterns.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "reason": "该模式偏情绪或偏流量，容易让 CLAW 失真。",
                }
            )
        else:
            avoid_patterns.append(
                {
                    "pattern_id": pattern["pattern_id"],
                    "reason": "该模式可借鉴，但必须补充流程、证据和边界说明后再使用。",
                }
            )
    return {
        "round_id": round_id,
        "generated_at": now_iso(),
        "fit_patterns": fit_patterns,
        "avoid_patterns": avoid_patterns,
        "translation_rules": [
            "优先把热点转成流程原理，而不是平台八卦。",
            "封面可以锋利，但正文必须给出最小可验证步骤。",
            "不要把外部新闻热度直接当成小红书热度。",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-dir", required=True, type=Path, help="round directory")
    args = parser.parse_args()

    round_dir = args.round_dir.resolve()
    raw_samples_dir = round_dir / "collector" / "raw_samples"
    raw_samples = load_samples(raw_samples_dir)
    samples, notes = dedupe_samples(raw_samples)

    method_log = build_method_log(round_dir.name, raw_samples, samples, notes)
    evidence_pack = build_evidence_pack(round_dir.name, samples)
    pattern_digest = build_pattern_digest(round_dir.name, samples)
    claw_bridge = build_claw_bridge(round_dir.name, pattern_digest)

    collector_dir = round_dir / "collector"
    dump_json(collector_dir / "xhs_collection_method_log.json", method_log)
    dump_json(collector_dir / "xhs_evidence_pack.json", evidence_pack)
    dump_json(collector_dir / "viral_pattern_digest.json", pattern_digest)
    dump_json(collector_dir / "claw_topic_bridge.json", claw_bridge)
    print(collector_dir)


if __name__ == "__main__":
    main()
