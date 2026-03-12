#!/usr/bin/env python3
"""Update a content-race round stage and recompute top-level round state."""

from __future__ import annotations

import argparse
from pathlib import Path

from content_race_common import (
    compute_round_top_status,
    dump_json,
    load_round_status,
    now_iso,
    refresh_completion_checks,
)
from update_supervision_status import render_supervision_artifacts


VALID_STAGES = {"knowledge_digest", "xhs_collection", "workflow_submissions", "weekly_scorecard"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--round-dir", required=True, type=Path)
    parser.add_argument("--stage", required=True, choices=sorted(VALID_STAGES))
    parser.add_argument("--status", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--artifact", default="")
    parser.add_argument("--next-action", action="append", default=[])
    parser.add_argument("--closure-state", default="")
    args = parser.parse_args()

    round_dir = args.round_dir.resolve()
    payload = load_round_status(round_dir)
    payload["generated_at"] = now_iso()
    payload.setdefault("blocked_stages", {})
    payload["blocked_stages"][args.stage] = {
        "status": args.status,
        "reason": args.reason,
    }
    if args.artifact:
        payload["blocked_stages"][args.stage]["artifact"] = args.artifact
    if args.closure_state:
        payload["closure_state"] = args.closure_state
    if args.next_action:
        payload["next_actions"] = args.next_action

    payload["status"] = compute_round_top_status(payload)
    refresh_completion_checks(payload)
    dump_json(round_dir / "round_status.json", payload)
    render_supervision_artifacts(round_dir)
    print(round_dir / "round_status.json")


if __name__ == "__main__":
    main()
