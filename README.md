# Agentic Video Production Publisher

Public skill for running AI video production end to end: consistent characters, music beat maps, complex scene ledgers, generated-asset provenance, and OpenClaw YouTube/TikTok handoff.

The skill is designed for Claude, Codex, OpenClaw, GitHub, and ClawHub. It does not bundle third-party prompt libraries or private generated media.

## Skill

- `skill/agentic-video-production-publisher`

## What It Does

- Locks recurring characters through visual markers and reference assets.
- Separates identity, wardrobe, environment plates, motion prompts, and final edit provenance.
- Keeps music as an edit map while keeping generation-scene audio diegetic.
- Validates prompt hygiene, missing rights notes, missing references, and publish readiness.
- Exports a YouTube handoff bundle compatible with supervised OpenClaw publishing workflows.

## Quick Start

```bash
python3 skill/agentic-video-production-publisher/scripts/init_video_bundle.py \
  --out runs/video-bundle.json \
  --title "Project title" \
  --owner "zack-dev-cm" \
  --aspect-ratio "16:9" \
  --runtime 90
```

```bash
python3 skill/agentic-video-production-publisher/scripts/check_video_bundle.py \
  --bundle runs/video-bundle.json \
  --repo-root . \
  --out reports/video-qc.json
```

## Claude Package

```bash
mkdir -p dist
cd skill
zip -r ../dist/agentic-video-production-publisher-claude.zip agentic-video-production-publisher
```

Upload the zip in Claude through Settings -> Capabilities -> Skills -> Upload skill.

## Codex Install

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/agentic-video-production-publisher "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## ClawHub Publish

```bash
clawhub publish "$PWD/skill/agentic-video-production-publisher" \
  --owner zack-dev-cm \
  --slug agentic-video-production-publisher \
  --name "Agentic Video Production Publisher" \
  --version 1.0.0 \
  --tags "video,openclaw,youtube,ai-production,skills" \
  --changelog "Initial public release for consistent-character AI video production and OpenClaw publisher handoff." \
  --clawscan-note "Workflow creates local manifests and publish handoff bundles; logged-in browser publishing remains supervised and uses existing OpenClaw profile sessions."
```

## Safety

Do not commit generated videos, music, cookies, account sessions, tokens, browser profiles, private prompt archives, or copied third-party skill bodies.
