# Transcription workflow

Own audio extraction, standard transcription, and timestamped subtitle transcription.

## 1. Extract audio and transcribe

mlx-audio cannot read mp4 containers directly. Extract audio to wav first:

```bash
ffmpeg -i '<mp4_path>' -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/yt_audio.wav -y
```

Then transcribe:

```bash
# Ask the runtime's local-file reader for the absolute local path of this loaded
# youtube-upload/SKILL.md. If it cannot return a readable path, stop rather than
# guessing an installation layout or source checkout.
SKILL_FILE="<runtime-resolved path of the loaded youtube-upload/SKILL.md>"
test -f "${SKILL_FILE}" || { printf '%s\n' 'ERROR: loaded youtube-upload SKILL.md is unavailable.' >&2; exit 1; }
SKILL_DIR="$(cd -- "$(dirname -- "${SKILL_FILE}")" && pwd -P)" || exit 1
test -f "${SKILL_DIR}/scripts/transcribe.py" || { printf '%s\n' 'ERROR: loaded youtube-upload scripts are unavailable.' >&2; exit 1; }
uv run "${SKILL_DIR}/scripts/transcribe.py" /tmp/yt_audio.wav
```

This outputs JSON to stdout:
```json
{"transcript": "...", "duration_seconds": 123.4, "language": "en"}
```

If duration_seconds > 3600, warn: "Video is over 1 hour. Transcription may take
several minutes."

Parse the JSON and save `transcript` and `duration_seconds` for the next steps.

**If subtitles are requested** (`--subs`, or the user asked for captions/자막 or a
global audience): Qwen3-ASR gives no timestamps, which subtitles need. Use the
whisper-based timestamped transcriber instead — it doubles as the timing backbone
for every translated track:

```bash
mkdir -p /tmp/subs
uv run "${SKILL_DIR}/scripts/transcribe_srt.py" /tmp/yt_audio.wav /tmp/subs/<spoken_lang>.srt --language "<spoken_lang>"
```

This writes `/tmp/subs/<spoken_lang>.srt` (raw, timestamped) +
`/tmp/subs/<spoken_lang>.segments.json` and prints `duration_seconds`. When you
use this path, you do NOT also need `transcribe.py` — the cleaned SRT (next
step) is your transcript source.
