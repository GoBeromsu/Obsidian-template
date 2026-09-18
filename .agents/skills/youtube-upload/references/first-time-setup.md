# First-time setup

Own one-time YouTube upload environment and OAuth setup.

### Prerequisites
- GCP project: `obsidian-385509` (project number: `1084198536329`)
- YouTube Data API v3 must be enabled in this project
- Enable at: https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=1084198536329
- ffmpeg must be installed (`brew install ffmpeg`)
- `gjc` must be installed and authenticated for the configured non-Anthropic
  provider/model (default `openai-codex/gpt-5.6-sol`)
- For subtitles, mlx-whisper is auto-installed by `uv run` on first use of
  `transcribe_srt.py` (no manual install needed)

### Manual setup
1. Ensure YouTube Data API v3 is enabled in your Google Cloud project
2. Download OAuth client ID JSON from Google Cloud Console
3. Save it to `${HOME}/.config/youtube-upload/credentials.json`
   (or symlink from gws: `ln -s ~/.config/gws/client_secret.json ${HOME}/.config/youtube-upload/credentials.json`)
4. Run: `uv run "${SKILL_DIR}/scripts/upload.py" --auth-only`
5. Complete OAuth consent in browser (youtube.upload scope)
6. Place your face photo at `${SKILL_DIR}/assets/face.png`
7. Supply an optional Obsidian graph view screenshot through the thumbnail command's `--background` value

### Automated setup (craft-skills:browser with Aside backend)
If the manual browser consent is blocked (headless environment, expired token):
1. Start OAuth flow with browser redirect captured:
   ```bash
   BROWSER=echo uv run "${SKILL_DIR}/scripts/upload.py" --auth-only
   ```
   This prints the OAuth URL to stdout instead of opening a browser.
2. Complete consent with `craft-skills:browser`, explicitly selecting its Aside
   backend: open the printed OAuth URL in a signed-in browser session and approve
   the Google login + consent screen; wait for the local redirect to complete.
3. Token is saved to `${HOME}/.config/youtube-upload/token.json`
