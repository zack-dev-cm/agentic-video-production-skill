# Publisher Handoff

Use this reference when a final edit is ready for OpenClaw-assisted YouTube or TikTok publishing.

## Required Before Upload

- final video file exists locally
- export has the expected aspect ratio and duration
- title, description, privacy, audience, tags, and playlist are selected
- thumbnail exists if the platform run needs one
- music provenance and rights note are recorded
- generated visual providers and selected asset IDs are recorded where known
- operator has named the OpenClaw browser profile

## YouTube Metadata

Description should include, when relevant:

- short human description of the video
- music attribution or license note
- AI-generated visual disclosure if the channel policy requires it
- source chain summary such as `visual:Seedance`, `image:Nano Banana`, `audio:Suno`, `edit:DaVinci`
- links requested by the operator

Do not paste private prompt archives into public descriptions.

## TikTok Metadata

Keep captions shorter than YouTube descriptions. Preserve only attribution that is required or strategically useful. Hashtags should be concrete and not spammy.

## OpenClaw Execution Log

Record these milestones in the YouTube creator bundle or equivalent log:

- opened Studio/upload page in named profile
- uploaded file
- set title and description
- set thumbnail, playlist, audience, privacy, schedule
- reviewed checks/copyright page
- paused for manual challenge if any
- published or scheduled
- captured Studio URL and public URL
- opened public URL and captured evidence

## Handoff To Existing Skills

If the local environment has `openclaw-youtube-tiktok-publisher`, use it for browser execution after this skill exports the production and YouTube bundles.

If the public ClawHub `youtube-openclaw-creator` skill is installed, use its scripts to append execution steps, validate the YouTube bundle, and render the final report.

For TikTok, export `runs/tiktok-openclaw-bundle.json` with `scripts/export_tiktok_handoff.py`, then use the OpenClaw publisher skill to execute the browser upload and append any final post URL or screenshot evidence back into the production bundle.
