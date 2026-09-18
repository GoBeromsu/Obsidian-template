---
name: youtube-upload
description: >-
  "upload video" / "youtube upload" / "영상 업로드" / "이 영상 올려줘" — upload a
  local video to YouTube: transcript-driven metadata, thumbnail, validation,
  multilingual localization and subtitle tracks, and an Obsidian tracking note.
  Raw footage (one or many takes) is edited into a publishable master first.
  Subtitles, transcript correction, and localization are part of this flow, not
  separate skills. Not for other people's videos or YouTube Shorts.
version: 2.0.3
allowed-tools: [Bash, Read, Edit, Write, Grep, Glob, AskUserQuestion]
compatibility: claude-code, hermes, codex
---

# YouTube Upload Pipeline

Upload a local mp4 video to YouTube with auto-generated metadata, branded
thumbnail, and SEO-optimized description, then track it in the Obsidian vault.

## Overview

Pipeline: (optional Step 0: raw footage → edited master) → mp4 → ffmpeg audio
extraction → transcript (mlx-audio) → transcript correction → bilingual metadata
+ chapters + reviewed thumbnail (default) → YouTube upload + language/localization
→ multilingual subtitle tracks (when requested) → vault note.

The default upload path produces:
- A **cleaned transcript**: the raw ASR output is full of stutters ("the the",
  "I I"), false starts, and occasional degenerate loops. We correct it into
  readable prose before it ever reaches a description, subtitle, or vault note —
  unreadable transcripts make for unreadable subtitles.
- A reviewed branded thumbnail: face photo with bold hook text, optionally over
  an Obsidian graph view background. An already explicit user-requested
  no-custom-thumbnail exception is `N/A` with its reason; missing face is never
  that exception.
- An SEO-optimized description with timestamps/chapters generated from the
  transcript
- Bilingual metadata by default (spoken language + the other of English/Korean),
  and **localized titles/descriptions for the full language set** when the user
  wants a global audience
- **Multi-language subtitle (caption) tracks** — timestamped via mlx-whisper,
  cleaned, then translated into each target language (same timing, translated
  text) — when subtitles are requested
- Language metadata (`defaultAudioLanguage`) to enable YouTube auto-dubbing
- Automatic vault note tracking at `15. Work/02 Area/Youtube/`

**For the multilingual subtitle + localization sub-pipeline (the full language
set, translation, caption upload, and its caveats), read
`references/multilingual.md`.** The steps below cover the core single-/dual-language
flow and point to that reference at the multilingual steps.

## When to Use

- Use when uploading your own mp4 video to YouTube
- Use when the user says "upload video", "youtube upload", "영상 업로드"
- Use when the user provides an mp4 path with upload intent
- Use when the input is raw footage — one take or a folder of takes — that
  needs editing into a publishable master first (Step 0)
- Do NOT use for downloading, clipping, or ingesting other people's videos
- Do NOT use for YouTube Shorts (blog-writer handles those)

## Input

- **Required**: mp4 file path
  - If the user provides a `.mov` from iPhone/Desktop, remux it to a temp `.mp4` before upload (do not modify the original):
    ```bash
    ffmpeg -y -i '<mov_path>' -map 0:v:0 -map 0:a:0 -c copy -movflags +faststart /tmp/<safe_name>_youtube_upload.mp4
    ```
    Then use that `/tmp/...mp4` path for `scripts/upload.py`.
- **Optional**:
  - `--title "..."` — override generated title
  - `--description "..."` — override generated description
  - `--privacy private|unlisted|public` — default: private; a different
    visibility is considered only after successful semantic and SARI review
  - `--thumbnail-text "HOOK"` — override generated hook text
  - `--no-graph-background` — use face-only thumbnail layout instead of an optional user-supplied graph view background
  - `--language <code>` — original spoken language of the video (default: auto-detected from transcript). Sets `defaultAudioLanguage` on YouTube.
  - `--localize-ko "제목" "설명"` — override Korean localized title/description
  - `--localize-en "title" "desc"` — override English localized title/description
  - `--subs <langs>` — comma-separated subtitle/localization languages, e.g.
    `en,es,hi,ar,fr,pt,ru,zh,ko`. Default set (when the user asks for multiple
    languages / a global audience): `en,es,hi,ar,fr,pt,ru,zh,ko` — the most-spoken
    world languages + Korean. See `references/multilingual.md`.
  - `--no-subs` — skip subtitle generation entirely (metadata + localization only)
  - `--no-correct` — skip transcript correction (rarely wanted; the raw ASR text
    is hard to read and makes poor subtitles)
  - Validation passthroughs for `upload.py`: `--validation-policy <path>`,
    `--validation-model <provider/model>`, `--validation-timeout <seconds>`,
    and `--validation-max-chars <characters>`. Use these only to select a
    verified policy/backend capacity; they never bypass validation.

