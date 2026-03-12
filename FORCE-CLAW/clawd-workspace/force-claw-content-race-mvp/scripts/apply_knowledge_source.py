#!/usr/bin/env python3
"""Replace the round Feishu source URL and rebuild knowledge_digest from a Feishu extract."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from content_race_common import (
    compute_round_top_status,
    dump_json,
    load_json,
    load_round_status,
    now_iso,
    refresh_completion_checks,
)
from update_supervision_status import render_supervision_artifacts


NOISE_PATTERNS = (
    r"^(登录/注册|立即编辑|搜索|目录|分享知识库|评论|使用指南|效率指南|外部|分享)$",
    r"^(数据表|仪表盘|文档|文件夹|应用|表格|新建|筛选|分组|排序|行高|填色)$",
    r"^\d+$",
)


def normalize_lines(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if len(line) < 6:
            continue
        if any(re.match(pattern, line) for pattern in NOISE_PATTERNS):
            continue
        lines.append(line)
    seen = set()
    unique = []
    for line in lines:
        if line in seen:
            continue
        seen.add(line)
        unique.append(line)
    return unique


def pick_brand_truths(lines: list[str]) -> list[str]:
    return [line for line in lines if len(line) >= 12][:3]


def pick_principle_cards(lines: list[str]) -> list[dict[str, str]]:
    cards = []
    for index, line in enumerate(lines[:5], start=1):
        cards.append(
            {
                "id": f"p-{index}",
                "title": line[:30],
                "summary": line,
            }
        )
    return cards


def pick_jobs(lines: list[str]) -> list[str]:
    jobs = [line for line in lines if any(token in line for token in ("适合", "帮助", "目标", "用户", "团队"))]
    return jobs[:3]


def pick_banned_angles(lines: list[str]) -> list[str]:
    banned = [line for line in lines if any(token in line for token in ("不要", "禁止", "避免", "不应"))]
    return banned[:3]


def pick_language_notes(lines: list[str], title: str) -> list[str]:
    notes = [line for line in lines if any(token in line for token in ("表达", "风格", "语言", "语气"))]
    if not notes and title:
        notes = [f"当前知识源标题为《{title}》，后续表达应与该主题保持一致。"]
    return notes[:3]


def build_digest(source_url: str, extract: dict, captured_at: str) -> dict:
    text = extract.get("text", "")
    top_lines = extract.get("metadata", {}).get("top_lines", [])
    title = extract.get("title") or extract.get("metadata", {}).get("document_title", "")
    lines = normalize_lines("\n".join(top_lines) + "\n" + text)

    brand_truths = pick_brand_truths(lines)
    principle_cards = pick_principle_cards(lines)
    audience_jobs = pick_jobs(lines)
    banned_angles = pick_banned_angles(lines)
    language_notes = pick_language_notes(lines, title)

    if not brand_truths or not principle_cards:
        raise ValueError("extract does not contain enough semantic lines to build knowledge_digest")

    return {
        "source_url": source_url,
        "captured_at": captured_at,
        "brand_truths": brand_truths,
        "principle_cards": principle_cards,
        "audience_jobs": audience_jobs,
        "banned_angles": banned_angles,
        "language_notes": language_notes,
    }


def append_worklog(round_dir: Path, message: str) -> None:
    worklog_path = round_dir / "worklog.md"
    if not worklog_path.exists():
        return
    current = worklog_path.read_text(encoding="utf-8")
    if "## Knowledge Source Updates" not in current:
        current += "\n## Knowledge Source Updates\n\n"
    current += f"- {message}\n"
    worklog_path.write_text(current, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-dir", required=True, type=Path)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--source-json", type=Path)
    parser.add_argument("--replace-only", action="store_true")
    parser.add_argument("--min-text-length", type=int, default=500)
    args = parser.parse_args()

    round_dir = args.round_dir.resolve()
    captured_at = now_iso()
    digest_path = round_dir / "knowledge_digest.json"
    current_digest = load_json(digest_path) if digest_path.exists() else {}
    current_digest["source_url"] = args.source_url

    status_payload = load_round_status(round_dir)
    status_payload["generated_at"] = captured_at

    if args.replace_only:
        dump_json(digest_path, current_digest)
        append_worklog(round_dir, f"{captured_at}: 已将知识源 URL 更新为 {args.source_url}，等待新的读取产物。")
        render_supervision_artifacts(round_dir)
        print(digest_path)
        return

    if not args.source_json:
        raise SystemExit("--source-json is required unless --replace-only is used")

    extract = load_json(args.source_json.resolve())
    if extract.get("status") != "ok":
        raise SystemExit(f"source extract status is {extract.get('status')}, not safe to build knowledge_digest")
    if len((extract.get("text") or "").strip()) < args.min_text_length:
        raise SystemExit("source extract text is too short to build a reliable knowledge_digest")

    digest = build_digest(args.source_url, extract, captured_at)
    dump_json(digest_path, digest)

    status_payload.setdefault("blocked_stages", {})
    status_payload["blocked_stages"]["knowledge_digest"] = {
        "status": "ready",
        "reason": "knowledge_digest_built_from_feishu_source",
        "artifact": str(digest_path),
    }
    status_payload["status"] = compute_round_top_status(status_payload)
    refresh_completion_checks(status_payload)
    dump_json(round_dir / "round_status.json", status_payload)
    render_supervision_artifacts(round_dir)
    append_worklog(
        round_dir,
        f"{captured_at}: 已从 {args.source_url} 重建 knowledge_digest，并将 knowledge_digest 阶段标记为 ready。",
    )
    print(digest_path)


if __name__ == "__main__":
    main()
