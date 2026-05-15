# Post-Launch Critical Review: v1.0.0 -> v1.0.1

## Verdict

Rework, then ship free.

The v1.0.0 skill had a useful production spine, but it was too broad in its public promise and under-tested for a package meant to coordinate expensive video-generation work. v1.0.1 tightens the parts that can fail deterministically.

## What Was Weak

1. ClawHub command drift: the docs included `--owner` and `--clawscan-note`, but the current local `clawhub publish` CLI rejected those flags.
2. TikTok overclaim: the description promised YouTube/TikTok handoff, but only the YouTube exporter existed.
3. Character consistency blind spot: the checker did not warn when shots referenced character slugs while `bundle.characters` was empty.
4. Runtime robustness: malformed numeric fields could crash validation instead of returning a useful QC finding.
5. Trust surface: v1.0.0 had smoke checks from the release process but no committed test suite.

## Adjustments Made

- Updated README and platform adapter publish commands to match the current ClawHub CLI.
- Added `scripts/export_tiktok_handoff.py`.
- Updated `scripts/check_video_bundle.py` to warn on shot characters without a character bible.
- Updated numeric parsing so bad runtimes become validation findings instead of tracebacks.
- Added `tests/test_video_scripts.py` covering character-bible warnings, bad runtime handling, and YouTube/TikTok handoff exports.

## Product Gate

| Gate | Score | Reason |
|---|---:|---|
| Painful job | 2 | AI video work burns real credits when identity, prompts, music, and publishing are untracked. |
| First traffic source | 1 | ClawHub/GitHub/OpenClaw users are plausible, but no first 10 named users are recorded. |
| Trust reason | 1 | Public scripts and QC improve trust, but no real production case study is bundled. |
| Share moment | 1 | A clean production bundle/QC report is shareable, but the repo needs an example artifact. |
| Free MVP plan | 2 | Public MIT-0 skill, free ClawHub package, Claude zip, and Codex install path. |
| Kill criteria | 1 | Should be explicit after 30 days: installs, stars, issues, and at least one external video run. |

Decision: Ship free for 30 to 45 days, but do not monetize or claim full automation.

## Remaining Limitations

- It coordinates production; it does not call Higgsfield, Seedance, Suno, or an editor API directly.
- Beat mapping is manual; there is no audio analyzer yet.
- Browser publishing is delegated to OpenClaw publisher skills and still requires a logged-in profile.
- No real finished-video case study is included in the repo.

## Next Experiment

Run one real short-form music-video production through the bundle and publish the non-private artifacts:

- sanitized production bundle
- prompt ledger with private refs removed
- QC report
- YouTube/TikTok handoff report
- final public URL