## Pipeline

Follow these steps sequentially. Each step must succeed before the next.

## Output Contract

Return one receipt naming the exact verified master, cleaned transcript/audio evidence, primary/localized metadata, thumbnail review (or explicit `N/A — <reason>`), semantic report, artifact-bound `FINAL SARI: APPROVED` receipt, upload/localization/caption IDs, duplicate result, and vault note path only for completed stages. If a prerequisite is unavailable, report it, retain prepared artifacts, and stop before upload/OAuth/vault mutation; do not claim a result.
Run the authenticated GJC gate before new-upload credentials; errors and violations stop every mutation. Semantic validation/SARI remain required but grant no separate OAuth/upload/vault effects. Privacy defaults to private only after review, never as fallback; leave caller environment untouched and use `google-auth-oauthlib` for loopback callbacks.

### 0. Edit raw footage (skip when input is already an edited master)

Classify input as `raw` or `finished` from inspected duration, streams, representative playback, and audio; record the classification, evidence, and decision in the run receipt. Enter this step only for unedited recording material. Produce a verified rendered master, record editing, audio-processing, and color evidence or a justified skip, then continue with that mp4 in Step 1. Read `references/video-editing-workflow.md` for the complete editing workflow.

### 1. Extract audio and transcribe

Extract mp4 audio to WAV, then produce the transcript and duration for later steps. When subtitles are requested, produce timestamped SRT tracks instead. Read `references/transcription-workflow.md` for the extraction, runtime-path, transcription, and timestamped-caption commands.

### 1.5. Correct the transcript

Raw ASR output is not publishable. Qwen3-ASR and whisper both emit the speaker's
disfluencies verbatim — repeated words ("the the", "I I I"), false starts,
filler, and occasionally a *degenerate loop* where one phrase repeats dozens of
times. That text is unpleasant to read in a vault note and actively bad as a
subtitle. So before generating any metadata, clean it:

- Remove stutters, repeated words, and false starts; keep the speaker's meaning
  and voice — this is light editing, not rewriting or summarizing.
- Collapse any degenerate repeated run into the single intended sentence.
- Fix obvious ASR mishearings when the intent is clear from context (e.g.
  "white combinator" → "Y Combinator", "Andrew Young" → "Andrew Ng").
- Add sentence punctuation so it reads as prose.
- Listen to the audio around every material correction (proper noun, number,
  negation, product name, or unclear phrase) and record the timestamp and
  before/after text. Context-only guesses are not corrections.

If you transcribed via **whisper for subtitles**, clean it *cue-by-cue* directly
in `/tmp/subs/<spoken_lang>.srt`: fix each cue's text but NEVER touch the `-->` timestamp
lines. The cleaned cues, concatenated, become the readable transcript for the
vault note (Step 6) and the source for translated subtitle tracks. If you
transcribed via **Qwen3-ASR** (no subtitles), just clean the flat transcript.

Skip only if `--no-correct` was passed and the run receipt states why publishing
verbatim ASR is acceptable. Save the cleaned transcript and audio-grounding
evidence for Steps 2 and 6.

### 2. Generate metadata

From the transcript, generate YouTube metadata yourself (do NOT call a separate
script). Determine the spoken language from the transcript's `language` field
(or from `--language` if provided). Generate all metadata in the **primary
language** (matching the spoken audio), then generate a **localized version** in
the other language (English ↔ Korean).

**Primary metadata** (in the spoken language):

