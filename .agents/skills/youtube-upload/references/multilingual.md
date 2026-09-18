# Multilingual Subtitles & Localization

Read this when the user wants subtitles/captions in multiple languages, localized
titles/descriptions beyond the en↔ko default, or asks to "reach a global audience".
This is the sub-pipeline that turns one upload into a video that shows the right
language to viewers everywhere: a Riyadh viewer sees Arabic, a São Paulo viewer
sees Portuguese, a 上海 viewer sees 简体中文 — same video, no extra distribution.

There are two independent layers, and they are NOT the same thing:

| Layer | What it is | API surface | Script |
|---|---|---|---|
| **Captions** | On-screen subtitle tracks (.srt per language) | `captions().insert` | `subtitle.py` |
| **Localizations** | Translated title + description per locale | `videos().update(part=localizations)` | `build_localizations.py` + `upload.py` |

Do both for full coverage. Captions need real timestamps; localizations don't.

## Default language set

Unless the user names a set, default to the most-spoken world languages + Korean:

```
en, es, hi, ar, fr, pt, ru, zh, ko
```

File codes map to YouTube BCP-47 codes automatically in `subtitle.py` /
`build_localizations.py`: `zh → zh-Hans`, `pt → pt-BR`. Use the file codes
(`zh`, `pt`) for SRT filenames; use the BCP-47 codes (`zh-Hans`, `pt-BR`) as the
keys inside localization fragments.

## Why captions need a real transcription, not Qwen3-ASR

`transcribe.py` (Qwen3-ASR) returns flat text with **no timestamps** — fine for
the readable transcript and metadata, useless for subtitles. Translated tracks
especially need timing, and YouTube's `sync=true` only works for the
same-language-as-audio track. So:

1. Determine the actual spoken-language code (`<spoken_lang>`) and run
   `transcribe_srt.py` (mlx-whisper) once to get the **timing backbone** —
   a timestamped `<spoken_lang>.srt` plus `*.segments.json`.
2. **Clean** the source-language cues (see "Transcript correction" in SKILL.md) — whisper
   output has the same disfluencies and occasionally a *degenerate loop* (a
   segment repeating one phrase 50×). Fix the text, keep the timestamps.
3. **Translate** the cleaned source-language SRT into each target language, reusing the
   **exact same timestamps**. Every track has identical cue timing; only the text
   differs.

## Step-by-step

### A. Timing backbone

```bash
uv run "$SKILL_DIR/scripts/transcribe_srt.py" /tmp/yt_audio.wav /tmp/subs/<spoken_lang>.srt --language <spoken_lang>
```

Produces `/tmp/subs/<spoken_lang>.srt` (raw, timestamped) and
`/tmp/subs/<spoken_lang>.segments.json`.

### B. Clean the source-language SRT

Edit `/tmp/subs/<spoken_lang>.srt` cue-by-cue: remove stutters/false starts, collapse any
degenerate repeated segment, make each cue a readable line. **Never touch the
`-->` timestamp lines.** The cleaned cue text, concatenated, is also the readable
transcript for the vault note — so you clean once and reuse.

### C. Translate into each language (parallelize)

For each target language, produce `/tmp/subs/<code>.srt` with the **same cue
numbers and same timestamps** as `<spoken_lang>.srt`, translating only the text lines. This
is ideal work for parallel subagents — one per language — because the tracks are
independent. Give each agent `<spoken_lang>.srt` and instruct:
- keep cue numbers and `-->` timestamp lines byte-for-byte identical,
- translate only the spoken text,
- natural/idiomatic translation, not word-for-word.

Validate every file has the same cue count as `<spoken_lang>.srt` before uploading.

### D. Upload caption tracks

Captions require the `youtube.force-ssl` scope (the plain `youtube` scope returns
403 — both `upload.py` and `subtitle.py` already request force-ssl).
`subtitle.py` requires the caller-scoped `OAUTHLIB_INSECURE_TRANSPORT=1` setting
for its localhost callback; do not persist it or add it to shared environment
configuration.

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 uv run "$SKILL_DIR/scripts/subtitle.py" "<VIDEO_ID>" \
  --dir /tmp/subs --langs en,es,hi,ar,fr,pt,ru,zh,ko --replace
```

`--replace` deletes an existing same-language track before re-inserting (safe to
re-run). Omit it to skip languages that already have a track.

### E. Localized titles + descriptions (all languages)

For each locale, write a fragment file `/tmp/loc/<code>.json`:

```json
{"es": {"title": "...", "description": "..."}}
```

Translate the title (≤ 100 chars) and the full description **structure** —
hook/summary, Timestamps, and hashtags. Translate the chapter *labels* but
**keep the timestamp numbers exactly** (`0:00`, `1:20`, …). Do not add, remove,
or translate links, tool URLs, or subscribe/like CTAs; the canonical
three-block description contract forbids them. Use ASCII digits in every
language (incl. Arabic/Chinese) so YouTube still parses chapters.

Merge + validate (catches dropped chapters and over-long titles before upload):

```bash
uv run "$SKILL_DIR/scripts/build_localizations.py" \
  --dir /tmp/loc --output /tmp/localizations.json
```

Apply:

```bash
uv run "$SKILL_DIR/scripts/upload.py" --update <VIDEO_ID> \
  --transcript /tmp/yt_validate_transcript.txt \
  --localizations-file /tmp/localizations.json
```

`--transcript <path|->` is mandatory for localization changes. `upload.py`
fetches and merges the existing localizations, validates the complete transcript
against that exact outgoing object, and mutates only after validator exit 0, so
en/ko set during the main upload are preserved. Exit 1 (execution/evidence
error) and exit 2 (violations) both stop before mutation; neither falls back to
a private update.

## Caveats learned the hard way

- **Unescaped quotes break a fragment.** A translated string containing a raw
  `"` (e.g. Chinese quoting a term) invalidates the JSON. Prefer the language's
  own quotation marks (Chinese「」, French «», German „") or escape with `\"`.
  `build_localizations.py` reports exactly which fragment failed to parse.
- **Translators "correct" chapter timestamps.** They rewrite `1:20` into prose
  and the chapter markers vanish. `build_localizations.py` hard-fails if any
  description drops a timestamp.
- **Arabic/Chinese digits.** Keep timestamps in ASCII digits, not Arabic-Indic
  or full-width forms, or YouTube won't recognize chapters.
- **Caption scope.** force-ssl is mandatory for `captions()`. If you only ever
  ran the old `youtube` scope, delete `~/.config/youtube-upload/token.json` and
  re-auth so the new scope is granted.
- **OAuth re-auth must be interactive.** A detached background `--auth-only`
  can't open the browser or hold the localhost callback — it dies silently. Have
  the user run `uv run "$SKILL_DIR/scripts/upload.py" --auth-only` in their own
  shell and approve the consent screen.
- **Cue counts must match.** If a translated SRT has a different number of cues
  than `<spoken_lang>.srt`, the timing has drifted — regenerate that track.
