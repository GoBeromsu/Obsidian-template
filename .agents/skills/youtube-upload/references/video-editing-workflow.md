# Video editing workflow (raw footage → edited master)

Use this reference when the upload input is unedited recording material —
multiple takes across scenes, a folder of clips, or a single raw take with
warm-ups, filler words, or dead air. It turns raw footage into the verified
master that Step 1 of the upload pipeline consumes.

Two ground rules hold throughout:

- **The edit is text.** Every artifact — transcripts, the edit decision list,
  LUTs, graphics, timing — lives as a readable, diffable file. Never reach for
  a GUI editor or a timeline; read, edit, and re-render the files instead.
- **Run commands directly; one bundled helper for the dead-air/stammer cut.**
  Multi-take selection, grading, and graphics run as direct commands
  (ffmpeg/ffprobe, mlx-whisper, npx remotion). The single-take dead-air +
  stammer cut is built by `scripts/build_edl.py`, because the cut filtergraph it
  emits is too large and error-prone to hand-write. Do not add other new files
  under `scripts/` for this stage.
- **Tuning lives in `.env`.** Silence threshold, padding, stammer sensitivity,
  energy-snap window, color look, CRF, preset, and audio bitrate are env-var
  defaults (`env.example` committed; copy it to a gitignored `.env`), each
  overridable per run with the matching `build_edl.py` flag.
- **Evidence is per stage.** Classify the input as `raw` or `finished`, then
  record editing, audio-processing, and color evidence or a justified skip for
  each stage. A filename, user label, or worker self-report is not evidence.

The pipeline is input-shape agnostic: one take or N takes across M scenes run
the same steps. With a single take, scene selection collapses to trimming
filler words and silence out of that one take — everything else is unchanged.

## Working directory layout

Create a scratch working directory next to the footage (or under `/tmp`):

```
work/
├── transcripts/*.json    # word timestamps per take — cut points are grepped from these
├── final-edit.json       # the EDL: picks, in/out points, written rationale
├── cuts/                 # per-pick segments + the stitched cut
├── luts/*.cube           # optional: hand-written color LUTs
└── graphics/             # optional: Remotion project (src/, anim.tsx, FinalEdit.tsx)
```

## 1. Organize and probe

1. Inventory every input file. Group takes by scene when a script or naming
   convention reveals scene structure (e.g. consecutive clip IDs per scene);
   with no structure, treat the input as a single scene.
2. Probe each file so cut and render decisions use real numbers:

```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,color_primaries,color_transfer,color_space \
  -of json '<take>.mp4'
```

3. Record per take: duration, resolution, fps, codec, and all three color
   fields. Missing or inconsistent color metadata is `unknown`, not SDR.
4. Read the script (when provided) and map which takes belong to which scene,
   including re-shoots that appear out of order.

## 2. Transcribe every take with word timestamps

Word-level timing is what makes precise cuts possible — every cut point and
overlay cue is grepped out of these JSON files, never scrubbed on a timeline.

Do NOT use `scripts/transcribe.py` here: it emits a plain transcript plus
duration only, with no word timing. Use mlx-whisper directly — it reads video
containers through its ffmpeg backend, so no audio-extraction step is needed
here (unlike mlx-audio in Step 1 of the upload pipeline):

```bash
mlx_whisper '<take>.mp4' --word-timestamps True \
  --output-format json --output-dir work/transcripts
```

Output shape per take (one object per word):

```json
"words": [
  { "word": " Hey",    "start": 1.02, "end": 1.50 },
  { "word": " it's",   "start": 1.90, "end": 2.04 }
]
```

Tolerate transcription errors in proper nouns (a name may transcribe wrong);
the timestamps still land, and timestamps are what the cut needs.

## 3. Select the best takes (subagent per scene)

Spawn one subagent per scene; have verifier passes double-check the picks.
Each subagent:

1. Reads all candidate-take transcripts for its scene.
2. Picks the best take: fewest filler words (ums), complete on-script
   delivery, clean ending. Later takes are often (not always) the best —
   judge from the transcript, never assume.
3. Disqualifies broken takes explicitly (incomplete delivery, long dead
   pauses mid-sentence) and writes the reason down.