**Title** (up to 90 characters; front-load the hook in the first 50 characters):
- Promise a specific, deliverable outcome — the viewer predicts ≥70% of the video's content from the title alone
- Trigger genuine curiosity without manufactured urgency, shock-caps, or outcome exaggeration; avoid vague all-caps superlatives and impossible-outcome framing — see `references/title-packaging-rubric.md` for the full bad-pattern diagnostic table
- Place the primary keyword in the first 0–5 words; use sentence case (acronyms such as API, CLI, AI and proper tool names may be uppercase)
- These rules apply equally to the localized (Korean) title — see `references/title-packaging-rubric.md` for bilingual guidance and rewrite examples

**Description** — three fixed blocks in this order, no links and no
subscribe/like call-to-action:
```
[1-2 sentence hook + 3-5 key points summarizing what the viewer learns]

Timestamps:
0:00 Introduction
[MM:SS] [Chapter title from transcript topic shifts]
[MM:SS] [Chapter title]
...

#Hashtag1 #Hashtag2 ... (5-10 relevant hashtags)
```

Chapters must start at 0:00, have at least 3 entries, and each be at least 10
seconds apart. Ground every non-zero timestamp in timestamped transcript/audio
evidence and verify it against the final rendered timeline. When Step 0 ran,
`build_edl.py`'s `chapter_seed_starts` are candidates, not proof of a topic
change. Never estimate chapter times from prose or duration. Write this same
three-block structure in the localized description below (a natural translation,
not machine-literal).

**Tags** (5-12 relevant keywords as comma-separated list, include both languages)

**Thumbnail hook text** (3–4 words; 5 as absolute ceiling):
- Complement the title — title carries the searchable what; thumbnail text adds the when, how, or scale
- Use specific, verifiable hooks; ban shock-bait phrases (GAME CHANGER, MIND BLOWN, SHOCKING, INSANE, UNBELIEVABLE)
- Compliant examples: `In 15 Min`, `Step by Step`, `2x Faster`, `Worth It?`, `7 Plugins`, `Free Tool`, `15분 완성`, `실제 사용`
- Review EN/KO titles with the rendered thumbnail: both must package the same
  video and the thumbnail must add a complementary fact. For an explicit
  no-custom-thumbnail exception, record `N/A — <reason>`; missing rendered
  proof is not a pass.

**Localized metadata** (in the other language):

Generate a localized title and description for the alternate language. YouTube
displays these automatically to viewers whose language preference matches.
- If spoken language is `en`: generate `ko` localized title + description
- If spoken language is `ko`: generate `en` localized title + description
- The localized description should be a natural translation, not a machine-literal one

Save both primary and localized metadata for use in Steps 4 and 4.5.

If the user provided `--title`, `--description`, `--thumbnail-text`,
`--localize-ko`, or `--localize-en` overrides, use those instead of generating.

### 3. Generate thumbnail

Generate and show a 1280x720 JPEG for review before uploading. Use graph-view unless `--no-graph-background` is specified or no graph image is supplied; face-only still requires `assets/face.png`. If unavailable, report the missing prerequisite, retain prepared artifacts, and stop before upload/OAuth/vault effects. Only an already explicit no-custom-thumbnail request may continue; record `Thumbnail: N/A — <reason>` and no rendered proof. Read `references/thumbnail-workflow.md` for commands, layout, font verification, and review details.

### 3.5. Validate (pre-upload gate)

Run the validation gate on the transcript + generated metadata BEFORE uploading.
This protects against accidental disclosure of internal info (director/colleague
mentions, product criticism, operational numbers) defined in
`references/upload-policy.md`. It uses the already-authenticated non-Anthropic
GJC CLI route (`openai-codex/gpt-5.6-sol` by default); no Anthropic key is
required or supported.

```bash
# Persist metadata for the validator.
cat > /tmp/yt_validate_metadata.json << METADATA_EOF
{"title": "<title>", "description": "<description>", "tags": "<tag1,tag2,...>"}
METADATA_EOF

# Persist transcript (avoids ARG_MAX on long videos).
cat > /tmp/yt_validate_transcript.txt << 'TRANSCRIPT_EOF'
<transcript_text>
TRANSCRIPT_EOF

uv run "${SKILL_DIR}/scripts/validate.py" \
  --transcript /tmp/yt_validate_transcript.txt \
  --metadata /tmp/yt_validate_metadata.json \
  > /tmp/yt_validate_report.json
VALIDATE_EXIT=$?
```

