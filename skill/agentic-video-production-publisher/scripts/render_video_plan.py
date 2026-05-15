#!/usr/bin/env python3
"""Render a markdown production plan from an AI video production bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def line(label: str, value: Any) -> str:
    text = str(value or "").strip()
    return f"- {label}: `{text}`" if text else f"- {label}:"


def render_list(values: list[Any]) -> str:
    clean = [str(value).strip() for value in values if str(value).strip()]
    return ", ".join(f"`{value}`" for value in clean) if clean else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="Production bundle JSON.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    args = parser.parse_args()

    payload = load_json(Path(args.bundle).expanduser().resolve())
    project = payload.get("project") or {}
    music = payload.get("music") or {}
    assets = payload.get("assets") or {}
    publish = payload.get("publish") or {}

    title = str(project.get("title") or "AI Video Production").strip()
    lines = [f"# {title}", ""]

    lines.extend(
        [
            "## Project",
            line("owner", project.get("owner")),
            line("format", project.get("format")),
            line("aspect ratio", project.get("aspect_ratio")),
            line("target runtime seconds", project.get("target_runtime_seconds")),
            f"- target platforms: {render_list(project.get('target_platforms') or [])}",
        ]
    )
    if str(project.get("logline") or "").strip():
        lines.append(f"- logline: {str(project.get('logline')).strip()}")

    lines.extend(["", "## Characters"])
    characters = payload.get("characters") or []
    if characters:
        for character in characters:
            if not isinstance(character, dict):
                continue
            slug = str(character.get("slug") or "").strip()
            lines.append(f"- `{slug}`: {str(character.get('visual_markers') or '').strip()}")
            refs = character.get("reference_assets") or []
            if refs:
                lines.append(f"- `{slug}` refs: {render_list(refs)}")
            drift = character.get("forbidden_drift") or []
            if drift:
                lines.append(f"- `{slug}` forbidden drift: {render_list(drift)}")
    else:
        lines.append("- No recurring characters recorded.")

    lines.extend(
        [
            "",
            "## Music",
            line("provider", music.get("provider")),
            line("track", music.get("track_title")),
            line("source", music.get("source")),
            line("BPM", music.get("bpm")),
            line("key", music.get("key")),
            line("rights", music.get("rights_note")),
        ]
    )
    beat_map = music.get("beat_map") or []
    if beat_map:
        lines.append("")
        lines.append("### Beat Map")
        for beat in beat_map:
            if isinstance(beat, dict):
                lines.append(
                    f"- `{beat.get('timecode', '')}` {beat.get('section', '')}: {beat.get('edit_intent', '')}"
                )

    lines.extend(["", "## Worlds"])
    worlds = payload.get("worlds") or []
    if worlds:
        for world in worlds:
            if isinstance(world, dict):
                lines.append(f"- `{world.get('slug', world.get('name', ''))}`: {world.get('description', '')}")
    else:
        lines.append("- No worlds recorded.")

    lines.extend(["", "## Shot Ledger"])
    shots = payload.get("shots") or []
    if shots:
        lines.append("| Shot | World | Mode | Runtime | Status | Characters | Asset |")
        lines.append("|---|---|---|---:|---|---|---|")
        for shot in shots:
            if not isinstance(shot, dict):
                continue
            characters_text = ", ".join(str(item) for item in shot.get("characters") or [])
            lines.append(
                "| {shot_id} | {world} | {mode} | {runtime} | {status} | {characters} | {asset} |".format(
                    shot_id=shot.get("shot_id", ""),
                    world=shot.get("world", ""),
                    mode=shot.get("mode", ""),
                    runtime=shot.get("runtime_seconds", ""),
                    status=shot.get("status", ""),
                    characters=characters_text,
                    asset=shot.get("selected_asset", ""),
                )
            )
    else:
        lines.append("- No shots recorded.")

    lines.extend(
        [
            "",
            "## Assets",
            line("final video", assets.get("final_video")),
            line("thumbnail", assets.get("thumbnail_file")),
            line("description", assets.get("description_file")),
        ]
    )

    youtube = publish.get("youtube") or {}
    lines.extend(
        [
            "",
            "## YouTube Handoff",
            line("channel", youtube.get("channel_name")),
            line("browser profile", youtube.get("browser_profile")),
            line("privacy", youtube.get("privacy")),
            line("audience", youtube.get("audience")),
            line("published URL", youtube.get("published_video_url")),
            line("Studio URL", youtube.get("studio_url")),
        ]
    )

    qc = payload.get("qc") or {}
    lines.extend(["", "## QC", line("status", qc.get("status"))])
    for finding in qc.get("findings") or []:
        lines.append(f"- finding: {finding}")
    for decision in qc.get("operator_decisions") or []:
        lines.append(f"- decision: {decision}")

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