4. Chooses cut-in/cut-out timestamps that sit inside silent gaps between
   words — find the gap in the word timestamps and cut there, so no syllable
   is clipped. Cut out warm-up openers (e.g. a spoken "Hey [name]" used to
   start the sentence warm) by locating where the warm-up ends and placing
   the cut-in in the following gap.
5. Records a `selection_rationale` string explaining the pick and the
   rejections — the rationale is part of the edit artifact, not commentary.

## 4. Write the EDL: final-edit.json

The edit decision list is one JSON file. Schema per scene:

```json
{
  "scene": 1,
  "title": "Part 1: Intro",
  "candidate_takes": ["C001", "C002", "C003", "C004", "C017 (re-shoot)"],
  "selection_rationale": "C017 is incomplete — 5.8s dead pause mid-sentence, disqualified. C003 is the cleanest complete take: zero ums, clean ending.",
  "clips": [
    { "clip": "C003", "start": 1.89, "end": 60.81,
      "first_words": "Hey everyone, it's..." }
  ]
}
```

- `start`/`end` are seconds from the word-timestamp gaps chosen in step 3.
- `first_words` anchors each clip for human review and for the verification
  pass in step 5.
- A scene may stitch multiple clips when no single take is fully usable.

## 5. Cut, concat, and verify the cut

One frame-accurate cut per pick, then join:

```bash
# per pick — re-encode for frame accuracy (-c copy snaps to keyframes; do not use it for cuts)
ffmpeg -ss 1.89 -to 60.81 -i 'C003.mp4' 'work/cuts/seg1.mp4'

# then join the picks in scene order
ffmpeg -f concat -safe 0 -i concat.txt -c copy 'work/cuts/stitched.mp4'
```

`concat.txt` lists the segment files in order (`file 'seg1.mp4'` per line).
Segments cut with identical encoding parameters concat cleanly with `-c copy`.

**Verification gate — re-transcribe the cut.** Run mlx-whisper on the
stitched output and check against the EDL:

- each scene begins with its `first_words`
- zero filler words survived at the cut boundaries
- no mid-sentence truncation at any seam

Fix the EDL and re-cut until the re-transcription is clean. Only a verified
stitched cut moves on.

## 5b. Dead-air + stammer cut and source-aware SDR delivery (single take)

A single long take (e.g. a phone-recorded daily log) is tightened by removing
dead air and repeated false-starts, then rendered to the SDR delivery master in
one pass. SDR sources remain SDR without tone mapping; verified HLG sources are
converted. This is where `scripts/build_edl.py` runs.

### Produce the three inputs

```bash
SRC='IMG_0001.MOV'; DUR=$(ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 "$SRC")

# 1) 16 kHz mono PCM — feeds both the ASR and the energy-snap
ffmpeg -y -i "$SRC" -vn -ac 1 -ar 16000 -c:a pcm_s16le take.wav

# 2) silencedetect log (stderr) — the dead-air source
ffmpeg -hide_banner -i take.wav -af silencedetect=noise=-30dB:d=0.5 \
  -f null - 2> silence.txt

# 3) word-timestamp ASR — the stammer source (set --language to the spoken one)
mlx_whisper take.wav --language <spoken_lang> --word-timestamps True \
  --output-format json --output-name words -o .
```

### Build the cut

```bash
# Ask the runtime's local-file reader for the absolute local path of the loaded
# youtube-upload/SKILL.md. Stop if it cannot return a readable path; never infer
# a source checkout or installation layout.
SKILL_FILE="<runtime-resolved path of the loaded youtube-upload/SKILL.md>"
test -f "$SKILL_FILE" || { printf '%s\n' 'ERROR: loaded youtube-upload SKILL.md is unavailable.' >&2; exit 1; }
SKILL_DIR="$(cd -- "$(dirname -- "$SKILL_FILE")" && pwd -P)" || exit 1
test -f "$SKILL_DIR/scripts/build_edl.py" || { printf '%s\n' 'ERROR: loaded youtube-upload scripts are unavailable.' >&2; exit 1; }
python3 "$SKILL_DIR/scripts/build_edl.py" \
  --silence silence.txt --words words.json --wav take.wav \
  --duration "$DUR" --out edit \
  --source-color auto --source-video "$SRC"
# overridable per run, e.g.  --min-silence 1.5  --look mobius
```

