#!/usr/bin/env python3
"""Export a TikTok OpenClaw handoff bundle from an AI video production bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def choose(*values: Any) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def require(value: str, label: str) -> str:
    if not value.strip():
        raise SystemExit(f"{label} is required")
    return value.strip()


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def portable_path(path: Path, base_dir: Path) -> str:
    resolved = path.expanduser().resolve()
    candidates = [base_dir.expanduser().resolve(), Path.cwd().resolve()]
    for candidate in candidates:
        try:
            return str(resolved.relative_to(candidate))
        except ValueError:
            continue
    return resolved.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="Production bundle JSON.")
    parser.add_argument("--out", required=True, help="Output TikTok handoff JSON.")
    parser.add_argument("--browser-profile", default="", help="OpenClaw browser profile.")
    parser.add_argument("--video-file", default="", help="Final video file.")
    parser.add_argument("--caption", default="", help="TikTok caption.")
    parser.add_argument("--hashtag", action="append", default=[], help="Repeatable hashtag without or with #.")
    args = parser.parse_args()

    source_path = Path(args.bundle).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    source_label = portable_path(source_path, out_path.parent)
    source = load_json(source_path)
    assets = source.get("assets") or {}
    publish = source.get("publish") or {}
    tiktok = publish.get("tiktok") or {}
    music = source.get("music") or {}

    browser_profile = require(choose(args.browser_profile, tiktok.get("browser_profile")), "browser profile")
    video_file = require(choose(args.video_file, assets.get("final_video")), "video file")
    caption = choose(args.caption, tiktok.get("caption"))
    hashtags = dedupe(
        [str(item) for item in (tiktok.get("hashtags") or [])]
        + [tag if tag.startswith("#") else f"#{tag}" for tag in args.hashtag]
    )

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "platform": "tiktok",
        "source_production_bundle": source_label,
        "run": {
            "browser_profile": browser_profile,
            "operator_mode": "supervised",
            "goal": "Publish final AI video export to TikTok through OpenClaw.",
        },
        "content": {
            "caption": caption,
            "hashtags": hashtags,
        },
        "assets": {
            "video_file": video_file,
            "extra_files": [source_label],
        },
        "provenance": {
            "music_provider": str(music.get("provider") or "").strip(),
            "music_source": str(music.get("source") or "").strip(),
            "music_rights": str(music.get("rights_note") or "").strip(),
            "production_provenance": publish.get("provenance") or [],
        },
        "verification": {
            "status": "planned",
            "planned_checks": [
                "confirm the named OpenClaw browser profile is logged into the intended TikTok account",
                "confirm final export path, caption, hashtags, and attribution requirements",
                "pause for CAPTCHA, 2FA, passkey, or email verification",
                "capture upload and final post evidence",
                "record final TikTok post URL",
            ],
        },
        "artifacts": {
            "published_video_url": choose(tiktok.get("published_video_url")),
            "evidence_files": [],
        },
        "steps": [],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