The script writes a JSON report to stdout. Its exact shape, the digest binding, and the
fail-closed evidence rules are in `references/upload-policy.md`.

**Exit and branching rule**:

- Exit `0` with `passed: true` → continue to final artifact review.
- Exit `2` with a completed, evidence-bound violation report → **stop before
  upload**, correct the inputs, and run a fresh review.
- Exit `1` or any `error` field → **stop before upload** and surface the
  sanitized error.

For new uploads, both nonzero exits block before credentials are loaded or any
YouTube mutation. Text updates may authenticate and read current metadata before
their gate, but both nonzero exits still block every YouTube mutation. Never
reinterpret either as permission to upload privately.

Save the successful report path for the final artifact and Step 6 validation
receipt. On exit 1 or 2, preserve the stopped-state report outside the vault and
perform no upload, update, or tracking-note mutation.

### 3.75. Final SARI artifact review

Assemble a durable final-review artifact containing:

- input classification and the exact final master identity;
- editing, audio-processing, and color evidence, or a justified skip for each;
- audio-grounded transcript correction evidence;
- final-timeline chapter anchors;
- EN/KO title plus rendered-thumbnail complement review, or `N/A — <reason>` for
  an already explicit no-custom-thumbnail exception;
- semantic validation digest and `review` identity;
- ffprobe output and representative frame samples with their timestamps.

Frame samples prove only the sampled moments: state their timestamp coverage and
do not claim full-video visual review. A separate SARI reviewer must inspect the
actual final master and packaging artifact and return an explicit
`FINAL SARI: APPROVED` receipt bound to that artifact. Worker self-report,
partial frame inspection, or an approval for an earlier render is insufficient.
Any `REVISE`, missing receipt, or artifact mismatch stops before Step 4. This
approval is required even when the intended visibility is private.

### 4. Upload

Three paths, by intent:
- **Publish (primary)** — a new upload. This is the default and the dominant
  case; run the command below.
- **Update (secondary)** — swap thumbnail / description / metadata on an
  existing video with `upload.py --update <video_id>` (title/description/tags).
  Use this when the footage is unchanged and only metadata or the thumbnail
  changes — no new video_id, views preserved.
- **Delete + new upload** — YouTube cannot replace a video's file, so a re-edit
  ships only as delete-old + upload-new, which mints a **new video_id/URL and
  resets views/comments**. This is destructive and irreversible: do it **only on
  an explicit user confirmation**, never automatically. On a real re-upload,
  update the vault note's `video_id`, `source`, and `image` fields to the new
  video.

```bash
# upload.py independently validates the exact outgoing metadata before loading
# credentials. Privacy defaults to private after that review succeeds.
uv run "${SKILL_DIR}/scripts/upload.py" '<mp4_path>' \
  --transcript /tmp/yt_validate_transcript.txt \
  --title "<title>" \
  --description "<description>" \
  --tags "<tag1,tag2,...>" \
  --privacy "<private|unlisted|public>" \
  --language "<spoken_language_code>" \
  --thumbnail /tmp/yt_thumbnail.jpg
```

`--transcript <path|->` is mandatory for every new upload. The uploader binds
the complete transcript to the exact normalized outgoing title, description,
tags, and any localizations, and runs validation before credential loading.
Exit 1 or 2 aborts without upload. The default privacy is `private`; explicit
`unlisted` or `public` applies only after validation and the separate manual
SARI approval both succeed.

The `--language` flag sets both `snippet.defaultLanguage` and
`snippet.defaultAudioLanguage` on YouTube. This tells YouTube what language the
video is spoken in, which is required for auto-dubbing to activate.

This outputs JSON to stdout:
```json
{"video_id": "abc123", "youtube_url": "https://www.youtube.com/watch?v=abc123"}
```

Parse and save `video_id` and `youtube_url`.

