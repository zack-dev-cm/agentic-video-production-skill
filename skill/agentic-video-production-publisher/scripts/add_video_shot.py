#!/usr/bin/env python3
"""Append or replace one shot in an AI video production bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_MODES = {"narrative", "studio", "action", "performance", "atmospheric", "mixed"}
ALLOWED_STATUS = {"planned", "prompted", "generated", "selected", "rejected", "edited", "replaced"}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def nonempty(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(f"{label} must not be empty")
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="Production bundle JSON.")
    parser.add_argument("--shot-id", required=True, help="Stable shot ID, such as S001.")
    parser.add_argument("--world", default="", help="World or sequence label.")
    parser.add_argument("--mode", default="narrative", choices=sorted(ALLOWED_MODES), help="Cinema mode.")
    parser.add_argument("--runtime", type=float, default=0.0, help="Shot runtime in seconds.")
    parser.add_argument("--intent", default="", help="One-line shot intention.")
    parser.add_argument("--characters", default="", help="Comma-separated character visual marker slugs.")
    parser.add_argument("--references", default="", help="Comma-separated reference asset paths or IDs.")
    parser.add_argument("--prompt-file", default="", help="Path to exact generation prompt.")
    parser.add_argument("--prompt", default="", help="Inline prompt text. Prefer prompt-file for long prompts.")
    parser.add_argument("--provider", default="", help="Generation provider or editor.")
    parser.add_argument("--status", default="planned", choices=sorted(ALLOWED_STATUS), help="Shot status.")
    parser.add_argument("--selected-asset", default="", help="Selected render path or URL.")
    parser.add_argument("--note", action="append", default=[], help="Repeatable note.")
    parser.add_argument("--replace", action="store_true", help="Replace existing shot with same ID.")
    args = parser.parse_args()

    bundle_path = Path(args.bundle).expanduser().resolve()
    payload = load_json(bundle_path)
    shots = payload.setdefault("shots", [])
    if not isinstance(shots, list):
        raise SystemExit("bundle.shots must be a list")

    shot_id = nonempty(args.shot_id, "shot-id")
    existing_index = next((idx for idx, item in enumerate(shots) if isinstance(item, dict) and item.get("shot_id") == shot_id), None)
    if existing_index is not None and not args.replace:
        raise SystemExit(f"shot {shot_id} already exists; pass --replace to update it")

    shot = {
        "shot_id": shot_id,
        "world": args.world.strip(),
        "mode": args.mode,
        "runtime_seconds": args.runtime,
        "intent": args.intent.strip(),
        "characters": split_csv(args.characters),
        "references": split_csv(args.references),
        "prompt_file": args.prompt_file.strip(),
        "prompt": args.prompt.strip(),
        "provider": args.provider.strip(),
        "status": args.status,
        "selected_asset": args.selected_asset.strip(),
        "rejected_assets": [],
        "notes": [item.strip() for item in args.note if item.strip()],
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }

    if existing_index is None:
        shots.append(shot)
    else:
        shots[existing_index] = shot

    bundle_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(bundle_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
