---
name: agentic-video-production-publisher
description: End-to-end agentic AI video production and publishing workflow for consistent characters, music-video beat maps, complex multi-world scenes, generated-asset provenance, and OpenClaw YouTube/TikTok handoff. Use when users ask to create, adapt, coordinate, package, or publish AI videos or music videos using Claude, Codex, OpenClaw, Higgsfield, Seedance, Nano Banana, Soul Cinema, Suno, GitHub, or ClawHub skills.
license: MIT-0
metadata: {"openclaw":{"skillKey":"agentic-video-production-publisher","requires":{"anyBins":["python3","python"]},"relatedSkills":["openclaw-youtube-tiktok-publisher","youtube-openclaw-creator"]}}
---

# Agentic Video Production Publisher

## Goal

Run a full AI video production from idea to published video without losing character identity, music timing, asset provenance, or final publishing evidence.

This skill is an original public workflow inspired by common high-quality video-generation practice: separate identity from styling, still-image references from motion prompts, music timing from diegetic scene audio, and generation experiments from final publish evidence.

## Non-Negotiables

- Keep character identity and styling as separate layers. Identity comes from locked visual markers and reference assets; wardrobe, hair styling, props, and scene lighting are per-shot layers.
- Write video prompts with visual descriptors, not character names. Names are allowed in the production bundle for humans, but generation prompts should use visual markers.
- Keep generated-video prompt audio diegetic unless the target tool explicitly needs a music cue. Music belongs in the edit map and final soundtrack provenance, not inside Seedance-style scene audio.
- Keep every generated asset traceable: provider, model/tool, prompt file, source refs, selected take, rejected takes when known, license or rights note, and final export path.
- Use OpenClaw only for logged-in browser publishing. Pause for CAPTCHA, 2FA, account checks, or final irreversible publish confirmation.
- Do not publish copied third-party skill text or provider prompts unless the user owns it or provides explicit license/permission. Publish clean workflow instructions and local manifests instead.

## Quick Start

1. Create a production bundle.

```bash
python3 {baseDir}/scripts/init_video_bundle.py --out runs/video-bundle.json --title "Project title" --owner "zack-dev-cm"
```

2. Build the production bible in the bundle:
   - characters: identity lock, visual markers, reference assets, approved wardrobe layers
   - music: provider, track ID or URL, BPM, key, rights note, beat map
   - worlds: scene plates, lighting rules, palette, camera mode
   - shots: shot ID, runtime, characters, references, prompt file, selected render

3. Add shots as prompts are approved.

```bash
python3 {baseDir}/scripts/add_video_shot.py --bundle runs/video-bundle.json --shot-id S001 --world stadium --mode performance --runtime 6 --intent "wide opening crowd hit" --characters "rose-pink-braids,platinum-bob" --prompt-file prompts/S001-seedance.txt
```

4. Check the bundle before final edit or publish.

```bash
python3 {baseDir}/scripts/check_video_bundle.py --bundle runs/video-bundle.json --repo-root . --out reports/video-qc.json
```

5. Render a readable production plan.

```bash
python3 {baseDir}/scripts/render_video_plan.py --bundle runs/video-bundle.json --out reports/video-plan.md
```

6. Export a YouTube publisher handoff after the final edit exists.

```bash
python3 {baseDir}/scripts/export_youtube_handoff.py --bundle runs/video-bundle.json --out runs/youtube-openclaw-bundle.json --channel-name "Channel" --browser-profile "youtube-profile" --video-title "Final title" --video-file exports/final.mp4
```

For TikTok:

```bash
python3 {baseDir}/scripts/export_tiktok_handoff.py --bundle runs/video-bundle.json --out runs/tiktok-openclaw-bundle.json --browser-profile "tiktok-profile" --video-file exports/final.mp4 --caption "Caption" --hashtag aivideo
```

Then use `openclaw-youtube-tiktok-publisher` or `youtube-openclaw-creator` to upload through the logged-in OpenClaw browser profile.

## Workflow

### 1. Intake

Ask for only missing production-critical inputs:

- target format: short vertical, landscape video, music video, teaser, ad, narrative short
- target platforms: YouTube, TikTok, Shorts, Reels, internal review
- final runtime and aspect ratio
- music source and usage rights
- whether recurring characters already have reference images
- preferred generation stack, if any