If upload.py exits with error about missing credentials, tell the user:
"Run `python3 ${SKILL_DIR}/scripts/upload.py --auth-only` to set up YouTube OAuth
credentials first."

Include `--thumbnail /tmp/yt_thumbnail.jpg` by default. Omit it only for an already explicit user-requested no-custom-thumbnail exception, recording `N/A — <reason>`; missing face alone stops upload and retains artifacts. Omission never bypasses semantic validation, artifact-bound SARI, or separate OAuth/upload/vault effects.

### 4.5. Language & Localization

After upload, set the English/Korean localized metadata by default. When `--subs` is given or the user requests a global audience, use the multilingual localization flow; read `references/multilingual.md` for language selection, fragment generation, validation, application, and the auto-dubbing reminder. Require `--transcript` for every policy-relevant update and stop on either nonzero validation exit.

### 4.6. Multilingual subtitle (caption) tracks

When subtitles are requested, generate cleaned, timestamp-aligned translated SRT tracks and upload and verify them. Read `references/multilingual.md` for the language set, translation rules, caption command, and verification.

### 5. Check for duplicates

```bash
obsidian search vault=Ataraxia query="video_id: <video_id>"
```

If a note already exists with this video_id, warn the user and skip note
creation. Report the existing note path.

### 5.5. Generate Feedback section

Generate Feedback only after the duplicate check. Save the rendered markdown from `### English` through the end of `### Action Items` to `/tmp/yt_upload_feedback.md`; read `references/feedback-generation.md` for the language branch, required structure, templates, and field rules.

### 6. Create vault note

Reach this step only after semantic validation passed and Step 5.5 wrote a non-empty `/tmp/yt_upload_feedback.md`. Assemble the note at `15. Work/02 Area/Youtube/<title>.md` with `## Feedback` above `## Transcript`, then set the frontmatter properties. Create and mutate the note through `obsidian create` and `obsidian property:set` via Bash, never the Edit or Write tools. Read `references/vault-note-write.md` for the assembly commands, the full property list, and the re-upload update path.

### 7. Confirm

Report to the user:
- Video uploaded: `<youtube_url>`
- Privacy: `<privacy_status>` (default private, or the explicitly requested value)
- Validation: `passed` with digest and response identity; otherwise report the
  stopped state and do not claim an upload
- Language: `<spoken_language>` (defaultAudioLanguage set)
- Transcript: corrected (or `--no-correct` if skipped)
- Localizations: `<list of locale codes set, e.g., en + ko>`
- Subtitles: `<list of caption languages uploaded, or "none">`
- Thumbnail: reviewed graph view / face-only, or `N/A — <reason>` for an
  explicit user-requested no-custom-thumbnail exception; missing `face.png`
  reports a stopped prerequisite and retained artifacts
- Vault note: `15. Work/02 Area/Youtube/<title>.md`
- MoC tracking: visible in 📚 802 Youtube
- Auto-dubbing: remind if not previously mentioned

## Do NOT

- Edit existing uploaded videos outside the maintenance runbook (`## Existing
  uploaded video metadata maintenance`) — metadata/localization/caption updates
  go through that runbook; ad-hoc edits to published videos are off-limits
