"""Very small HTTP server for webhook and health-check scaffolding."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .config import Settings
from .runtime import ShortVideoMvpRuntime


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")


def build_handler(settings: Settings) -> type[BaseHTTPRequestHandler]:
    runtime = ShortVideoMvpRuntime(
        project_root=Path(settings.project_root),
        runtime_dir=settings.runtime_artifact_dir,
    )

    class Handler(BaseHTTPRequestHandler):
        server_version = "FeishuWorkflowBuilder/0.1"

        def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
            body = _json_bytes(payload)
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/health":
                self._send_json(
                    {
                        "status": "ok",
                        "project_name": settings.project_name,
                        "workflow_name": settings.workflow_name,
                        "workflow_template": settings.workflow_template,
                        "project_root": settings.project_root,
                        "runtime_artifact_dir": settings.runtime_artifact_dir,
                    }
                )
                return

            self._send_json({"error": "not_found", "path": self.path}, HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:  # noqa: N802
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length) if content_length else b""
            payload = json.loads(raw_body.decode("utf-8") or "{}")

            if self.path == "/jobs/topic-ingest":
                result = runtime.ingest_topics(
                    source_path=payload.get("source_path"),
                    manual_notes=payload.get("manual_notes"),
                )
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path == "/jobs/create-draft":
                result = runtime.create_draft(
                    selected_title=payload.get("selected_title"),
                    selected_rank=int(payload.get("selected_rank", 1)),
                )
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path == "/jobs/publish-package":
                result = runtime.build_publish_package()
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path == "/jobs/import-metrics":
                result = runtime.import_metrics(source_path=payload.get("source_path"))
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path == "/jobs/extract-rules":
                result = runtime.extract_rules()
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path == "/jobs/full-run":
                result = runtime.full_run(
                    selected_title=payload.get("selected_title"),
                    selected_rank=int(payload.get("selected_rank", 1)),
                )
                self._send_json({"code": 0, "message": "ok", "result": result})
                return

            if self.path != "/events":
                self._send_json({"error": "not_found", "path": self.path}, HTTPStatus.NOT_FOUND)
                return

            challenge = payload.get("challenge")
            if challenge:
                self._send_json({"challenge": challenge})
                return

            self._send_json(
                {
                    "code": 0,
                    "message": "received",
                    "project_name": settings.project_name,
                    "event_type": payload.get("header", {}).get("event_type"),
                }
            )

        def log_message(self, format: str, *args: object) -> None:
            print(f"[{settings.project_name}] {self.address_string()} - {format % args}")

    return Handler


def run_server(settings: Settings) -> None:
    server = ThreadingHTTPServer((settings.host, settings.port), build_handler(settings))
    print(
        json.dumps(
                {
                    "status": "starting",
                    "project_name": settings.project_name,
                    "workflow_name": settings.workflow_name,
                    "workflow_template": settings.workflow_template,
                    "host": settings.host,
                    "port": settings.port,
                },
            ensure_ascii=False,
        )
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(
            json.dumps(
                {"status": "stopping", "project_name": settings.project_name},
                ensure_ascii=False,
            )
        )
    finally:
        server.server_close()
