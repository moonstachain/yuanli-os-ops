"""Environment-backed settings for the generated scaffold."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    project_name: str
    workflow_name: str
    workflow_template: str
    feishu_app_id: str
    feishu_app_secret: str
    feishu_verify_token: str
    feishu_encrypt_key: str
    host: str
    port: int
    project_root: str
    runtime_artifact_dir: str

    @classmethod
    def from_env(cls) -> "Settings":
        project_root = os.getenv("PROJECT_ROOT", str(Path(__file__).resolve().parents[2]))
        return cls(
            project_name=os.getenv("PROJECT_NAME", "feishu-short-video-growth-mvp"),
            workflow_name=os.getenv("WORKFLOW_NAME", "原力创业短视频增长MVP"),
            workflow_template=os.getenv("WORKFLOW_TEMPLATE", "short-video-growth"),
            feishu_app_id=os.getenv("FEISHU_APP_ID", ""),
            feishu_app_secret=os.getenv("FEISHU_APP_SECRET", ""),
            feishu_verify_token=os.getenv("FEISHU_VERIFY_TOKEN", ""),
            feishu_encrypt_key=os.getenv("FEISHU_ENCRYPT_KEY", ""),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            project_root=project_root,
            runtime_artifact_dir=os.getenv(
                "RUNTIME_ARTIFACT_DIR",
                str(Path(project_root) / "runtime-artifacts"),
            ),
        )
