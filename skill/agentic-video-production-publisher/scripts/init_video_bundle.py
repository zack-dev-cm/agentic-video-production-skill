#!/usr/bin/env python3
"""Create an AI video production bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def require_text(value: str, label: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise SystemExit(f"{label} must not be empty")
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Output JSON bundle.")
    parser.add_argument("--title", required=True, help="Project title.")
    parser.add_argument("--owner", default="", help="Project owner or publisher handle.")
    parser.add_argument("--format", default="music_video", help="Project format label.")
    parser.add_argument("--aspect-ratio", default="", help="Target aspect ratio, such as 16:9 or 9:16.")
    parser.add_argument("--runtime", type=float, default=0.0, help="Target final runtime in seconds.")
    parser.add_argument("--platform", action="append", default=[], help="Repeatable target platform.")
    parser.add_argument("--track-title", default="", help="Music track title.")
    parser.add_argument("--track-provider", default="", help="Music provider, such as Suno or local.")
    parser.add_argument("--track-source", default="", help="Track source URL or local ID.")
    parser.add_argument("--bpm", type=float, default=0.0, help="Track BPM.")
    parser.add_argument("--key", default="", help="Track musical key.")
    parser.add_argument("--rights-note", default="", help="Music rights or attribution note.")
    parser.add_argument("--youtube-channel", default="", help="Planned YouTube channel name.")
    parser.add_argument("--openclaw-profile", default="", help="Planned OpenClaw browser profile.")
    parser.add_argument("--final-video", default="", help="Planned or actual final export path.")
    args = parser.parse_args()

    platforms = args.platform or ["youtube"]
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "project": {
            "title": require_text(args.title, "title"),
            "owner": args.owner.strip(),
            "format": args.format.strip() or "music_video",
            "aspect_ratio": args.aspect_ratio.strip(),
            "target_runtime_seconds": args.runtime,
            "target_platforms": platforms,
            "logline": "",
        },
        "characters": [],
        "music": {
            "provider": args.track_provider.strip(),
            "track_title": args.track_title.strip(),
            "source": args.track_source.strip(),
            "bpm": args.bpm,
            "key": args.key.strip(),
            "rights_note": args.rights_note.strip(),
            "beat_map": [],
        },
        "worlds": [],
        "shots": [],
        "assets": {
            "reference_assets": [],
            "generated_assets": [],
            "thumbnail_file": "",
            "description_file": "",
            "final_video": args.final_video.strip(),
        },
        "publish": {
            "youtube": {
                "channel_name": args.youtube_channel.strip(),
                "browser_profile": args.openclaw_profile.strip(),
                "title": "",
                "description_file": "",
                "privacy": "unlisted",
                "audience": "unspecified",
                "tags": [],
                "playlists": [],
                "published_video_url": "",
                "studio_url": "",
            },
            "tiktok": {
                "browser_profile": args.openclaw_profile.strip(),
                "caption": "",
                "hashtags": [],
                "published_video_url": "",
            },
            "provenance": [],
        },
        "qc": {
            "status": "planned",
            "findings": [],
            "operator_decisions": [],
        },
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
