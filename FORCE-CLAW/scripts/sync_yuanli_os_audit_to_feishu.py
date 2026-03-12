#!/usr/bin/env python3
"""Build and sync the 原力OS system audit bundle into Feishu Bitable."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path
from typing import Any
from urllib import request as urllib_request


REPO_ROOT = Path(__file__).resolve().parents[2]
FORCE_CLAW_ROOT = REPO_ROOT / "FORCE-CLAW"
CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).expanduser()
SKILLS_ROOT = CODEX_HOME / "skills"
AI_DA_GUAN_JIA_ROOT = Path(
    os.environ.get("AI_DA_GUAN_JIA_ROOT", str(SKILLS_ROOT / "ai-da-guan-jia"))
).expanduser()
OS_YUANLI_ROOT = Path(os.environ.get("OS_YUANLI_ROOT", str(SKILLS_ROOT / "os-yuanli"))).expanduser()
DEFAULT_REPORT_PATH = FORCE_CLAW_ROOT / "YUANLI_OS_SYSTEM_AUDIT_REPORT.md"
DEFAULT_SCHEMA_PATH = FORCE_CLAW_ROOT / "references" / "yuanli-os-feishu-base-schema.json"
DEFAULT_EXTERNAL_SEED_PATH = FORCE_CLAW_ROOT / "references" / "yuanli-os-external-intel-seed.json"
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "output" / "yuanli-os-feishu-sync"
DEFAULT_FEISHU_LINK = os.environ.get(
    "YUANLI_OS_FEISHU_LINK",
    "https://h52xu4gwob.feishu.cn/wiki/DdNXw06poicDHHkSKIdcRrYDnod?from=from_copylink",
)
DEFAULT_ACCOUNT_ID = os.environ.get("YUANLI_OS_FEISHU_ACCOUNT_ID", "feishu-claw")
DEFAULT_OWNER = "OS-原力"
BRIDGE_PATH = REPO_ROOT / "tools" / "feishu-bitable-bridge" / "scripts" / "feishu_bitable_bridge.py"
USER_AGENT = "yuanli-os-feishu-sync/1.0"

SYSTEM_OBJECT_KEY = "system"
SUBSYSTEM_KEYS = {
    "原力OS理论与文档层": "subsystem::theory-docs",
    "根层协议与总入口层": "subsystem::root-entry",
    "skill 生态层": "subsystem::skill-ecology",
    "任务与 runtime 行为层": "subsystem::runtime-behavior",
    "领域证明层": "subsystem::domain-proof",
}
SAMPLE_KEYS = {
    "公众号内容链": "sample::wechat-content-chain",
    "AI大管家 skill review / inventory": "sample::ai-da-guan-jia-review",
    "guan-jia-claw canonical task + run": "sample::guan-jia-claw-canonical",
    "内容赛马 / 短视频增长实验": "sample::content-race-short-video",
}
AXIS_TO_FIELD = {
    "主题层": "主题层分",
    "策略层": "策略层分",
    "执行层": "执行层分",
    "递归进化": "递归进化分",
    "全局最优": "全局最优分",
    "人类友好": "人类友好分",
}
SECTION_AXIS = {
    "4.2": "主题层",
    "4.3": "策略层",
    "4.4": "执行层",
    "4.5": "递归进化",
    "4.6": "全局最优",
    "4.7": "人类友好",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-path", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--schema-path", type=Path, default=DEFAULT_SCHEMA_PATH)
    parser.add_argument("--external-seed-path", type=Path, default=DEFAULT_EXTERNAL_SEED_PATH)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--link", default=DEFAULT_FEISHU_LINK)
    parser.add_argument("--account-id", default=DEFAULT_ACCOUNT_ID)
    parser.add_argument(
        "--sync-scope",
        choices=["full", "internal", "external"],
        default="full",
        help="full writes all tables; internal skips HTTP refresh; external refreshes benchmark metadata then rewrites all tables.",
    )
    parser.add_argument("--run-id", help="Override audit run id. Defaults to yuanli-audit-YYYYMMDD-HHMMSS.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[`'\"“”‘’]+", "", text)
    text = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", text)
    return text.strip("-") or "item"


def parse_score(value: str) -> float:
    text = value.strip()
    if not text:
        return 0.0
    if "/" in text:
        text = text.split("/", 1)[0]
    try:
        return float(text)
    except ValueError:
        return 0.0


def parse_markdown_table(section: str) -> list[dict[str, str]]:
    lines = [line.strip() for line in section.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        return []
    header = [cell.strip() for cell in lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < len(header):
            continue
        rows.append(dict(zip(header, cells)))
    return rows


def collect_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^###\s+([0-9]+\.[0-9]+)\s+(.+)$", text, re.M))
    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        sections[match.group(1)] = text[start:end]
    return sections


def extract_h2_section(text: str, title_prefix: str) -> str:
    match = re.search(rf"^##\s+{re.escape(title_prefix)}.*$", text, re.M)
    if not match:
        return ""
    start = match.start()
    next_match = re.search(r"^##\s+[0-9]+\..*$", text[match.end():], re.M)
    end = match.end() + next_match.start() if next_match else len(text)
    return text[start:end]


def extract_score_and_grade(section: str) -> tuple[float, str]:
    score_match = re.search(r"`(?:系统总分|得分|样本评分)：\s*([0-9.]+)\s*/\s*10`", section)
    grade_match = re.search(r"`等级：\s*([A-Z][+]?)`", section)
    return (
        float(score_match.group(1)) if score_match else 0.0,
        grade_match.group(1) if grade_match else "",
    )


def extract_paragraph_after(label: str, section: str) -> str:
    lines = section.splitlines()
    target = f"{label}："
    for idx, line in enumerate(lines):
        if line.strip() != target:
            continue
        collected: list[str] = []
        for candidate in lines[idx + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                if collected:
                    break
                continue
            if re.match(r"^(###|##)\s+", stripped):
                break
            if stripped.endswith("：") and not stripped.startswith("- ") and collected:
                break
            collected.append(stripped.lstrip("- ").strip())
        return " ".join(collected)
    return ""


def extract_bullets(section: str) -> list[str]:
    bullets = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def extract_judgment_value(section: str, label: str) -> str:
    match = re.search(rf"-\s+`?{re.escape(label)}`?\s+(.*?)(?:\n-\s+`|\Z)", section, re.S)
    if not match:
        return ""
    return " ".join(line.strip() for line in match.group(1).splitlines() if line.strip())


def object_meta(object_key: str) -> dict[str, str]:
    if object_key == SYSTEM_OBJECT_KEY:
        return {"对象类型": "system", "对象名称": "OS-原力 全系统", "父对象": ""}
    for name, key in SUBSYSTEM_KEYS.items():
        if key == object_key:
            return {"对象类型": "subsystem", "对象名称": name, "父对象": SYSTEM_OBJECT_KEY}
    for name, key in SAMPLE_KEYS.items():
        if key == object_key:
            return {"对象类型": "sample", "对象名称": name, "父对象": SYSTEM_OBJECT_KEY}
    return {"对象类型": "object", "对象名称": object_key, "父对象": SYSTEM_OBJECT_KEY}


def latest_ai_review_paths() -> tuple[Path | None, Path | None]:
    root = AI_DA_GUAN_JIA_ROOT / "artifacts" / "ai-da-guan-jia" / "reviews"
    candidates = sorted(root.glob("**/review.md"))
    review_md = candidates[-1] if candidates else None
    review_json = review_md.with_name("review.json") if review_md and review_md.with_name("review.json").exists() else None
    return review_md, review_json


def collect_internal_evidence(run_id: str) -> list[dict[str, str]]:
    review_md, review_json = latest_ai_review_paths()
    entries: list[tuple[str, str, Path | None, str, str, str]] = [
        (
            SYSTEM_OBJECT_KEY,
            "report",
            DEFAULT_REPORT_PATH,
            "当前系统总审计报告",
            "当前系统总分、子系统分、扣分账本和路线图都以该报告为主源。",
            "评分卡总表,扣分与差距,进化动作",
        ),
        (
            "subsystem::theory-docs",
            "doc",
            FORCE_CLAW_ROOT / "YUANLI_OS.md",
            "原力OS 总纲",
            "定义治理OS与工作OS的总结构。",
            "评分卡总表,内部证据",
        ),
        (
            "subsystem::theory-docs",
            "doc",
            FORCE_CLAW_ROOT / "YUANLI_OS_3X3_EVOLUTION.md",
            "3×3 二阶演化框架",
            "定义治理求解器、工作分类器与系统层级。",
            "评分卡总表,内部证据",
        ),
        (
            "subsystem::theory-docs",
            "doc",
            FORCE_CLAW_ROOT / "YUANLI_OS_3X3_WECHAT_PLAYBOOK.md",
            "公众号实战应用说明书",
            "把三层方法落到高频内容任务。",
            "领域证明层,内部证据",
        ),
        (
            "subsystem::root-entry",
            "skill",
            OS_YUANLI_ROOT / "SKILL.md",
            "OS-原力 root skill",
            "规定六判断、三层 gate、验真与进化顺序。",
            "根层协议与总入口层,评分卡总表",
        ),
        (
            "subsystem::root-entry",
            "reference",
            OS_YUANLI_ROOT / "references" / "task-family-map.md",
            "任务族映射",
            "定义研究审计与治理协作的高阶混合模式。",
            "根层协议与总入口层,递归队列",
        ),
        (
            SYSTEM_OBJECT_KEY,
            "reference",
            OS_YUANLI_ROOT / "references" / "audit-rubric.md",
            "审计评分标准",
            "6 轴 × 10 分模型是系统审计的固定评分器。",
            "检查点明细,评分卡总表",
        ),
        (
            SYSTEM_OBJECT_KEY,
            "reference",
            OS_YUANLI_ROOT / "references" / "system-audit-playbook.md",
            "系统行为审计 playbook",
            "规定 Inquiry Brief 到 Evolution Note 的高阶审计路径。",
            "审计批次,进化动作",
        ),
        (
            "subsystem::runtime-behavior",
            "runtime",
            FORCE_CLAW_ROOT / "clawd-workspace/guan-jia-claw-workspace/state/task-ledger.json",
            "canonical task ledger",
            "现有 canonical task 状态和字段缺口以 ledger 为准。",
            "任务与 runtime 行为层,扣分与差距",
        ),
        (
            "sample::wechat-content-chain",
            "pilot",
            FORCE_CLAW_ROOT / "clawd-workspace/guan-jia-claw-workspace/runtime-artifacts/pilots/wechat-demo-smoke/pilot-manifest.json",
            "公众号 demo pilot",
            "证明公众号链已经形成 verified 阶段式证据链。",
            "领域证明层,评分卡总表",
        ),
        (
            "sample::content-race-short-video",
            "experiment",
            FORCE_CLAW_ROOT / "clawd-workspace/force-claw-content-race-mvp/runtime-artifacts/runs/real-round-20260310-01/round_status.json",
            "内容赛马状态",
            "显示 blocked_auth_or_access_gate 与 not_closed 的真实阻塞。",
            "扣分与差距,递归队列",
        ),
        (
            "sample::content-race-short-video",
            "experiment",
            FORCE_CLAW_ROOT / "feishu-short-video-growth-mvp/runtime-artifacts/state/full_run_summary.json",
            "短视频增长实验状态",
            "领域证明层的实验类证据样本。",
            "领域证明层,评分卡总表",
        ),
    ]
    if review_md:
        entries.append(
            (
                "subsystem::skill-ecology",
                "review",
                review_md,
                "AI大管家 review.md",
                "技能树强弱区块、中层缺口与候选动作都以 review 为主源。",
                "skill 生态层,扣分与差距",
            )
        )
    if review_json:
        entries.append(
            (
                "subsystem::skill-ecology",
                "review",
                review_json,
                "AI大管家 review.json",
                "供结构化读取 normalized skills 与 findings。",
                "skill 生态层,内部证据",
            )
        )

    rows: list[dict[str, str]] = []
    for object_key, source_type, path, summary, conclusion, reuse in entries:
        if path is None or not path.exists():
            continue
        stat = path.stat()
        evidence_key = f"{run_id}::{object_key}::{slugify(path.name)}"
        rows.append(
            {
                "Internal Evidence Key": evidence_key,
                "Object Key": object_key,
                "来源类型": source_type,
                "来源路径": str(path),
                "canonical 标记": "yes",
                "时间戳": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "证据摘要": summary,
                "抽取结论": conclusion,
                "复用去向": reuse,
            }
        )
    return rows


def fetch_url_metadata(url: str) -> dict[str, str]:
    req = urllib_request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib_request.urlopen(req, timeout=20) as response:
        html = response.read(160000).decode("utf-8", errors="ignore")
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
        title = unescape(title_match.group(1)).strip() if title_match else ""
        return {"final_url": response.geturl(), "title": re.sub(r"\s+", " ", title)}


def freshness_score(captured_on: str) -> int:
    try:
        captured = date.fromisoformat(captured_on)
    except ValueError:
        return 5
    age = (date.today() - captured).days
    if age <= 90:
        return 10
    if age <= 365:
        return 8
    if age <= 730:
        return 6
    return 4


def build_external_rows(seed: dict[str, Any], refresh: bool) -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, float]]:
    sources = seed.get("sources") or []
    mappings = seed.get("mappings") or []
    source_by_key = {item["external_intel_key"]: item for item in sources if isinstance(item, dict)}
    external_rows: list[dict[str, str]] = []
    mapping_rows: list[dict[str, str]] = []

    for item in sources:
        if not isinstance(item, dict):
            continue
        key = str(item["external_intel_key"])
        fetched_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = str(item.get("source_title") or "")
        final_url = str(item.get("source_url") or "")
        if refresh:
            try:
                meta = fetch_url_metadata(final_url)
                final_url = meta["final_url"] or final_url
                title = meta["title"] or title
            except Exception:
                pass
        fresh = freshness_score(str(item.get("captured_on") or ""))
        external_rows.append(
            {
                "External Intel Key": key,
                "主题/对象": str(item.get("topic_or_object") or ""),
                "来源类型": str(item.get("source_type") or ""),
                "来源 URL": final_url,
                "来源标题": title,
                "权威级别": str(item.get("authority_level") or ""),
                "抓取日期": fetched_at,
                "新鲜度": str(fresh),
                "摘要": str(item.get("summary") or ""),
                "最佳实践结论": str(item.get("best_practice_conclusion") or ""),
                "置信度": str(item.get("confidence") or ""),
                "相关度": str(item.get("relevance") or ""),
            }
        )

    benchmark_scores: dict[str, list[float]] = {}
    for mapping in mappings:
        if not isinstance(mapping, dict):
            continue
        source = source_by_key.get(str(mapping.get("external_intel_key") or ""))
        if not source:
            continue
        fresh = freshness_score(str(source.get("captured_on") or ""))
        authority = float(mapping.get("authority") or 0)
        relevance = float(mapping.get("relevance") or 0)
        reuse = float(mapping.get("reuse") or 0)
        gap_value = float(mapping.get("gap_value") or 0)
        score = round((authority + relevance + fresh + reuse + gap_value) / 5.0, 1)
        object_key = str(mapping.get("object_key") or "")
        benchmark_key = f"{source['external_intel_key']}::{object_key}"
        benchmark_scores.setdefault(object_key, []).append(score)
        mapping_rows.append(
            {
                "Benchmark Link Key": benchmark_key,
                "External Intel Key": str(source["external_intel_key"]),
                "Object Key": object_key,
                "权威性": f"{authority:.1f}",
                "相关性": f"{relevance:.1f}",
                "新鲜度": f"{fresh:.1f}",
                "可复用性": f"{reuse:.1f}",
                "差距价值": f"{gap_value:.1f}",
                "外部对标分": f"{score:.1f}",
                "本地差距说明": str(mapping.get("local_gap") or ""),
                "适配结论": str(mapping.get("adaptation") or ""),
                "状态": str(mapping.get("status") or "active"),
            }
        )
    averaged = {key: round(sum(values) / len(values), 1) for key, values in benchmark_scores.items() if values}
    return external_rows, mapping_rows, averaged


def build_checkpoint_rows(
    run_id: str,
    sections: dict[str, str],
    evidence_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    evidence_keys = [row["Internal Evidence Key"] for row in evidence_rows[:6]]
    checkpoint_rows: list[dict[str, str]] = []
    axis_deductions: dict[str, str] = {}
    for section_id, axis in SECTION_AXIS.items():
        section = sections.get(section_id, "")
        rows = parse_markdown_table(section)
        deduction = extract_paragraph_after("关键扣分", section)
        axis_deductions[axis] = deduction
        for row in rows:
            checkpoint = str(row.get("检查点") or "")
            score = str(row.get("分数") or "0")
            score_num = parse_score(score)
            status = "已形成" if score_num >= 2 else "部分形成" if score_num >= 1 else "缺口"
            checkpoint_rows.append(
                {
                    "Checkpoint Key": f"{run_id}::{SYSTEM_OBJECT_KEY}::{slugify(axis)}::{slugify(checkpoint)}",
                    "Audit Run ID": run_id,
                    "Object Key": SYSTEM_OBJECT_KEY,
                    "轴名": axis,
                    "检查点名": checkpoint,
                    "得分": f"{score_num:.1f}",
                    "状态": status,
                    "证据句": str(row.get("证据句") or ""),
                    "扣分原因": deduction,
                    "改进动作": deduction,
                    "证据键列表": "\n".join(evidence_keys),
                }
            )
    return checkpoint_rows, axis_deductions


def build_system_row(
    run_id: str,
    sections: dict[str, str],
    external_scores: dict[str, float],
) -> tuple[dict[str, str], dict[str, float], str]:
    table_rows = parse_markdown_table(sections["4.1"])
    axis_scores: dict[str, float] = {}
    key_deductions: list[str] = []
    for row in table_rows:
        axis = str(row.get("维度") or "").strip("`")
        axis_scores[axis] = parse_score(str(row.get("分数") or "0"))
        if row.get("关键扣分"):
            key_deductions.append(str(row["关键扣分"]))
    internal_score, grade = extract_score_and_grade(sections.get("1.1", ""))
    if internal_score <= 0:
        internal_score = round(sum(axis_scores.values()) / len(axis_scores), 1) if axis_scores else 0.0
    external_score = external_scores.get(SYSTEM_OBJECT_KEY, 0.0)
    composite = round(internal_score * 0.7 + external_score * 0.3, 1)
    row = {
        "Scorecard Key": f"{run_id}::{SYSTEM_OBJECT_KEY}",
        "Audit Run ID": run_id,
        "Object Key": SYSTEM_OBJECT_KEY,
        "对象类型": "system",
        "对象名称": "OS-原力 全系统",
        "父对象": "",
        "内部成熟度": f"{internal_score:.1f}",
        "外部对标分": f"{external_score:.1f}",
        "综合分": f"{composite:.1f}",
        "等级": grade,
        "关键扣分": "；".join(key_deductions),
        "下一步动作摘要": "先让评分标准和系统审计变成 OS-原力 的稳定器官。",
    }
    for axis, field in AXIS_TO_FIELD.items():
        row[field] = f"{axis_scores.get(axis, 0.0):.1f}" if axis in axis_scores else ""
    return row, axis_scores, grade


def build_section_scorecard(
    run_id: str,
    object_key: str,
    section: str,
) -> dict[str, str]:
    total_score, grade = extract_score_and_grade(section)
    rows = parse_markdown_table(section)
    row = {
        "Scorecard Key": f"{run_id}::{object_key}",
        "Audit Run ID": run_id,
        "Object Key": object_key,
        "内部成熟度": f"{total_score:.1f}",
        "外部对标分": "0.0",
        "综合分": f"{total_score * 0.7:.1f}",
        "等级": grade,
        "关键扣分": "",
        "下一步动作摘要": "",
    }
    row.update(object_meta(object_key))
    if object_key.startswith("subsystem::"):
        deductions: list[str] = []
        weakest_score = 99.0
        next_action = ""
        for axis_row in rows:
            axis = str(axis_row.get("维度") or "").strip("`")
            score = parse_score(str(axis_row.get("分数") or "0"))
            field = AXIS_TO_FIELD.get(axis)
            if field:
                row[field] = f"{score:.1f}"
            deduction = str(axis_row.get("扣分说明") or "")
            deductions.append(f"{axis}：{deduction}")
            if score < weakest_score:
                weakest_score = score
                next_action = deduction
        row["关键扣分"] = "；".join(deductions)
        row["下一步动作摘要"] = next_action
    else:
        for field in AXIS_TO_FIELD.values():
            row[field] = ""
        penalty = extract_paragraph_after("扣分点", section)
        why = extract_paragraph_after("为什么得这个分", section)
        row["关键扣分"] = penalty
        row["下一步动作摘要"] = why
    return row


def scorecard_with_external(
    row: dict[str, str],
    external_scores: dict[str, float],
) -> dict[str, str]:
    object_key = row["Object Key"]
    external_score = external_scores.get(object_key, 0.0)
    internal_score = parse_score(row.get("内部成熟度", "0"))
    row["外部对标分"] = f"{external_score:.1f}"
    row["综合分"] = f"{round(internal_score * 0.7 + external_score * 0.3, 1):.1f}"
    if external_score <= 0:
        deduction = row.get("关键扣分", "")
        extra = "缺少外部对标证据"
        row["关键扣分"] = f"{deduction}；{extra}".strip("；")
    return row


def infer_severity(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["最大", "not_closed", "blocked", "为空", "缺口", "不足"]):
        return "high"
    if any(token in lowered for token in ["仍", "还没有", "不够", "partial"]):
        return "medium"
    return "low"


def infer_layer(text: str) -> str:
    if "外部" in text or "对标" in text:
        return "全局最优"
    if "ledger" in text or "runtime" in text or "字段" in text:
        return "执行层"
    if "strategy" in text or "策略" in text:
        return "策略层"
    if "theme" in text or "主题" in text:
        return "主题层"
    if "人类" in text or "复杂度" in text:
        return "人类友好"
    return "递归进化"


def build_gap_rows(
    run_id: str,
    report_text: str,
    scorecards: list[dict[str, str]],
    mapping_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    section = extract_h2_section(report_text, "7.")
    rows = parse_markdown_table(section)
    gap_rows: list[dict[str, str]] = []
    for row in rows:
        gap_type = str(row.get("扣分项") or "")
        evidence = str(row.get("证据句") or "")
        repair = str(row.get("改进动作") or "")
        gap_slug = slugify(gap_type)
        gap_rows.append(
            {
                "Gap Key": f"{run_id}::{SYSTEM_OBJECT_KEY}::{gap_slug}",
                "Audit Run ID": run_id,
                "Object Key": SYSTEM_OBJECT_KEY,
                "差距类型": gap_type,
                "来源层": infer_layer(gap_type + repair),
                "严重度": infer_severity(evidence + repair),
                "当前状态": "observed",
                "目标状态": "closed",
                "阻塞原因": evidence,
                "证据键": evidence,
                "建议修复": repair,
                "状态": "open",
            }
        )
    covered_objects = {row["Object Key"] for row in mapping_rows}
    for scorecard in scorecards:
        object_key = scorecard["Object Key"]
        if object_key in covered_objects:
            continue
        object_name = scorecard["对象名称"]
        gap_rows.append(
            {
                "Gap Key": f"{run_id}::{object_key}::external-intel-gap",
                "Audit Run ID": run_id,
                "Object Key": object_key,
                "差距类型": "external_intel_gap",
                "来源层": "全局最优",
                "严重度": "medium",
                "当前状态": "missing_external_benchmark",
                "目标状态": "benchmarked",
                "阻塞原因": f"{object_name} 当前没有有效外部对标证据。",
                "证据键": "对标映射缺失",
                "建议修复": f"为 {object_name} 补充 GitHub / 官方文档 / 公开最佳实践 benchmark。",
                "状态": "open",
            }
        )
    return gap_rows


def build_action_rows(run_id: str, sections: dict[str, str], gap_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    actions: list[dict[str, str]] = []
    cadence_map = {"8.1": ("immediate", "high"), "8.2": ("30-90d", "medium"), "8.3": ("long-term", "low")}
    for section_id, (cadence, priority) in cadence_map.items():
        section = sections.get(section_id, "")
        lines = []
        for line in section.splitlines():
            stripped = line.strip()
            if re.match(r"^[0-9]+\.\s", stripped):
                lines.append(re.sub(r"^[0-9]+\.\s*", "", stripped))
        for idx, title in enumerate(lines, start=1):
            gap_key = ""
            for gap in gap_rows:
                if any(token in title for token in gap["差距类型"].split()):
                    gap_key = gap["Gap Key"]
                    break
            action_type = "repair" if cadence == "immediate" else "harden" if cadence == "30-90d" else "evolve"
            actions.append(
                {
                    "Action Key": f"{run_id}::{section_id}::{idx}",
                    "Audit Run ID": run_id,
                    "Gap Key": gap_key,
                    "动作标题": title,
                    "动作类型": action_type,
                    "负责人": DEFAULT_OWNER,
                    "优先级": priority,
                    "预期收益": "降低系统失真并提升下一轮审计分。",
                    "投入等级": "medium" if priority != "high" else "high",
                    "计划节奏": cadence,
                    "状态": "open",
                    "闭环证据": "",
                    "关闭时间": "",
                }
            )
    return actions


def build_recursion_rows(run_id: str, gap_rows: list[dict[str, str]], now: datetime) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for gap in gap_rows:
        gap_slug = gap["Gap Key"].split("::")[-1]
        is_external = gap["差距类型"] == "external_intel_gap" or gap["来源层"] == "全局最优"
        cadence = "weekly_external" if is_external else "daily_internal"
        next_run = now + timedelta(days=7 if is_external else 1)
        rows.append(
            {
                "Loop Key": f"{gap['Object Key']}::{gap_slug}",
                "Object Key": gap["Object Key"],
                "复审节奏": cadence,
                "触发类型": gap["差距类型"],
                "上次内部同步": now.strftime("%Y-%m-%d %H:%M:%S") if not is_external else "",
                "上次外部同步": now.strftime("%Y-%m-%d %H:%M:%S") if is_external else "",
                "下次运行": next_run.strftime("%Y-%m-%d %H:%M:%S"),
                "过期标记": "false",
                "阻塞": gap["阻塞原因"],
                "分数变化": "0.0",
                "是否自动开 gap": "yes",
            }
        )
    return rows


def build_bundle(args: argparse.Namespace) -> tuple[dict[str, Any], Path]:
    report_text = args.report_path.read_text(encoding="utf-8")
    sections = collect_sections(report_text)
    now = datetime.now()
    run_id = args.run_id or now.strftime("yuanli-audit-%Y%m%d-%H%M%S")
    run_dir = args.output_root / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    internal_evidence_rows = collect_internal_evidence(run_id)
    external_seed = load_json(args.external_seed_path)
    external_rows, mapping_rows, external_scores = build_external_rows(
        external_seed,
        refresh=args.sync_scope in {"full", "external"},
    )
    checkpoint_rows, axis_deductions = build_checkpoint_rows(run_id, sections, internal_evidence_rows)

    system_row, _, system_grade = build_system_row(run_id, sections, external_scores)
    system_row = scorecard_with_external(system_row, external_scores)

    scorecards = [system_row]
    for section_id, object_key in {
        "5.1": SUBSYSTEM_KEYS["原力OS理论与文档层"],
        "5.2": SUBSYSTEM_KEYS["根层协议与总入口层"],
        "5.3": SUBSYSTEM_KEYS["skill 生态层"],
        "5.4": SUBSYSTEM_KEYS["任务与 runtime 行为层"],
        "5.5": SUBSYSTEM_KEYS["领域证明层"],
        "6.1": SAMPLE_KEYS["公众号内容链"],
        "6.2": SAMPLE_KEYS["AI大管家 skill review / inventory"],
        "6.3": SAMPLE_KEYS["guan-jia-claw canonical task + run"],
        "6.4": SAMPLE_KEYS["内容赛马 / 短视频增长实验"],
    }.items():
        row = build_section_scorecard(run_id, object_key, sections[section_id])
        row = scorecard_with_external(row, external_scores)
        scorecards.append(row)

    gap_rows = build_gap_rows(run_id, report_text, scorecards, mapping_rows)
    action_rows = build_action_rows(run_id, sections, gap_rows)
    recursion_rows = build_recursion_rows(run_id, gap_rows, now)

    subsystem_rows = [row for row in scorecards if row["对象类型"] == "subsystem"]
    strongest = max(subsystem_rows, key=lambda item: parse_score(item["内部成熟度"]))["对象名称"]
    weakest = min(subsystem_rows, key=lambda item: parse_score(item["内部成熟度"]))["对象名称"]
    external_system_score = sum(parse_score(row["外部对标分"]) for row in subsystem_rows + [system_row]) / (len(subsystem_rows) + 1)
    batch_row = {
        "Audit Run ID": run_id,
        "审计日期": now.strftime("%Y-%m-%d"),
        "审计范围": "FORCE-CLAW + ~/.codex/skills + AI大管家历史行为",
        "时间边界": "2026-03-13 本地可检索快照",
        "mode": "full",
        "内部权重": "0.7",
        "外部权重": "0.3",
        "内部总分": system_row["内部成熟度"],
        "外部总分": f"{round(external_system_score, 1):.1f}",
        "综合分": system_row["综合分"],
        "等级": system_grade,
        "最强区块": strongest,
        "最弱区块": weakest,
        "当前最大失真": extract_judgment_value(sections.get("1.2", ""), "当前最大失真")
        or "技能树交通规则不足、runtime canonical 字段不够硬、部分实验停在 access gate 或 partial closure。",
        "状态": "applied" if args.apply else "preview_ready" if args.dry_run else "bundle_ready",
        "报告路径": str(args.report_path),
        "同步结果": str(run_dir / "sync-result.json"),
    }

    table_payloads = {
        "审计批次": [batch_row],
        "评分卡总表": scorecards,
        "检查点明细": checkpoint_rows,
        "扣分与差距": gap_rows,
        "进化动作": action_rows,
        "内部证据": internal_evidence_rows,
        "外部情报": external_rows,
        "对标映射": mapping_rows,
        "递归队列": recursion_rows,
    }

    for table_name, rows in table_payloads.items():
        save_json(run_dir / f"{slugify(table_name)}.json", rows)

    bundle = {
        "run_id": run_id,
        "generated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "sync_scope": args.sync_scope,
        "report_path": str(args.report_path),
        "schema_path": str(args.schema_path),
        "external_seed_path": str(args.external_seed_path),
        "table_payloads": table_payloads,
        "axis_deductions": axis_deductions,
    }
    save_json(run_dir / "bundle.json", bundle)
    return bundle, run_dir


def load_bridge_module() -> Any:
    spec = importlib.util.spec_from_file_location("yuanli_feishu_bridge", BRIDGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load bridge module from {BRIDGE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def upsert_rows(
    client: Any,
    bridge: Any,
    table_id: str,
    key_field: str,
    actual_primary_field: str,
    rows: list[dict[str, Any]],
    apply: bool,
) -> dict[str, int]:
    existing_records = client.list_records(table_id) if table_id else []
    index = bridge.existing_index(existing_records, actual_primary_field) if table_id else {}
    preview_create = 0
    preview_update = 0
    created = 0
    updated = 0
    for row in rows:
        key = str(row.get(key_field) or "").strip()
        if not key:
            raise ValueError(f"Row missing key field {key_field}: {row}")
        payload = dict(row)
        payload[actual_primary_field] = key
        if key in index:
            preview_update += 1
            if apply:
                client.update_record(table_id, str(index[key]["record_id"]), payload)
                updated += 1
        else:
            preview_create += 1
            if apply:
                client.create_record(table_id, payload)
                created += 1
    return {
        "would_create": preview_create,
        "would_update": preview_update,
        "created": created,
        "updated": updated,
    }


def sync_bundle(bundle: dict[str, Any], args: argparse.Namespace, run_dir: Path) -> dict[str, Any]:
    manifest = load_json(args.schema_path)
    table_specs = {item["table_name"]: item for item in manifest.get("tables", []) if isinstance(item, dict)}

    if args.dry_run and not args.apply:
        sync_tables: dict[str, Any] = {}
        for table_name, rows in bundle["table_payloads"].items():
            spec = table_specs[table_name]
            sync_tables[table_name] = {
                "primary_field": spec["primary_field"],
                "actual_primary_field": spec["primary_field"],
                "row_count": len(rows),
                "table_id": "",
                "ensure_table": {"status": "preview_skipped_remote"},
                "preview": {"would_create": len(rows), "would_update": 0},
                "result": {"created": 0, "updated": 0},
            }
        sync_result = {
            "ok": True,
            "run_id": bundle["run_id"],
            "mode": "dry-run",
            "sync_scope": args.sync_scope,
            "account_id": args.account_id,
            "base_token": "",
            "link": args.link,
            "tables": sync_tables,
            "note": "Local preview only. Remote Feishu calls are skipped until --apply is used.",
        }
        save_json(run_dir / "sync-result.json", sync_result)
        return sync_result

    bridge = load_bridge_module()
    creds = bridge.load_feishu_account(args.account_id)
    base_token = bridge.resolve_base_token(
        args.link,
        app_id=creds["app_id"],
        app_secret=creds["app_secret"],
    )
    client = bridge.FeishuBitableClient(creds["app_id"], creds["app_secret"], base_token)

    ensure_results: dict[str, Any] = {}
    for table_name, spec in table_specs.items():
        ensured = bridge.ensure_table(
            client,
            table_name=table_name,
            primary_field=str(spec["primary_field"]),
            field_names=[str(field) for field in spec.get("fields", [])],
            apply=bool(args.apply),
        )
        ensure_results[table_name] = ensured

    sync_tables: dict[str, Any] = {}
    for table_name, rows in bundle["table_payloads"].items():
        spec = table_specs[table_name]
        ensured = ensure_results[table_name]
        actual_primary_field = str(spec["primary_field"])
        table_id = ensured.get("table_id") or ""
        if table_id:
            current_fields = client.list_fields(table_id)
            primary = next((item for item in current_fields if item.get("is_primary")), None)
            if primary and primary.get("field_name"):
                actual_primary_field = str(primary["field_name"])
        result = {
            "primary_field": spec["primary_field"],
            "actual_primary_field": actual_primary_field,
            "row_count": len(rows),
            "table_id": table_id,
            "ensure_table": ensured,
            "preview": {"would_create": 0, "would_update": 0},
            "result": {"created": 0, "updated": 0},
        }
        if table_id:
            counts = upsert_rows(
                client,
                bridge,
                table_id,
                str(spec["primary_field"]),
                actual_primary_field,
                rows,
                bool(args.apply),
            )
            result["preview"]["would_create"] = counts["would_create"]
            result["preview"]["would_update"] = counts["would_update"]
            result["result"]["created"] = counts["created"]
            result["result"]["updated"] = counts["updated"]
        sync_tables[table_name] = result

    sync_result = {
        "ok": True,
        "run_id": bundle["run_id"],
        "mode": "apply" if args.apply else "dry-run" if args.dry_run else "bundle-only",
        "sync_scope": args.sync_scope,
        "account_id": args.account_id,
        "base_token": base_token,
        "link": args.link,
        "tables": sync_tables,
    }
    save_json(run_dir / "sync-result.json", sync_result)
    return sync_result


def main() -> int:
    args = parse_args()
    try:
        bundle, run_dir = build_bundle(args)
        sync_result = sync_bundle(bundle, args, run_dir) if args.apply or args.dry_run else {
            "ok": True,
            "run_id": bundle["run_id"],
            "mode": "bundle-only",
        }
        print(
            json.dumps(
                {
                    "status": "ok",
                    "run_id": bundle["run_id"],
                    "run_dir": str(run_dir),
                    "mode": sync_result["mode"],
                    "tables": {name: len(rows) for name, rows in bundle["table_payloads"].items()},
                    "sync_result": sync_result,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
