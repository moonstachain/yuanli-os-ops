#!/usr/bin/env python3
"""Repository-level validation for the yuanli-os-ops migration bundle."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "README.md",
    ROOT / ".gitignore",
    ROOT / "bootstrap/BOOTSTRAP_CONTRACT.md",
    ROOT / "bootstrap/ENVIRONMENT_CHECKLIST.md",
    ROOT / "bootstrap/CONNECTION_ORDER.md",
    ROOT / "bootstrap/COLLABORATION_PROTOCOL.md",
    ROOT / "bootstrap/HEALTHCHECK.md",
    ROOT / "bootstrap/HEALTHCHECK_CONTRACT.md",
    ROOT / "bootstrap/SKILLS_MANIFEST.md",
    ROOT / "bootstrap/REMOTE_CONTROL_RUNBOOK.md",
    ROOT / "bootstrap/MIGRATION_MANIFEST.json",
    ROOT / "FORCE-CLAW/YUANLI_OS.md",
    ROOT / "FORCE-CLAW/YUANLI_OS_3X3_EVOLUTION.md",
    ROOT / "FORCE-CLAW/YUANLI_OS_3X3_WECHAT_PLAYBOOK.md",
    ROOT / "FORCE-CLAW/YUANLI_OS_SYSTEM_AUDIT_REPORT.md",
    ROOT / "FORCE-CLAW/BLUEPRINT.md",
    ROOT / "FORCE-CLAW/scripts/sync_yuanli_os_audit_to_feishu.py",
    ROOT / "FORCE-CLAW/references/yuanli-os-feishu-base-schema.json",
    ROOT / "FORCE-CLAW/references/yuanli-os-external-intel-seed.json",
    ROOT / "FORCE-CLAW/feishu-short-video-growth-mvp/README.md",
    ROOT / "FORCE-CLAW/dify-short-video-content-system/README.md",
    ROOT / "FORCE-CLAW/clawd-workspace/force-claw-content-race-mvp/README.md",
    ROOT / "tools/feishu-bitable-bridge/scripts/feishu_bitable_bridge.py",
]


def main() -> int:
    errors: list[str] = []
    for path in REQUIRED:
        if not path.exists():
            errors.append(f"missing: {path.relative_to(ROOT)}")

    sync_script = ROOT / "FORCE-CLAW/scripts/sync_yuanli_os_audit_to_feishu.py"
    if sync_script.exists():
        text = sync_script.read_text(encoding="utf-8")
        for needle in [
            'Path("/Users/liming/.codex/skills',
            'Path("/Users/liming/AI Project',
        ]:
            if needle in text:
                errors.append(f"source-machine path still hardcoded in sync script: {needle}")

    if errors:
        print("FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("OK")
    print(f"root: {ROOT}")
    print(f"required_paths: {len(REQUIRED)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
