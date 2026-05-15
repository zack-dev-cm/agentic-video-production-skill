#!/usr/bin/env python3
"""Export a YouTube OpenClaw creator bundle from an AI video production bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_PRIVACY = {"private", "unlisted", "public"}
ALLOWED_AUDIENCE = {"made_for_kids", "not_made_for_kids", "unspecified"}


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


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
    parser.add_argument("--out", required=True, help="Output YouTube creator bundle JSON.")
    parser.add_argument("--channel-name", default="", help="YouTube channel name.")
    parser.add_argument("--browser-profile", default="", help="OpenClaw browser profile.")
    parser.add_argument("--video-title", default="", help="YouTube title.")
    parser.add_argument("--video-file", default="", help="Final video file.")
    parser.add_argument("--description-file", default="", help="Description file.")
    parser.add_argument("--thumbnail-file", default="", help="Thumbnail file.")
    parser.add_argument("--privacy", default="", choices=sorted(ALLOWED_PRIVACY | {""}), help="Privacy.")
    parser.add_argument("--audience", default="", choices=sorted(ALLOWED_AUDIENCE | {""}), help="Audience.")
    parser.add_argument("--tag", action="append", default=[], help="Repeatable YouTube tag.")
    parser.add_argument("--playlist", action="append", default=[], help="Repeatable playlist.")
    args = parser.parse_args()

    source_path = Path(args.bundle).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    source_label = portable_path(source_path, out_path.parent)
    source = load_json(source_path)
    project = source.get("project") or {}
    assets = source.get("assets") or {}
    publish = source.get("publish") or {}
    youtube = publish.get("youtube") or {}
    music = source.get("music") or {}

    title = require(choose(args.video_title, youtube.get("title"), project.get("title")), "video title")
    channel = require(choose(args.channel_name, youtube.get("channel_name")), "channel name")
    browser_profile = require(choose(args.browser_profile, youtube.get("browser_profile")), "browser profile")
    video_file = require(choose(args.video_file, assets.get("final_video")), "video file")
    privacy = choose(args.privacy, youtube.get("privacy"), "unlisted")
    audience = choose(args.audience, youtube.get("audience"), "unspecified")

    tags = dedupe([str(item) for item in (youtube.get("tags") or [])] + args.tag)
    playlists = dedupe([str(item) for item in (youtube.get("playlists") or [])] + args.playlist)
    notes = [
        f"Source production bundle: {source_label}",
        f"Music provider: {music.get('provider', '')}",
        f"Music source: {music.get('source', '')}",
        f"Music rights: {music.get('rights_note', '')}",
    ]

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "run": {
            "channel_name": channel,
            "goal": "Publish final AI video export from production bundle.",
            "browser_profile": browser_profile,
            "operator_mode": "supervised",
            "notes": [note for note in notes if not note.endswith(": ")],
        },
        "content": {
            "title": title,
            "privacy": privacy,
            "audience": audience,
            "category": "",
            "language": "en",
            "publish_at": "",
            "tags": tags,
            "playlists": playlists,
        },
        "assets": {
            "video_file": video_file,
            "description_file": choose(args.description_file, youtube.get("description_file"), assets.get("description_file")),
            "thumbnail_file": choose(args.thumbnail_file, assets.get("thumbnail_file")),
            "extra_files": [source_label],
        },
        "artifacts": {
            "youtube_studio_url": choose(youtube.get("studio_url")),
            "published_video_url": choose(youtube.get("published_video_url")),
            "evidence_files": [],
        },
        "verification": {
            "status": "planned",
            "processing_state": "not_started",
            "planned_checks": [
                "confirm the named OpenClaw browser profile is logged into the intended YouTube account",
                "confirm final export path, title, description, thumbnail, privacy, and audience values",
                "pause for CAPTCHA, 2FA, passkey, or email verification",
                "capture Studio confirmation evidence after publish or schedule",
                "record final public or scheduled video URL",
            ],
        },
        "steps": [],
    }

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
