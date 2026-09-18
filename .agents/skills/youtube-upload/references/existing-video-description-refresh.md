# Existing video description refresh

Use this reference when Beomsu asks to improve descriptions for already-published own-channel uploads, especially a recent window such as “이번 주에 올린 것들”.

## Durable workflow

1. Compute the requested window in KST with `date`/Python, then select uploads from the channel uploads playlist by `publishedAt`.
2. Verify OAuth channel identity before editing: `channels().list(mine=True)` should return `Beomsu Koh | 고범수`.
3. Fetch target videos with `videos().list(part="snippet,status,contentDetails,localizations")`.
4. Obtain and save the complete transcript for each video. If public extraction
   is disabled, recover it from the audio. If no complete transcript can be
   obtained, stop that video's text update; title/metadata alone cannot satisfy
   the semantic gate.
5. Write the merged desired localizations to a JSON file, then update the
   description and localizations through the canonical uploader:
   ```bash
   uv run "${SKILL_DIR}/scripts/upload.py" --update "<video_id>" \
     --transcript "/tmp/<video_id>-transcript.txt" \
     --description "<new_primary_description>" \
     --localizations-file "/tmp/<video_id>-localizations.json"
   ```
   Add `--title` or `--tags` only when those fields change. The uploader fetches
   current snippet/localizations, constructs the exact merged outgoing metadata,
   and validates it before the first mutating request. Exit 1 and exit 2 both
   stop without mutation.
6. Preserve existing localized titles and non-target languages in the desired
   object; ensure `en` and `ko` have non-empty descriptions when useful.
7. Verify with a fresh API read for each video: primary description non-empty, `en` localization description non-empty, and `ko` localization description non-empty.

## Description shape

- Shorts: 1-sentence hook/summary and 4–8 hashtags. No fabricated timestamps,
  links, or subscribe/like CTA.
- Long-form videos with transcript evidence: 1–2 paragraph hook/summary,
  timestamp chapters starting at `0:00`, and 5–10 hashtags. Do not add links
  or subscribe/like CTA.
- Korean/English localization: natural translation, not literal machine phrasing;
  keep the same promise without adding links or CTA.

## Reporting shape

Report compactly:

- window used
- video URLs/IDs touched
- description/localization fields verified
- transcript-disabled caveats

Avoid tables unless Beomsu explicitly asks for them.

## Captions and dubbing support

When Beomsu asks to improve descriptions, titles, localizations, captions, or dubbing support for already-published own-channel videos, update the existing records through YouTube Data API instead of re-uploading.

### Bulk description / localization refresh

Use `references/existing-video-description-refresh.md` for the concise runbook and reporting shape.

When Beomsu asks to strengthen descriptions for “this week’s uploads” or a similar recent window:

1. Compute the date window live in KST; do not infer the week from model context.
2. Verify the OAuth channel with `channels().list(mine=True)` and confirm it is `Beomsu Koh | 고범수` before editing.
3. Read the uploads playlist (`contentDetails.relatedPlaylists.uploads`), fetch videos with `videos().list(part="snippet,status,contentDetails,localizations")`, and select only videos whose `publishedAt` falls inside the requested window.
4. Inspect current descriptions and localizations. If primary descriptions are empty or thin, generate primary-language descriptions with a hook, 3–6 bullets, and hashtags (no links, no subscribe/like CTA — match the Step 2 template). Add timestamps for long-form videos when transcript or chapter evidence is available; avoid fabricated timestamps for transcript-disabled short clips.
5. Obtain and save the complete transcript for each target. If public transcript
   extraction is disabled or absent, recover it from the audio before proposing
   text changes. If no complete transcript can be obtained, stop that video's
   title/description/tags/localizations update; visible metadata alone is not
   enough for the semantic gate.
