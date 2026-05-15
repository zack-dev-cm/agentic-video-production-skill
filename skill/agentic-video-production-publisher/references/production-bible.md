# Production Bible

Use this reference when the default scripts are not enough and the bundle needs to be edited by hand.

## Bundle Shape

Core fields:

- `project`: title, owner, format, aspect ratio, runtime, target platforms
- `characters`: identity lock, visual markers, reference assets, styling variants, drift risks
- `music`: provider, track title, source URL or ID, BPM, key, rights note, beat map
- `worlds`: location or set, visual rules, palette, lens/camera mode, scene plates
- `shots`: one entry per generation attempt or final edit shot
- `assets`: references, generated assets, final video, thumbnails, description files
- `publish`: YouTube/TikTok metadata, browser profile, provenance, final URLs
- `qc`: validation findings and operator decisions

## Character Lock Fields

Recommended character object:

```json
{
  "slug": "rose-pink-braids",
  "display_name": "Sol",
  "visual_markers": "rose-pink braided hair, warm fair skin, sharp almond eyes, athletic build",
  "identity_lock": "Face, build, hair color, skin tone, and distinguishing markers that must survive every shot.",
  "reference_assets": ["refs/sol-base.png", "refs/sol-sheet.png"],
  "styling_layers": ["white stadium tank and light cargo pants"],
  "forbidden_drift": ["hair color changes", "face shape changes", "brand logos"]
}
```

Prompt outputs should use `visual_markers`, not `display_name`.

## Music Beat Map Fields

Recommended beat object:

```json
{
  "timecode": "00:31.500",
  "section": "drop",
  "musical_event": "kick and hook enter",
  "edit_intent": "cut from narrative plate to dance break",
  "shot_ids": ["S014", "S015"]
}
```

Keep lyrics out unless the operator owns them and the final platform metadata requires them.

## Shot Object

Recommended shot object:

```json
{
  "shot_id": "S001",
  "world": "stadium",
  "mode": "performance",
  "runtime_seconds": 6.0,
  "characters": ["rose-pink-braids", "platinum-bob"],
  "references": ["refs/stadium-plate.png", "refs/group-sheet.png"],
  "prompt_file": "prompts/S001.txt",
  "prompt": "",
  "provider": "Seedance",
  "status": "prompted",
  "selected_asset": "",
  "rejected_assets": [],
  "notes": "Use crowd and stage noise only in generation prompt."
}
```

## Mode Guide

- `narrative`: lived-in dramatic scene, handheld realism
- `studio`: white seamless, editorial set, clean controlled lighting
- `action`: chase, combat, stunts, smoke, debris, reactive camera
- `performance`: stage, concert, dance, crowd, jumbotron, hard cuts
- `atmospheric`: no-human environment plates, weather, abandoned spaces, mood

## Prompt Hygiene

Before a prompt is approved:

- remove real brand names and protected IP unless the user explicitly owns the rights
- replace character names with visual descriptors
- remove non-diegetic music instructions from scene audio
- ensure the uploaded reference list matches the prompt
- state runtime and shot count clearly
- keep text and signage generic unless readable text is required and approved

## Public Release Hygiene

Before GitHub or ClawHub publication:

- strip private absolute paths from examples
- avoid bundling generated media unless licensed for public redistribution
- avoid copying downloaded third-party skill bodies into the repo
- include only workflow instructions, scripts, references, and small synthetic examples