When the user provides raw Claude skills, prompt notes, or downloaded examples, review them for reusable workflow rules. Do not copy long prompt blocks into a public skill or repo.

### 2. Character Lock

Create a character bible before shot prompts:

- human-facing name or slug
- visual marker phrase for prompts
- face and body lock: bone structure, skin tone, hair color/texture, body proportions, distinguishing markers
- reference assets: base identity, 6-panel sheet, close-up face, body reference
- allowed variants: wardrobe, hairstyle, makeup, accessories
- forbidden drift: face changes, hair color swaps, logo/text artifacts, age-language, brand names

If no reference exists, create still-image prompts in this order:

1. single full-body outfit reference on white seamless
2. 6-panel multi-angle character sheet
3. environment or character-in-environment scene plate
4. motion shot prompt using those references

### 3. Music Map

Treat music as an edit spine:

- record provider and source: Suno, Udio, local audio, licensed track, original composition
- record rights note and attribution requirement
- capture BPM, key, sections, bars, timestamps, drops, vocal entries, and silence moments
- map each shot to beat ranges and edit intention
- keep lyrics out of public prompts unless the user owns the lyrics and explicitly requests them

For Seedance-style scene prompts, audio should be diegetic only: footsteps, crowd, breath, cloth, room tone, weather, props, vehicles, spoken words physically in-frame.

### 4. Scene And Shot Ladder

Use one shot ledger row per generated motion attempt:

- `shot_id`: stable ID such as `S001`
- `world`: stadium, narrative city, dance void, BTS, environment plate
- `mode`: narrative, studio, action, performance, atmospheric
- `runtime`: seconds for this shot
- `characters`: visual marker slugs, not prose names
- `references`: image/video/audio refs used in the generation UI
- `prompt_file`: the exact generation prompt
- `provider`: Seedance, Veo, Runway, Kling, Pika, local edit, etc.
- `status`: planned, prompted, generated, selected, rejected, edited, replaced
- `selected_asset`: final chosen take path or URL
- `notes`: visible issues, fixes, continuity risks

For complex scenes, split choreography into beats before writing the prompt. A single prompt should not carry a whole music video unless the generator actually supports long coherent sequences.

### 5. QC Gates

Run bundle checks at these points:

- after character bible lock
- after the first prompt batch
- before final edit assembly
- before YouTube/TikTok handoff
- after publish evidence is captured

Block or fix:

- missing final video path before publish
- missing music rights note
- shot prompts that use character names instead of visual markers
- obvious non-diegetic music instructions in generation prompts
- missing reference assets for recurring characters
- final publish metadata without channel/profile
- private absolute paths in shareable bundles

### 6. Publish Handoff

Before opening YouTube Studio or TikTok:

- export the YouTube or TikTok handoff bundle
- render the production report
- keep final title, description, tags, thumbnail, privacy, audience, source provenance, and attribution in one place
- use the logged-in OpenClaw browser profile
- capture public URL or Studio URL and screenshot evidence after publish or schedule

## Platform Adapters

Read `references/platform-adapters.md` when packaging for Claude, Codex, OpenClaw, GitHub, or ClawHub.

Read `references/production-bible.md` when building the JSON bundle by hand or adding fields not covered by the scripts.

Read `references/publisher-handoff.md` before handing a completed export to YouTube or TikTok.

## Bundled Scripts

- `scripts/init_video_bundle.py`: create the production bundle skeleton.
- `scripts/add_video_shot.py`: append or replace shot ledger entries.
- `scripts/check_video_bundle.py`: validate references, prompt hygiene, rights notes, final export, and publish readiness.
- `scripts/render_video_plan.py`: render a markdown plan/report from the bundle.
- `scripts/export_youtube_handoff.py`: create a bundle compatible with the OpenClaw YouTube creator workflow.
- `scripts/export_tiktok_handoff.py`: create a TikTok handoff bundle for the OpenClaw publisher workflow.

## Done Criteria

The task is complete only when there is:

- a production bundle with locked characters, music map, shot ledger, and provenance
- a QC report with no blocking errors
- a final video export path
- a YouTube/TikTok handoff bundle if publishing is requested
- captured publish URL/evidence when the user asked to publish live