6. Write the merged desired localizations to a JSON file and update through the
   canonical uploader so it fetches existing values, validates the exact merged
   outgoing metadata, and mutates only after exit 0:
   ```bash
   uv run "${SKILL_DIR}/scripts/upload.py" --update "<video_id>" \
     --transcript "/tmp/<video_id>-transcript.txt" \
     --description "<new_primary_description>" \
     --localizations-file "/tmp/<video_id>-localizations.json"
   ```
   Add `--title` or `--tags` when those text fields change. Optional validator
   overrides are `--validation-policy`, `--validation-model`,
   `--validation-timeout`, and `--validation-max-chars`. Exit 1 or 2 stops
   before the first mutating request.
7. Preserve existing localized titles, fill localized descriptions, and merge
   rather than replace other languages; `upload.py` performs the final merge
   against the fetched current object before validation.
8. Verify after mutation with a fresh read: primary description non-empty, `en`
   description non-empty, and `ko` description non-empty for each updated video.
9. Report the exact video IDs/URLs touched, what changed, and transcript-disabled caveats. Keep it compact and table-free.

### Captions / dubbing support

When Beomsu asks to add a transcript/captions/dubbing support to an already-published
own-channel video:

1. Find the latest upload or target video via YouTube Data API (`channels().list(mine=True)`
   → uploads playlist → `playlistItems().list`). Verify the channel title is
   `Beomsu Koh | 고범수`.
2. Check public transcripts first with `youtube-content/scripts/fetch_transcript.py`.
   If transcripts are disabled or absent, download the audio with `yt-dlp` and
   transcribe locally.
3. For timestamped captions, prefer `mlx-whisper` over `scripts/transcribe.py`, because
   `scripts/transcribe.py` returns plain text only and currently hardcodes
   `language: "en"` in its JSON output:
   ```bash
   mkdir -p /tmp/yt_caption_work
   yt-dlp -f 'bestaudio/best' --extract-audio --audio-format wav \
     -o '/tmp/yt_caption_work/%(id)s.%(ext)s' 'https://www.youtube.com/watch?v=<video_id>'

   uv run --with mlx-whisper python - <<'PY'
   import json, mlx_whisper
   res = mlx_whisper.transcribe('/tmp/yt_caption_work/<video_id>.wav',
     path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='ko')
   open('/tmp/yt_caption_work/ko_segments.json','w').write(json.dumps(res, ensure_ascii=False))
   PY
   ```
4. Convert Whisper segments to `.srt` and upload captions through YouTube Data API:
   ```python
   from googleapiclient.http import MediaFileUpload
   body={"snippet":{"videoId": VIDEO_ID, "language":"ko", "name":"Korean transcript (Hermes)", "isDraft":False}}
   youtube.captions().insert(part="snippet", body=body,
     media_body=MediaFileUpload('/tmp/yt_caption_work/video.ko.srt', mimetype='application/octet-stream')).execute()
   ```
   Repeat with `language="en"` for an English translation track if available.
5. For Korean-spoken videos, set existing video language metadata to Korean:
   ```bash
   uv run "${SKILL_DIR}/scripts/upload.py" --update "<video_id>" --language ko
   ```
   This corrects `defaultLanguage` and `defaultAudioLanguage`, which is required for
   YouTube auto-dubbing eligibility.
6. Be explicit about the dubbing limit: YouTube Data API v3 cannot enable
   auto-dubbing or upload alternate audio tracks. Setting `defaultAudioLanguage=ko`
   plus English captions/localization prepares the video; YouTube Studio's
   Automatic dubbing setting must be enabled for YouTube to generate the English
   dub.
7. If no Ataraxia upload note exists, create/update
   `15. Work/02 Area/Youtube/<title>.md` with transcript, translation, video_id,
   source URL, duration, and language. Avoid direct writes only under Ataraxia
   `80. References/`; this YouTube work-area path is writable.

Legacy transcript extraction option: if YouTube already has a transcript, use
`craft-skills:browser` (explicitly select its Aside backend), `defuddle`, or
`youtube-content/scripts/fetch_transcript.py` and create the vault note manually.
