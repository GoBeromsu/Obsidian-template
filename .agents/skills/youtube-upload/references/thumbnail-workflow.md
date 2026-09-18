# Thumbnail workflow

Own thumbnail modes, generation commands, font verification, and user review.

### 3. Generate thumbnail

Two modes are available:

**Graph view mode** (default):
```bash
uv run "${SKILL_DIR}/scripts/generate_thumbnail.py" \
  --face "${SKILL_DIR}/assets/face.png" \
  --background "<user-supplied-graph-view-image>" \
  --text "<thumbnail_hook>" \
  --output /tmp/yt_thumbnail.jpg
```
Creates 1280x720 JPEG: Obsidian graph view background, dimmed overlay, bold
centered uppercase text, circular face inset in the bottom-right corner.

Hook text containing Hangul automatically switches to a Hangul-capable display
font (Noto Sans KR Black if installed, else Apple SD Gothic Neo Heavy); Latin
text keeps the default Impact. After generating, view the image and confirm no
character renders as a box (tofu) before showing it to the user.

**Face-only mode** (use when `--no-graph-background` is specified, or when no graph view image is supplied):
```bash
uv run "${SKILL_DIR}/scripts/generate_thumbnail.py" \
  --face "${SKILL_DIR}/assets/face.png" \
  --text "<thumbnail_hook>" \
  --output /tmp/yt_thumbnail.jpg
```
Creates 1280x720 JPEG: face fills canvas, dark gradient on left, bold text on
the left side.

Both modes require `assets/face.png`; `--no-graph-background` selects the
face-only layout and does not waive that prerequisite. If the asset is absent,
report the unavailable prerequisite, retain prepared artifacts, and stop before
upload, OAuth, or vault effects. Do not generate or open a placeholder and do
not omit `--thumbnail` unless the user had already explicitly requested no
custom thumbnail. For that exception, record `Thumbnail: N/A — <reason>` and
never claim rendered or thumbnail-review proof; semantic validation,
artifact-bound SARI, and separate effect authority remain binding.

When a thumbnail was generated, open it locally for the user to review before
uploading:
```bash
open /tmp/yt_thumbnail.jpg
```
