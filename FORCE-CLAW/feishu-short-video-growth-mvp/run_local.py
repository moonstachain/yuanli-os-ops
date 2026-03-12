#!/usr/bin/env python3
"""Run the local Feishu workflow scaffold."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from feishu_workflow_app.config import Settings
from feishu_workflow_app.server import run_server


def main() -> None:
    settings = Settings.from_env()
    run_server(settings)


if __name__ == "__main__":
    main()
