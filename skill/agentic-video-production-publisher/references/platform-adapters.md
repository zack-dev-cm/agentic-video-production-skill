# Platform Adapters

## Claude

Package the skill folder itself as a zip whose top-level directory contains `SKILL.md`:

```bash
cd skill
zip -r ../dist/agentic-video-production-publisher-claude.zip agentic-video-production-publisher
```

Upload the zip in Claude through Settings -> Capabilities -> Skills -> Upload skill.

Claude can use the workflow instructions directly. If it cannot run local scripts, it should maintain the JSON bundle structure in a text artifact and ask the operator to run the scripts locally when deterministic validation is needed.

## Codex

Install by copying or symlinking the skill folder into the Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skill/agentic-video-production-publisher "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Codex should run the bundled Python scripts for bundle creation, validation, report rendering, and YouTube handoff export. Use the local filesystem paths in the bundle while working, then render shareable reports before external publication.

## OpenClaw

OpenClaw should use this skill as a planning and execution ledger, not as a credential holder. Use OpenClaw browser automation only for logged-in UI operations such as YouTube Studio or TikTok upload.

Rules:

- Require a named browser profile that is already logged into the target account.
- Pause on CAPTCHA, 2FA, passkeys, account recovery, billing, copyright disputes, or final publish confirmation if the operator has not pre-approved it.
- Save screenshots for upload, metadata review, final confirmation, and first public view.
- Record every browser milestone in the publish bundle.

## GitHub

Use a public repo with:

- `README.md`
- `LICENSE`
- `skill/agentic-video-production-publisher/SKILL.md`
- `skill/agentic-video-production-publisher/agents/openai.yaml`
- bundled scripts and references

Do not commit generated videos, music files, private prompt archives, cookies, browser profiles, tokens, or unreleased third-party skill zips.

## ClawHub

Publish the skill folder, not the repo root:

The current `clawhub publish` CLI publishes under the logged-in account. Run `clawhub whoami` before publishing if the owner matters.

```bash
clawhub publish "$PWD/skill/agentic-video-production-publisher" \
  --slug agentic-video-production-publisher \
  --name "Agentic Video Production Publisher" \
  --version 1.0.2 \
  --tags "video,openclaw,youtube,tiktok,ai-production,skills" \
  --changelog "Align ClawHub tags with TikTok support and avoid absolute source-bundle paths in handoff exports."
```

After publish, inspect the ClawHub entry and confirm moderation status before calling the release complete.
