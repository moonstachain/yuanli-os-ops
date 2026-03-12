#!/usr/bin/env python3
"""Run the local short-video growth MVP demo end-to-end."""

from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from feishu_workflow_app.runtime import ShortVideoMvpRuntime


def main() -> None:
    project_root = Path(__file__).resolve().parent
    runtime = ShortVideoMvpRuntime(project_root=project_root)
    summary = runtime.full_run()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