`--source-color auto` requires `--source-video`; it probes the actual source.
Use `--source-color sdr-bt709` or `--source-color hlg-bt2020` only after an
independent source check justifies the explicit override.

This writes `edit.json` (keep segments, stats, `chapter_seed_starts` for
description chapters, and the color decision evidence) and `edit.fc` (the
file-backed `-/filter_complex` graph). It merges two
removal sources — silences ≥ `YT_MIN_SILENCE` (keeping `YT_CUT_PAD` of breathing
room each side) and same-token repeats within `YT_STAMMER_GAP` (keeping the last
clean take) — and **energy-snaps every boundary to the local audio minimum**, so
no splice clips a syllable. Pass `--words -` to skip stammer removal (e.g. a
language where word-level repeats are not the disfluency pattern).

The graph is `split/trim/concat`, never a single `select='between(...)+...'`
expression: that fails at filter init with `Cannot allocate memory` past ~130
terms, whereas trim+concat scales to hundreds of segments.

### Render once, with source-aware color handling

Inspect `edit.json.color.path` before rendering:

- `bt709-sdr-passthrough`: exact `bt709/bt709/bt709`; the graph ends with
  `format=yuv420p` and contains no `zscale` or `tonemap`.
- `hlg-bt2020-to-bt709-sdr`: exact
  `bt2020/arib-std-b67/bt2020nc`; the graph uses the verified linear-light
  `zscale → tonemap → zscale=bt709` chain with dithering. For this path only,
  gate on `zscale`:

  ```bash
  ffmpeg -filters | grep -q zscale || { echo "ffmpeg lacks zscale; install:"; \
  echo "  brew install zimg"; \
  echo "  brew uninstall ffmpeg  # clear the core formula-name conflict"; \
  echo "  brew install homebrew-ffmpeg/ffmpeg/ffmpeg --with-zimg"; \
  exit 1; }
  ```
- Missing/inconsistent metadata, an unknown transfer, or PQ (`smpte2084`)
  stops. Do not route PQ through the HLG chain. Re-probe the source, or select
  an explicit supported mode only when external source evidence establishes it.

```bash
ffmpeg -y -i "$SRC" -/filter_complex edit.fc -map '[v]' -map '[a]' \
  -c:v libx264 -crf "${YT_CRF:-16}" -preset "${YT_PRESET:-slow}" \
  -pix_fmt yuv420p -c:a aac -b:a "${YT_ABR:-256k}" -movflags +faststart \
  master.mp4
```

CRF 16 / preset slow keeps quality near-lossless; dithering prevents banding
on the HLG conversion path. `master.mp4` is the edited master — verify it per
step 5's gate, then feed it to Step 1 of the upload pipeline.

### Illustrative color evidence (synthetic, not a real execution)

**Synthetic SDR before:** ffprobe reports
`color_primaries=bt709`, `color_transfer=bt709`, `color_space=bt709`.
**Synthetic SDR after:** `edit.json.color.path=bt709-sdr-passthrough`;
`edit.fc` ends in `format=yuv420p` and has no tone-map filters.

**Synthetic HLG before:** ffprobe reports
`color_primaries=bt2020`, `color_transfer=arib-std-b67`,
`color_space=bt2020nc`. **Synthetic HLG after:**
`edit.json.color.path=hlg-bt2020-to-bt709-sdr`; `edit.fc` contains the verified
HLG linear-light chain and the rendered master probes as BT.709. These examples
illustrate the required receipt shape; they are not proof that any source was
executed or reviewed.

## 6. Optional: color grade with hand-written LUTs

Enter when the footage is log-encoded (e.g. S-Log3 looks flat and washed out)
or the user asks for a grade.

1. Hand-write `.cube` LUT files (plain text) converting the source space to
   Rec.709, in a few candidate looks (e.g. neutral, warm filmic, punchy,
   teal-orange) — no preset packs.
2. Render one still per look and let the user choose:

```bash
ffmpeg -ss 10 -i 'work/cuts/stitched.mp4' -vf lut3d='work/luts/warm_filmic.cube' \
  -frames:v 1 '/tmp/grade_warm_filmic.png'
```

3. Apply the chosen LUT at encode time (`-vf lut3d=...`) — the grade stays
   plain text, applied by ffmpeg, re-runnable.

## 7. Optional: graphics as code (Remotion)

Enter when static design frames (PNGs: title cards, overlays, lower thirds)
need to be animated into the cut.

1. Rebuild each design frame as a Remotion JSX component — every word, color,
   and beat becomes a prop, so design tweaks are one-line prompt changes
   rather than image re-exports.
2. Centralize the feel in one `anim.tsx`: a `TIMING` object (frames at the
   composition fps) with a handful of knobs — element entrance (`reveal`),
   sibling gap (`stagger`), panel slide-in/out (`overlayIn`/`overlayOut`),
   late emphasis (`emphasisDelay`) — plus one easing curve. A few numbers
   drive every animation; "make it snappier" is a one-line change.
3. Time the cue sheet from the transcript, not by scrubbing: grep
   `work/transcripts/` (or the stitched cut's transcript) for the trigger
   phrase and place each overlay's `at`/`dur` on the spoken word:

```js
// FinalEdit.tsx — overlays land on the word
const CUES = [
  { id: 'lower-third', at: 1.2,  dur: 4.5  },  // "…it's [name] from the team"
  { id: 'keypoint',    at: 12.2, dur: 25.6 },  // lands on the key phrase
];
```

4. Verify a cue visually with a single still before rendering anything long:

```bash
npx remotion still src/index.ts <CompositionId> /tmp/cue_check.png --frame=295
```

## 8. Optional: Figma design round-trip

Enter when a design team reviews or revises the graphics.

1. Export the Remotion components to a real Figma file via the Figma MCP —
   components, color variants, and a motion page with rendered GIFs.
2. When the design comes back updated, read the revised Figma file through
   the MCP and rebuild the JSX to match.
3. Code stays the source of truth: the round-trip is code → Figma → code,
   never a Figma file that drifts away from the rendered video.

## 9. Final render with still-by-still verification

1. **Before each full render**, render representative stills at the cue
   frames and inspect them — catch a wrong color, missed beat, or overlapping
   overlay on one frame instead of after a long render.
2. Render headless at delivery resolution and exact fps (match the source,
   e.g. 3840×2160 at 24 fps):

```bash
npx remotion render src/index.ts <CompositionId> out/final.mp4
```

3. Verify the output with ffprobe: duration matches the EDL total, frame
   count equals duration × fps, resolution and fps exact, audio present and
   in sync (spot-check a known word against its timestamp), file size sane.
4. Re-render after every fix; multiple re-renders in a session are normal and
   cheap because the entire edit is text.
5. Record every sampled frame timestamp and what it checks. Frame samples cover
   only those moments; do not claim they establish full-video continuity,
   color, or sync. Re-transcription, seam checks, duration/frame invariants,
   and representative playback provide separate evidence.
6. Assemble the exact master identity, EDL, audio/seam evidence, color receipt,
   transcript corrections, chapter anchors, packaging, and sample-coverage
   statement into the final review artifact. Publishing requires a separate
   artifact-bound `FINAL SARI: APPROVED` receipt; the editing worker cannot
   self-approve.

The verified render (or, without graphics, the verified stitched cut from
step 5 — graded if step 6 ran) is the **edited master**: feed it to Step 1 of
the upload pipeline. Preserve the corrected, audio-grounded transcript as a
file: every new `upload.py` call must receive it via `--transcript <path|->`.
The uploader revalidates that complete transcript against the exact outgoing
metadata before credential loading. Exit 1 (execution/evidence error) and exit
2 (content violations) both stop without upload; default-private visibility is
available only after validation succeeds. The separate manual, artifact-bound
SARI approval remains an additional pre-publish gate and is not implemented by
the uploader.

## Sources

- "How Fable Edited Its Own Video" — Claude Code video-editing deck by
  Thariq Shihipar (Anthropic), June 2026:
  https://thariqs.github.io/cc-video-editing-deck/