- Handle YouTube Shorts (blog-writer's domain)
- Treat validator exit 1 or exit 2 as permission to upload privately
- Treat default-private behavior as a validation fallback; it applies only
  after semantic validation passes
- Use Edit or Write tools on files in `80. References/` (hooks may block; use `obsidian create`/`obsidian property:set` instead)
- Import `_get_credentials()` from blog-writer (hardcoded TOKEN_PATH)
- Pass mp4 directly to mlx-audio transcribe.py (will fail with miniaudio DecodeError)

## Common Rationalizations


| Rationalization | Reality |
|---|---|
| "The auto-generated thumbnail is fine." | The default path requires a reviewed custom thumbnail; a prior explicit no-custom-thumbnail exception must be reported as `N/A` with its reason. |
| "I'll add the thumbnail later." | The pipeline requires the reviewed thumbnail before upload; only a prior explicit exception may omit it, with no rendered-proof claim. |
| "The hook text doesn't matter much." | The hook text is 70-80% of what makes someone click. 3-5 power words that trigger curiosity are non-negotiable. |
| "A simple one-line description is enough." | Descriptions with a hook, key points, timestamps, and hashtags rank dramatically better in YouTube search. The extra 30 seconds of generation saves hours of obscurity. |
| "I'll cut all the silences with one big `select='between(...)+...'` expression." | A select expression past ~130 terms fails at filter init with `Cannot allocate memory`. Build the cut as a `split/trim/concat` filtergraph (`build_edl.py`) — it scales to hundreds of segments. |
| "Cutting at the silencedetect edge (or the whisper word-start) is precise enough." | Both can land inside a phoneme — silencedetect edges sit on the speech ramp, and whisper word boundaries drift ±100-200 ms — so splices clip syllables and sound like a mid-word cut. Energy-snap every boundary to the local audio minimum (`build_edl.py` does this) so a splice always lands in a real gap. |
| "Every phone recording should be tone-mapped." | Exact BT.709 SDR must pass through without tone mapping. Only verified HLG BT.2020 uses the `zscale→tonemap→zscale=bt709` chain; unknown, inconsistent, and PQ sources stop pending source verification. |
| "A few clean frame samples prove the whole video is good." | Samples prove only their timestamps. State coverage limits, verify audio/timeline invariants separately, and require the final SARI artifact approval. |
| "I can skip chapters/timestamps." | YouTube uses chapters for search indexing and video navigation. Skipping them means losing free SEO and worse viewer retention. |
| "Localization isn't worth the effort for a small channel." | YouTube serves localized titles/descriptions to viewers in their language preference automatically. A Korean viewer sees the Korean title; an English viewer sees the English one. This is free discoverability in two markets with zero extra distribution effort. |
| "I'll set the language later in YouTube Studio." | Setting `defaultAudioLanguage` at upload time is the trigger for auto-dubbing eligibility. Doing it later means the video misses the initial recommendation window when YouTube's algorithm pushes new uploads. |
| "The raw transcript is good enough to publish." | ASR output is full of "the the", "I I", and false starts — sometimes a phrase loops 50× in one segment. It reads badly in the note and is worse as a subtitle. Cleaning it is a 30-second editing pass that every downstream artifact depends on. |
| "I'll just paste the multilingual localizations JSON on the command line." | One unescaped `"` inside a translated string silently breaks the entire upload, and translators routinely rewrite the chapter timestamps into prose, killing your chapter markers. Use `build_localizations.py` with fragment files — it hard-fails on both before anything ships. |
| "Auto-dubbing will handle other languages, so I don't need subtitle tracks." | Auto-dubbing is opt-in, UI-only, and not available for every video or language. Uploaded caption tracks work everywhere immediately, are indexed for search, and serve deaf/hard-of-hearing viewers. They're complementary, not redundant. |


## Red Flags


- Upload skipped Step 3.5 validation
- Upload proceeded after validator exit 1 or malformed/missing evidence
- Upload proceeded at any privacy after validator exit 2
- Final master uploaded without an artifact-bound `FINAL SARI: APPROVED` receipt
- Default-path upload completes without a reviewed custom thumbnail, or an
  explicit exception is missing its `N/A` reason
- Hook text repeats the full title instead of complementing it
- Hook text is longer than 5 words
- Description has no timestamps/chapters section
- Description has no hashtags
- Description carries a links block or a subscribe/like call-to-action (the
  template is hook+summary / chapters / hashtags only)
- A Step 0 dead-air cut built as a giant `select='between(...)+...'` expression
  instead of a `split/trim/concat` filtergraph
- A cut boundary that lands mid-word because the splice was not energy-snapped
  to a silent instant
- BT.709 SDR was tone-mapped, HLG BT.2020 omitted the verified conversion chain,
  or unknown/PQ color metadata was guessed
- A re-edit shipped as delete + new upload without an explicit user confirmation
  (mints a new video_id and resets views)
- Missing `assets/face.png` is treated as permission to continue without a
  thumbnail, a stopped run discards artifacts, or an exception is presented as
  rendered proof/bypasses semantic, SARI, or effect authority
- Vault note created in `80. References/` instead of `15. Work/02 Area/Youtube/`
- Transcript step skips ffmpeg extraction and fails on mp4 format
- Upload completes without `defaultAudioLanguage` set
- No localized metadata added (missing Korean or English localization)
- Language auto-detected as wrong language and not corrected
- Raw, uncorrected transcript (stutters/loops) used in the note or subtitles
- Multilingual localizations assembled as a raw CLI string instead of via
  `build_localizations.py` + `--localizations-file`
- Translated subtitle track has a different cue count than `<spoken_lang>.srt` (timing drift)
- Vault note created without a `## Feedback` section
- Paraphrase or Corrections lists use flat bullets instead of nested ones
- `## Transcript` appears above `## Feedback` in the vault note


## Verification


After completing the skill's process, confirm:
- [ ] Step 3.5 validation ran and produced /tmp/yt_validate_report.json
- [ ] Exit 0/1/2 was handled as pass / stop / stop respectively
- [ ] No OAuth/API/upload mutation occurred after exit 1 or 2
- [ ] Validation report has the input digest and completed response identity
- [ ] Final artifact has a matching `FINAL SARI: APPROVED` receipt
- [ ] Input is explicitly classified raw or finished with inspected evidence
- [ ] Editing, audio, and color stages have evidence or justified skips
- [ ] Audio was extracted from mp4 via ffmpeg before transcription
- [ ] Transcript was captured and parsed successfully
- [ ] Metadata includes title, description (with chapters/timestamps), tags, and hook text
- [ ] Description has timestamps starting at 0:00 with at least 3 chapters
- [ ] Description includes hashtags (5-10)
- [ ] Default path created and showed /tmp/yt_thumbnail.jpg (1280x720 JPEG);
      an explicit exception is `N/A — <reason>`
- [ ] Missing face asset or absent exception stopped upload and retained artifacts
- [ ] Video was uploaded and video_id was returned
- [ ] Custom thumbnail was set on YouTube, or explicit `N/A` was reported
      without claiming rendered proof
- [ ] Duplicate check passed (no existing note with same video_id)
- [ ] Vault note created at `15. Work/02 Area/Youtube/`
- [ ] Language was set via `--language` or auto-detected from transcript
- [ ] `defaultAudioLanguage` and `defaultLanguage` were set on YouTube
- [ ] Localized title/description added for the alternate language (en↔ko)
- [ ] Transcript was corrected (stutters/loops removed) unless `--no-correct`
- [ ] Material transcript corrections were checked against audio
- [ ] Chapter times were verified against the final timeline
- [ ] EN/KO titles and rendered thumbnail passed the complementary packaging
      rubric, or the explicit no-thumbnail exception is `N/A` with its reason
- [ ] Semantic validation, artifact-bound SARI, and separate
      OAuth/upload/vault effect authority remained binding on every branch
- [ ] Frame-sample timestamps and coverage limitations are stated
- [ ] Multilingual localizations validated via `build_localizations.py` (titles
      within length limits, chapter timestamps preserved) when more than en↔ko
- [ ] Subtitle tracks uploaded for each requested language and verified via
      `subtitle.py --list` (or subtitles explicitly skipped)
- [ ] Auto-dubbing reminder shown to user (first upload or explicit --language)
- [ ] Frontmatter is complete (type, video_id, source, date_published, duration_seconds, language, status, tags, title, description, image)
- [ ] Feedback section was generated in Step 5.5
- [ ] Vault note has `## Feedback` BEFORE `## Transcript`
- [ ] English section has all 4 H4 subsections: 잘한 점 / 아쉬운 점 / Paraphrase 추천 / 영어 표현 교정
- [ ] Paraphrase entries follow `원문 / 대안1 / (대안2) / 왜` nested bullet shape
- [ ] Corrections entries follow `"wrong" → "right" / 이유` nested bullet shape

## First-time setup

Read `references/first-time-setup.md` before configuring the YouTube upload environment or OAuth credentials.

## Caveats

Read `references/caveats.md` when troubleshooting a failure or comparing against the successful-run console output.

## Existing uploaded video metadata maintenance

For descriptions, titles, localizations, captions, or dubbing support on already-published own-channel videos, read `references/existing-video-description-refresh.md` before acting.
