# Upload caveats and expected output

Own troubleshooting notes and the successful-run console transcript.

## Caveats


- **mp4 format not supported by mlx-audio.** The miniaudio library cannot decode
  mp4 containers. Always extract audio to wav via ffmpeg before transcribing:
  ```bash
  ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/yt_audio.wav -y
  ```

- **Captions need the `youtube.force-ssl` scope.** The plain `youtube` scope
  returns 403 on `captions().insert`. Both `upload.py` and `subtitle.py` request
  force-ssl (a superset covering upload, thumbnails, localizations, and captions).

- **Qwen3-ASR has no timestamps.** For subtitles, transcribe with
  `transcribe_srt.py` (mlx-whisper) to get segment timing. Translated tracks
  reuse those exact timestamps — never re-time per language, or the tracks drift.

- **Multilingual subtitle/localization sub-pipeline** (language set, translation,
  fragment format, validation, caveats) lives in `references/multilingual.md`.
  Read it whenever more than the default en↔ko pair is involved.

- **Custom thumbnails require phone verification.** Your YouTube channel must
  have phone verification enabled to set custom thumbnails via the API. Go to
  YouTube Studio → Settings → Channel → Feature eligibility if thumbnails.set()
  returns a 403.

- **`obsidian move` silently fails.** Use `obsidian eval` + `app.fileManager.renameFile()`
  instead when moving/renaming vault notes:
  ```bash
  obsidian eval vault=Ataraxia code="const f=app.vault.getAbstractFileByPath('old/path.md'); if(f) await app.fileManager.renameFile(f,'new/path.md');"
  ```
  This guarantees wikilink auto-update. Never use filesystem `mv`/`cp` inside the vault.

- **`obsidian property:set` hangs on stdin.** When called from a script or pipeline,
  property:set may block waiting for stdin. Append `< /dev/null` to each call:
  ```bash
  obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=type value=video < /dev/null
  ```

- **`uv run` is required.** PEP 668 (Homebrew Python) blocks global `pip install`.
  All scripts use `# /// script` dependency headers so `uv run` auto-installs deps
  in an isolated env. Never `pip install` manually.

- **Use the `youtube.force-ssl` OAuth scope, not plain `youtube`.** Existing tokens
  may have been minted for `https://www.googleapis.com/auth/youtube.force-ssl` from
  the Claude/Obsidian skill. If the script declares only `.../auth/youtube`, token
  refresh can fail with `invalid_scope: Bad Request` and `run_local_server()` will
  wait on a localhost consent URL, making uploads look like they are hanging before
  any bytes move. Keep `SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]`.

- **Large originals can hit transient `BrokenPipeError`.** The Desktop screen
  recordings may be 1GB+ for a few minutes of video. `upload.py` should retry
  `request.next_chunk()` transport errors instead of failing the whole resumable
  upload at 50-70%.

- **Apostrophes in filenames.** When the generated title contains `'`, use template
  literals (backtick strings) in `obsidian eval` code to avoid shell quoting issues.

- **HEREDOC `<<'EOF'` does not expand `$(...)`.** Quoted heredocs treat the
  body literally, so `$(cat /tmp/yt_upload_feedback.md)` inside `<<'BODY_EOF'`
  would appear verbatim instead of inlining the file. Step 6 composes the note
  body inline via a shell group inside command substitution
  (`content="$({ echo ...; cat ...; })"`) to interpolate cleanly without an
  intermediate tmp file. Use the same pattern for any future composition step.

- **Auto-dubbing cannot be enabled via the YouTube Data API v3.** It must be
  toggled in YouTube Studio → Settings → Content → Automatic dubbing. Setting
  `defaultAudioLanguage` via API is necessary but not sufficient — it tells
  YouTube what language the audio is in, but the creator must opt in to dubbing
  separately.

- **Expressive Speech does NOT support Korean (as of 2026).** The tone/emotion
  preservation feature only covers 8 languages: English, French, German, Hindi,
  Indonesian, Italian, Portuguese, Spanish. Korean auto-dubs use the standard
  (non-expressive) voice.

- **Auto-dubbing eligibility requirements.** The video must be under 120 minutes,
  have detectable speech, and the creator must have YouTube Partner Program or
  advanced features enabled. Not all videos qualify.

- **Multi-language audio track uploads are UI-only.** The YouTube Data API v3 has
  no endpoint for uploading additional audio tracks. Use YouTube Studio →
  Content → Edit video → Languages tab → Add dub for manual dub uploads.


## Expected console output (successful run)


```
[ffmpeg] Extracting audio...
size=  20289KiB time=00:10:49.25 bitrate=256.0kbits/s
Loading model mlx-community/Qwen3-ASR-1.7B-8bit...
Model loaded in 3.9s
Transcribing: yt_audio.wav
Done: 24.9s, 4576 chars, 1073 tokens
{"transcript": "...", "duration_seconds": 649.3, "language": "en"}
Thumbnail saved: /tmp/yt_thumbnail.jpg (1280x720)
Uploading: my_video.mp4
Upload progress: 25%
Upload progress: 50%
Upload progress: 75%
Upload progress: 100%
Thumbnail set for dQw4w9WgXcQ
{"video_id": "dQw4w9WgXcQ", "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
```
