#!/usr/bin/env python3
"""Minimal Feishu Bitable bridge for AI大管家 sync workflows."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import parse as urllib_parse
from urllib import request as urllib_request


FEISHU_AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
FEISHU_API_BASE = "https://open.feishu.cn/open-apis/bitable/v1"
TEXT_FIELD_TYPE = 1
DEFAULT_ACCOUNT_ID = "feishu-claw"
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
KNOWN_BASE_TOKEN_BY_TABLE = {}
KNOWN_BASE_TOKEN_BY_LINK_FRAGMENT = {}


def json_request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    body = None
    request_headers = {"User-Agent": "ai-da-guan-jia-feishu-bridge/1.0"}
    if headers:
        request_headers.update(headers)
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers["Content-Type"] = "application/json; charset=utf-8"
    req = urllib_request.Request(url, data=body, headers=request_headers, method=method.upper())
    with urllib_request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_stdout(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def load_feishu_account(account_id: str) -> dict[str, str]:
    if OPENCLAW_CONFIG.exists():
        config = read_json(OPENCLAW_CONFIG)
        accounts = (((config.get("channels") or {}).get("feishu") or {}).get("accounts") or {})
        account = accounts.get(account_id) or {}
        app_id = str(account.get("appId") or "").strip()
        app_secret = str(account.get("appSecret") or "").strip()
        if app_id and app_secret:
            return {"app_id": app_id, "app_secret": app_secret}

    app_id = str(os.getenv("FEISHU_APP_ID") or "").strip()
    app_secret = str(os.getenv("FEISHU_APP_SECRET") or "").strip()
    if app_id and app_secret:
        return {"app_id": app_id, "app_secret": app_secret}

    raise RuntimeError(
        f"Missing Feishu account credentials for accountId={account_id}. "
        "Provide ~/.openclaw/openclaw.json or set FEISHU_APP_ID and FEISHU_APP_SECRET."
    )


def fetch_tenant_access_token(app_id: str, app_secret: str) -> str:
    result = json_request(
        "POST",
        FEISHU_AUTH_URL,
        payload={"app_id": app_id, "app_secret": app_secret},
    )
    if result.get("code") != 0:
        raise RuntimeError(f"Feishu auth failed: {result}")
    return str(result["tenant_access_token"])


def resolve_base_token(
    link: str,
    *,
    app_id: str,
    app_secret: str,
    table_id: str | None = None,
) -> str:
    for env_name in (
        "FEISHU_BITABLE_BRIDGE_BASE_TOKEN",
        "AI_DA_GUAN_JIA_FEISHU_BASE_TOKEN",
        "AI_DA_GUAN_JIA_REVIEW_FEISHU_BASE_TOKEN",
    ):
        value = str(os.getenv(env_name) or "").strip()
        if value:
            return value

    if table_id and table_id in KNOWN_BASE_TOKEN_BY_TABLE:
        return KNOWN_BASE_TOKEN_BY_TABLE[table_id]

    parsed = urllib_parse.urlparse(link)
    params = urllib_parse.parse_qs(parsed.query)
    for candidate in params.get("table", []):
        if candidate in KNOWN_BASE_TOKEN_BY_TABLE:
            return KNOWN_BASE_TOKEN_BY_TABLE[candidate]

    path_parts = [part for part in parsed.path.split("/") if part]
    for part in path_parts:
        if part in KNOWN_BASE_TOKEN_BY_LINK_FRAGMENT:
            return KNOWN_BASE_TOKEN_BY_LINK_FRAGMENT[part]
    if "wiki" in path_parts:
        wiki_index = path_parts.index("wiki")
        if wiki_index + 1 < len(path_parts):
            node_token = path_parts[wiki_index + 1]
            tenant_token = fetch_tenant_access_token(app_id, app_secret)
            wiki_result = json_request(
                "GET",
                f"https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token={urllib_parse.quote(node_token)}",
                headers={"Authorization": f"Bearer {tenant_token}"},
            )
            if wiki_result.get("code") != 0:
                raise RuntimeError(f"Failed to resolve wiki node token {node_token}: {wiki_result}")
            node = (wiki_result.get("data") or {}).get("node") or {}
            obj_type = str(node.get("obj_type") or "")
            obj_token = str(node.get("obj_token") or "")
            if obj_type == "bitable" and obj_token:
                return obj_token

    raise RuntimeError(
        "Unable to resolve Feishu Bitable base token from link. "
        "Set AI_DA_GUAN_JIA_FEISHU_BASE_TOKEN explicitly."
    )


def parse_link(link: str) -> dict[str, str]:
    parsed = urllib_parse.urlparse(link)
    params = urllib_parse.parse_qs(parsed.query)
    return {
        "table_id": (params.get("table") or [""])[0],
        "view_id": (params.get("view") or [""])[0],
    }


class FeishuBitableClient:
    def __init__(self, app_id: str, app_secret: str, base_token: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_token = base_token
        self._tenant_access_token: str | None = None

    def _auth_headers(self) -> dict[str, str]:
        if not self._tenant_access_token:
            result = json_request(
                "POST",
                FEISHU_AUTH_URL,
                payload={"app_id": self.app_id, "app_secret": self.app_secret},
            )
            if result.get("code") != 0:
                raise RuntimeError(f"Feishu auth failed: {result}")
            self._tenant_access_token = result["tenant_access_token"]
        return {"Authorization": f"Bearer {self._tenant_access_token}"}

    def _api(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        query: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{FEISHU_API_BASE}{path}"
        if query:
            url = f"{url}?{urllib_parse.urlencode(query)}"
        result = json_request(method, url, headers=self._auth_headers(), payload=payload)
        if result.get("code") != 0:
            raise RuntimeError(f"Feishu API failed {path}: {result}")
        return result

    def list_tables(self) -> list[dict[str, Any]]:
        result = self._api("GET", f"/apps/{self.base_token}/tables")
        return ((result.get("data") or {}).get("items") or [])

    def create_table(self, name: str) -> dict[str, Any]:
        result = self._api("POST", f"/apps/{self.base_token}/tables", payload={"table": {"name": name}})
        data = result.get("data") or {}
        return (data.get("table") or data or {})

    def list_fields(self, table_id: str) -> list[dict[str, Any]]:
        result = self._api("GET", f"/apps/{self.base_token}/tables/{table_id}/fields", query={"page_size": 100})
        return ((result.get("data") or {}).get("items") or [])

    def create_field(self, table_id: str, field_name: str, field_type: int = TEXT_FIELD_TYPE) -> dict[str, Any]:
        result = self._api(
            "POST",
            f"/apps/{self.base_token}/tables/{table_id}/fields",
            payload={"field_name": field_name, "type": field_type},
        )
        return ((result.get("data") or {}).get("field") or {})

    def update_field_name(self, table_id: str, field_id: str, field_name: str) -> None:
        self._api(
            "PUT",
            f"/apps/{self.base_token}/tables/{table_id}/fields/{field_id}",
            payload={"field_name": field_name},
        )

    def list_records(self, table_id: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            query = {"page_size": 500}
            if page_token:
                query["page_token"] = page_token
            result = self._api("GET", f"/apps/{self.base_token}/tables/{table_id}/records", query=query)
            data = result.get("data") or {}
            records.extend(data.get("items") or [])
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")
        return records

    def create_record(self, table_id: str, fields: dict[str, Any]) -> None:
        self._api("POST", f"/apps/{self.base_token}/tables/{table_id}/records", payload={"fields": fields})

    def update_record(self, table_id: str, record_id: str, fields: dict[str, Any]) -> None:
        self._api("PUT", f"/apps/{self.base_token}/tables/{table_id}/records/{record_id}", payload={"fields": fields})


def normalize_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        return [payload]
    if isinstance(payload, list) and all(isinstance(item, dict) for item in payload):
        return payload
    raise ValueError("payload-file must contain a JSON object or a list of JSON objects")


def existing_index(records: list[dict[str, Any]], primary_field: str) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for record in records:
        fields = record.get("fields") or {}
        key = fields.get(primary_field)
        if key not in (None, ""):
            index[str(key)] = record
    return index


def ensure_table(
    client: FeishuBitableClient,
    *,
    table_name: str,
    primary_field: str,
    field_names: list[str],
    apply: bool,
) -> dict[str, Any]:
    tables = client.list_tables()
    table = next((item for item in tables if item.get("name") == table_name), None)
    table_existed = table is not None
    if not table and apply:
        table = client.create_table(table_name)
        time.sleep(0.5)
    if not table:
        return {
            "table_name": table_name,
            "table_id": "",
            "primary_field": primary_field,
            "existed": False,
            "created": False,
            "missing_fields": field_names,
        }

    table_id = str(table.get("table_id") or "")
    existing_fields = client.list_fields(table_id)
    primary = next((item for item in existing_fields if item.get("is_primary")), None)
    if primary and primary.get("field_name") != primary_field and apply:
        try:
            client.update_field_name(table_id, str(primary["field_id"]), primary_field)
            time.sleep(0.2)
        except Exception:
            pass

    current_names = {str(item.get("field_name") or "") for item in client.list_fields(table_id)}
    missing_fields = [name for name in field_names if name not in current_names]
    if apply:
        for field_name in missing_fields:
            client.create_field(table_id, field_name)
            time.sleep(0.2)
    return {
        "table_name": table_name,
        "table_id": table_id,
        "primary_field": primary_field,
        "existed": table_existed,
        "created": (not table_existed) and bool(table_id),
        "missing_fields": missing_fields,
    }


def command_upsert_records(args: argparse.Namespace) -> int:
    payload = read_json(Path(args.payload_file))
    rows = normalize_rows(payload)
    account_id = str(args.account_id or os.getenv("FEISHU_BITABLE_BRIDGE_ACCOUNT_ID") or DEFAULT_ACCOUNT_ID)
    link_meta = parse_link(args.link)
    table_id = str(args.table_id or link_meta["table_id"] or "").strip()
    primary_field = str(args.primary_field or "").strip()
    if not primary_field:
        raise ValueError("--primary-field is required")
    creds = load_feishu_account(account_id)
    base_token = resolve_base_token(
        args.link,
        app_id=creds["app_id"],
        app_secret=creds["app_secret"],
        table_id=table_id or None,
    )
    client = FeishuBitableClient(creds["app_id"], creds["app_secret"], base_token)

    inferred_fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in inferred_fields:
                inferred_fields.append(str(key))

    table_created = False
    ensured: dict[str, Any] | None = None
    if not table_id:
        table_name = str(args.table_name or os.getenv("FEISHU_BITABLE_BRIDGE_DEFAULT_TABLE_NAME") or "AI大管家-运行日志")
        ensured = ensure_table(
            client,
            table_name=table_name,
            primary_field=primary_field,
            field_names=inferred_fields,
            apply=bool(args.apply),
        )
        table_id = ensured["table_id"]
        table_created = bool(ensured.get("created"))

    if not table_id:
        write_json_stdout(
            {
                "ok": True,
                "mode": "dry-run",
                "status": "preview_ready",
                "apply": False,
                "table_id": "",
                "table_created": table_created,
                "primary_field": primary_field,
                "row_count": len(rows),
                "preview": {"would_create": len(rows), "would_update": 0},
                "ensure_table": ensured,
            }
        )
        return 0

    existing_records = client.list_records(table_id)
    index = existing_index(existing_records, primary_field)
    would_create = 0
    would_update = 0
    for row in rows:
        key = str(row.get(primary_field) or "").strip()
        if not key:
            raise ValueError(f"payload row missing primary field: {primary_field}")
        if key in index:
            would_update += 1
        else:
            would_create += 1

    created = 0
    updated = 0
    if args.apply:
        for row in rows:
            key = str(row.get(primary_field) or "").strip()
            existing = index.get(key)
            if existing:
                client.update_record(table_id, str(existing["record_id"]), row)
                updated += 1
            else:
                client.create_record(table_id, row)
                created += 1

    write_json_stdout(
        {
            "ok": True,
            "mode": "apply" if args.apply else "dry-run",
            "status": "applied" if args.apply else "preview_ready",
            "apply": bool(args.apply),
            "account_id": account_id,
            "base_token": base_token,
            "table_id": table_id,
            "primary_field": primary_field,
            "row_count": len(rows),
            "preview": {"would_create": would_create, "would_update": would_update},
            "result": {"created": created, "updated": updated},
            "ensure_table": ensured,
        }
    )
    return 0


def command_sync_base_schema(args: argparse.Namespace) -> int:
    manifest = read_json(Path(args.manifest))
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    account_id = str(args.account_id or os.getenv("FEISHU_BITABLE_BRIDGE_ACCOUNT_ID") or DEFAULT_ACCOUNT_ID)
    link_meta = parse_link(args.link)
    creds = load_feishu_account(account_id)
    base_token = resolve_base_token(
        args.link,
        app_id=creds["app_id"],
        app_secret=creds["app_secret"],
        table_id=link_meta["table_id"] or None,
    )
    client = FeishuBitableClient(creds["app_id"], creds["app_secret"], base_token)

    tables_payload: list[dict[str, Any]] = []
    for table_spec in manifest.get("tables") or []:
        if not isinstance(table_spec, dict):
            continue
        ensured = ensure_table(
            client,
            table_name=str(table_spec.get("table_name") or ""),
            primary_field=str(table_spec.get("primary_field") or ""),
            field_names=[str(item) for item in (table_spec.get("fields") or [])],
            apply=bool(args.apply),
        )
        tables_payload.append(
            {
                "table_name": str(table_spec.get("table_name") or ""),
                "table_id": ensured.get("table_id") or "",
                "primary_field": str(table_spec.get("primary_field") or ""),
                "fields": [str(item) for item in (table_spec.get("fields") or [])],
                "views": [str(item) for item in (table_spec.get("views") or [])],
                "created": bool(ensured.get("created")),
                "existed": bool(ensured.get("existed")),
                "missing_fields": ensured.get("missing_fields") or [],
            }
        )

    write_json_stdout(
        {
            "ok": True,
            "mode": "apply" if args.apply else "dry-run",
            "status": "schema_applied" if args.apply else "schema_preview_ready",
            "account_id": account_id,
            "base_token": base_token,
            "base_name": str(manifest.get("base_name") or ""),
            "tables": tables_payload,
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Minimal Feishu Bitable bridge for AI大管家.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upsert = subparsers.add_parser("upsert-records")
    upsert.add_argument("--link", required=True)
    upsert.add_argument("--table-id")
    upsert.add_argument("--table-name")
    upsert.add_argument("--primary-field", required=True)
    upsert.add_argument("--payload-file", required=True)
    upsert.add_argument("--account-id")
    mode = upsert.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    upsert.set_defaults(func=command_upsert_records)

    schema = subparsers.add_parser("sync-base-schema")
    schema.add_argument("--link", required=True)
    schema.add_argument("--manifest", required=True)
    schema.add_argument("--account-id")
    schema_mode = schema.add_mutually_exclusive_group(required=True)
    schema_mode.add_argument("--dry-run", action="store_true")
    schema_mode.add_argument("--apply", action="store_true")
    schema.set_defaults(func=command_sync_base_schema)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:
        write_json_stdout(
            {
                "ok": False,
                "command": args.command,
                "error": str(exc),
            }
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
