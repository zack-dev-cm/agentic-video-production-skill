#!/usr/bin/env python3
"""Validate an AI video production bundle for consistency and publish readiness."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PRIVATE_PATH_RE = re.compile(r"^(?:/Users/|/home/|[A-Za-z]:\\\\Users\\\\)")
NON_DIEGETIC_RE = re.compile(r"\b(soundtrack|score|music plays|song plays|lyrics|chorus swells)\b", re.IGNORECASE)
BRAND_RE = re.compile(r"\b(Nike|Adidas|Timberland|Apple|iPhone|Coca-Cola|Marvel|Disney|Star Wars)\b", re.IGNORECASE)


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"expected JSON object in {path}")
    return payload


def add_issue(bucket: list[dict[str, str]], kind: str, message: str) -> None:
    bucket.append({"kind": kind, "message": message})


def number_value(
    value: Any,
    label: str,
    errors: list[dict[str, str]],
    warnings: list[dict[str, str]],
    *,
    required: bool,
) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        bucket = errors if required else warnings
        add_issue(bucket, label, f"{label} must be numeric; got {value!r}.")
        return 0.0


def exists_for_path(value: str, repo_root: Path) -> bool:
    if not value or re.match(r"^https?://", value):
        return True
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate.exists()
    return (repo_root / candidate).exists()


def read_prompt(shot: dict[str, Any], repo_root: Path) -> str:
    inline = str(shot.get("prompt") or "")
    prompt_file = str(shot.get("prompt_file") or "").strip()
    if prompt_file:
        candidate = Path(prompt_file).expanduser()
        if not candidate.is_absolute():
            candidate = repo_root / candidate
        if candidate.exists():
            return inline + "\n" + candidate.read_text(encoding="utf-8", errors="replace")
    return inline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", required=True, help="Production bundle JSON.")
    parser.add_argument("--repo-root", default=".", help="Root for relative path checks.")
    parser.add_argument("--out", required=True, help="Output JSON report.")
    args = parser.parse_args()

    bundle_path = Path(args.bundle).expanduser().resolve()
    repo_root = Path(args.repo_root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_json(bundle_path)
    project = payload.get("project") or {}
    characters = payload.get("characters") or []
    music = payload.get("music") or {}
    shots = payload.get("shots") or []
    assets = payload.get("assets") or {}
    publish = payload.get("publish") or {}

    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    if not str(project.get("title") or "").strip():
        add_issue(errors, "project.title", "Project title is required.")
    target_runtime = number_value(
        project.get("target_runtime_seconds"),
        "project.target_runtime_seconds",
        errors,
        warnings,
        required=False,
    )
    if target_runtime <= 0:
        add_issue(warnings, "project.runtime", "Target runtime is not set.")
    if not str(project.get("aspect_ratio") or "").strip():
        add_issue(warnings, "project.aspect_ratio", "Target aspect ratio is not set.")

    character_slugs: set[str] = set()
    if not isinstance(characters, list):
        add_issue(errors, "characters", "characters must be a list.")
        characters = []
    for character in characters:
        if not isinstance(character, dict):
            add_issue(errors, "characters", "Each character must be an object.")
            continue
        slug = str(character.get("slug") or "").strip()
        if not slug:
            add_issue(errors, "characters.slug", "Each character needs a slug.")
        else:
            character_slugs.add(slug)
        if not str(character.get("visual_markers") or "").strip():
            add_issue(warnings, f"character.{slug or '?'}", "visual_markers is missing.")
        if not str(character.get("identity_lock") or "").strip():
            add_issue(warnings, f"character.{slug or '?'}", "identity_lock is missing.")
        refs = character.get("reference_assets") or []
        if not refs:
            add_issue(warnings, f"character.{slug or '?'}", "No reference assets recorded.")
        for ref in refs:
            ref_text = str(ref).strip()
            if PRIVATE_PATH_RE.match(ref_text):
                add_issue(warnings, "private_path", f"Character reference uses a private absolute path: {ref_text}")
            if not exists_for_path(ref_text, repo_root):
                add_issue(warnings, "missing_reference", f"Character reference does not exist locally: {ref_text}")

    if str(music.get("provider") or "").strip() or str(music.get("track_title") or "").strip() or str(music.get("source") or "").strip():
        if not str(music.get("rights_note") or "").strip():
            add_issue(errors, "music.rights_note", "Music is configured but rights_note is missing.")
        if not music.get("beat_map"):
            add_issue(warnings, "music.beat_map", "Music beat_map is empty; edit timing may drift.")

    if not isinstance(shots, list):
        add_issue(errors, "shots", "shots must be a list.")
        shots = []
    if not shots:
        add_issue(warnings, "shots", "No shots have been added.")

    total_shot_runtime = 0.0
    for shot in shots:
        if not isinstance(shot, dict):
            add_issue(errors, "shots", "Each shot must be an object.")
            continue
        shot_id = str(shot.get("shot_id") or "?").strip()
        runtime = number_value(
            shot.get("runtime_seconds"),
            f"shot.{shot_id}.runtime_seconds",
            errors,
            warnings,
            required=True,
        )
        total_shot_runtime += max(runtime, 0.0)
        if runtime <= 0:
            add_issue(errors, f"shot.{shot_id}", "runtime_seconds must be greater than 0.")
        if not str(shot.get("mode") or "").strip():
            add_issue(errors, f"shot.{shot_id}", "mode is required.")
        prompt_file = str(shot.get("prompt_file") or "").strip()
        if prompt_file:
            if PRIVATE_PATH_RE.match(prompt_file):
                add_issue(warnings, "private_path", f"Shot prompt file uses a private absolute path: {prompt_file}")
            if not exists_for_path(prompt_file, repo_root):
                add_issue(warnings, f"shot.{shot_id}", f"prompt_file does not exist locally: {prompt_file}")
        elif not str(shot.get("prompt") or "").strip():
            add_issue(warnings, f"shot.{shot_id}", "No prompt or prompt_file recorded.")
        for ref in shot.get("references") or []:
            ref_text = str(ref).strip()
            if PRIVATE_PATH_RE.match(ref_text):
                add_issue(warnings, "private_path", f"Shot reference uses a private absolute path: {ref_text}")
            if not exists_for_path(ref_text, repo_root):
                add_issue(warnings, f"shot.{shot_id}", f"reference does not exist locally: {ref_text}")
        shot_characters = [str(item).strip() for item in shot.get("characters") or [] if str(item).strip()]
        if shot_characters and not character_slugs:
            add_issue(
                warnings,
                f"shot.{shot_id}",
                "Shot lists characters but no character bible exists in bundle.characters.",
            )
        for character_slug in shot_characters:
            if character_slugs and character_slug not in character_slugs:
                add_issue(warnings, f"shot.{shot_id}", f"Unknown character slug: {character_slug}")
        prompt_text = read_prompt(shot, repo_root)
        if NON_DIEGETIC_RE.search(prompt_text):
            add_issue(warnings, f"shot.{shot_id}", "Prompt may include non-diegetic music language.")
        if BRAND_RE.search(prompt_text):
            add_issue(warnings, f"shot.{shot_id}", "Prompt may include real brand or protected IP names.")
        for character in characters:
            if not isinstance(character, dict):
                continue
            display_name = str(character.get("display_name") or "").strip()
            if display_name and re.search(rf"\b{re.escape(display_name)}\b", prompt_text):
                add_issue(warnings, f"shot.{shot_id}", f"Prompt uses display name '{display_name}' instead of visual markers.")

    if target_runtime and total_shot_runtime and abs(total_shot_runtime - target_runtime) > max(3.0, target_runtime * 0.15):
        add_issue(warnings, "runtime", f"Shot runtime total {total_shot_runtime:.1f}s differs from target {target_runtime:.1f}s.")

    final_video = str(assets.get("final_video") or "").strip()
    youtube = publish.get("youtube") or {}
    tiktok = publish.get("tiktok") or {}
    publish_requested = bool(str(youtube.get("channel_name") or "").strip() or str(youtube.get("browser_profile") or "").strip())
    tiktok_requested = bool(
        str(tiktok.get("browser_profile") or "").strip()
        or str(tiktok.get("caption") or "").strip()
        or tiktok.get("hashtags")
    )
    if publish_requested or tiktok_requested:
        if not final_video:
            add_issue(errors, "assets.final_video", "Publish handoff is configured but final_video is missing.")
        elif not exists_for_path(final_video, repo_root):
            add_issue(errors, "assets.final_video", f"final_video does not exist locally: {final_video}")
    if publish_requested:
        if not str(youtube.get("channel_name") or "").strip():
            add_issue(errors, "publish.youtube.channel_name", "YouTube channel name is required for publish handoff.")
        if not str(youtube.get("browser_profile") or "").strip():
            add_issue(errors, "publish.youtube.browser_profile", "OpenClaw browser profile is required for publish handoff.")
    if tiktok_requested and not str(tiktok.get("browser_profile") or "").strip():
        add_issue(errors, "publish.tiktok.browser_profile", "OpenClaw browser profile is required for TikTok handoff.")

    status = "PASS" if not errors and not warnings else "REVIEW" if not errors else "BLOCK"
    report = {
        "schema_version": "1.0",
        "bundle_path": str(bundle_path),
        "repo_root": str(repo_root),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "characters": len(characters),
            "shots": len(shots),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "runtime": {
            "target_seconds": target_runtime,
            "shot_total_seconds": round(total_shot_runtime, 3),
        },
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
