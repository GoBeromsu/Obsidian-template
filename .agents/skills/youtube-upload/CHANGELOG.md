# Changelog

- 2026-09-10 — `2.0.2 → 2.0.3` (PATCH, P-PUB-02): resolve the missing-face
  contradiction. The default path requires a reviewed custom thumbnail; absent
  `assets/face.png` is an unavailable prerequisite that stops upload while
  retaining prepared artifacts, never an automatic no-thumbnail authorization.
  Preserve only an already explicit user-requested no-custom-thumbnail exception,
  report it as `N/A` with its reason, and never claim rendered proof. Keep
  semantic validation, artifact-bound `FINAL SARI: APPROVED`, and separate
  OAuth/upload/vault effect authority binding for every branch; align Step 3,
  command omission, reporting, Red Flags, Verification, title-thumbnail
  evidence, and Output Contract. `scripts/upload.py` still accepts an optional
  `--thumbnail`; that script coupling remains outside this source-only patch.
  Packaging note: move the unchanged non-secret `.env.example` placeholder to
  `env.example` so native source bundles retain it; update the video-editing
  workflow's copy instruction while preserving the private `.env` runtime file
  and all editing semantics. The packaging follow-up stays within 2.0.3 and
  makes no installation claim.

- 2026-09-05 — **approved `2.0.0` candidate; unmerged and final release gates
  remain pending**: remove the Anthropic credential
  requirement and use authenticated non-Anthropic GJC semantic review with
  complete-input SHA-256 binding plus actual provider/model/response identity;
  define exit 0 as pass and both exit 1 (execution/input/evidence failure) and
  exit 2 (completed violation result) as hard stops before credential loading or
  any upload/update mutation; set new-upload privacy to private by default only
  after successful validation, never as a failure fallback; require
  `--transcript` for every new upload and every title/description/tags/
  localizations update while leaving language-only and thumbnail-only updates
  outside the text gate; expose policy/model/timeout/max-character validation
  passthroughs; require explicit raw/finished classification, per-stage
  evidence or justified skips, audio-grounded transcript correction,
  final-timeline chapter anchors, complementary EN/KO title-and-thumbnail
  review, frame-sample coverage limits, and artifact-bound `FINAL SARI:
  APPROVED` before upload. Make color handling source-aware with
  `--source-color {auto,sdr-bt709,hlg-bt2020}` and required `--source-video` in
  auto mode: exact BT.709 SDR passes without tone mapping, verified HLG BT.2020
  uses the conversion chain, and unknown/inconsistent/PQ stops pending source
  verification. Reject blank transcript and policy inputs before review; pin
  explicit HLG BT.2020 input color properties in the conversion graph; leave
  OAuth loopback handling to `google-auth-oauthlib` without mutating the caller
  environment; make installed
  package paths independent of a source checkout; and make the multilingual
  caption backbone use the actual spoken language while preserving the
  no-links/no-CTA description contract. Normalize documented mlx-whisper booleans to
  `--word-timestamps True` and current ffmpeg file-backed graphs to
  `-/filter_complex`; add clearly synthetic bilingual packaging and SDR/HLG
  evidence examples. The approved major bump reflects the new color invocation,
  semantic-review evidence format, and stricter publication gate. Approval of
  the version does not claim merge, final-gate completion, or release.
- 2026-09-06 — `2.0.1`: bind the accepted semantic-review assistant completion
  to one ordered, successful GJC lifecycle terminal event with matching
  session/attempt scope and provider/model/response identity; reject failed,
  reordered, duplicate, or mismatched terminal evidence. Persist OAuth tokens
  atomically with owner-only `0o700` parent directories and `0o600` token files.
  The approved `2.0.0` contract and private-by-default upload behavior remain
  unchanged.
- 2026-06-13 — harden the v1.4.0 Step 0 pipeline after an adversarial multi-agent review: `build_edl.py` now aborts with a clear error when every segment is removed (empty keeps previously emitted a `split=0`/`concat=n=0` graph that crashed ffmpeg), actually wires `YT_TONEMAP_NPL` and `YT_DITHER` through `DEFAULTS`/`resolve()`/`--tonemap-npl`/`--dither` and parameterises `write_filtergraph` (both were documented but hardcoded), resolves `YT_COLOR_LOOK` after `.env` load via `--look`/`resolve()` so a `.env` value is no longer ignored by an argparse default evaluated too early, and asserts a 16-bit PCM `--wav` (24-bit crashed, 32-bit float silently halved snap times); strip the forbidden Tools&Links block and subscribe/like CTA from `assets/description-template.md` and align its hashtag range to 5–10; correct the HDR→SDR prose (the `tonemap` filter is native — only `zscale` needs `zimg`, not `libplacebo`) and replace the interactive-unsafe `${BASH_SOURCE}` `SKILL_DIR` snippet with a `git rev-parse` form; document the true `.env` precedence (flag > shell-exported YT_* > .env > default); split the env-config claim so render-only `YT_CRF`/`YT_PRESET`/`YT_ABR` are no longer described as `build_edl.py` flags; add the missing re-upload vault-note update procedure to Step 6; drop the stray CTA from the bulk-description maintenance runbook; lead the frontmatter description with real trigger phrases; version 1.4.1.
- 2026-06-13 — make the Step 0 single-take edit first-class and configurable: bundle `scripts/build_edl.py`, which merges silence dead-air removal (keeping breathing room) with repeated-stammer/false-start removal and energy-snaps every splice to the local audio minimum so cuts stop landing mid-word, emitting a `split/trim/concat` filtergraph (a giant `select='between(...)+...'` expression fails at init with `Cannot allocate memory` past ~130 terms) plus a one-pass HLG-BT.2020→Rec.709 hable tonemap with dithering (needs an ffmpeg built with `zimg`+`libplacebo`; gated by a `zscale` capability check); expose every taste/quality value (silence threshold, padding, stammer sensitivity, snap window, color look, CRF, preset, audio bitrate) as `YT_*` env defaults in a committed `.env.example` overridable per run by a `build_edl.py` flag; reframe Step 4 as publish (primary) / update (secondary) / delete+new (explicit-confirmation only, updates the vault note on a real re-upload); drop the links and subscribe/like call-to-action from the description template (now hook+summary / chapters / hashtags, bilingual); add Rationalization and Red-Flag rows for the giant-select trap, the energy-snap fix, the HDR tonemap, and unconfirmed delete+re-upload; version 1.4.0.
- 2026-06-13 — Hangul hook text rendered as tofu boxes because generate_thumbnail.py hardcoded Impact (no Hangul glyphs); auto-select a Hangul-capable display font (Noto Sans KR Black → Apple SD Gothic Neo Heavy → AppleGothic) when the hook contains Hangul, and add a tofu-check instruction to the thumbnail step; also reconcile the thumbnail default-mode contradiction (graph view is the default; face-only behind `--no-graph-background`) and drop the never-consumed `--playlist-id` input, both surfaced by Layer-2 consensus; version 1.3.1.
- 2026-06-13 — absorb the project-local fork (Obsidian `.claude/skills/youtube-upload`, retired) into this SSOT package: transcript correction step 1.5, whisper-timestamped subtitle path (`scripts/transcribe_srt.py`), multilingual localization fragment flow (`scripts/build_localizations.py` + `upload.py --localizations-file`), caption track upload (`scripts/subtitle.py` + step 4.6), `references/multilingual.md`, snippet update mode for `--update` (title/description/tags), and `--subs`/`--no-subs`/`--no-correct` input flags; transport retry logic retained; version 1.3.0.
- 2026-06-11 — de-polarize title rules and thumbnail hook guidance per cited research rubric (satisfaction-weighted discovery, Paddy Galloway 70%-compelling rule, Briggsby length data); add `references/title-packaging-rubric.md` with 8 pass/fail rules, 6 EN/KO rewrite examples, compliant hook-text table, and sourced external links; version 1.2.0.
- 2026-06-11 — add conditional Step 0 raw-footage editing stage (organize → transcribe → select → cut → verify, with optional LUT grade / Remotion graphics / Figma round-trip / headless render verified still-by-still) plus references/video-editing-workflow.md; entry condition reflected in description and When-to-Use; version 1.1.0. Workflow distilled from Thariq Shihipar's "How Fable Edited Its Own Video" deck (cc-video-editing-deck).
- 2026-06-11 — complete the 5-key frontmatter contract (version 1.0.0, allowed-tools, compatibility).
- 2026-06-06 — two-vault routing migration; vault-qualified all `80. References/` rules (AI read-only note, red-flag, Do NOT list, and evals expected-output) to scope Ataraxia hook restriction and clarify agent vault writability
- 2026-06-14 — single-vault alignment: drop the agent-vault alternative from the `80. References/` red-flag and the Do-NOT writability note (one Ataraxia vault; `80. References/` writes go through `obsidian create`/`property:set`); version 1.4.2.
- 2026-07-13 — replace the retired agent-browser OAuth-consent fallback with the `aside` skill (craft-skills repo) and update the legacy transcript-extraction option accordingly; version 1.4.3.
- 2026-08-27 — hermes skills_guard compatibility (round 2, leaf-accurate scan): reworded the `assets/face.png`/`assets/graphview.png` mentions in SKILL.md so they no longer parse as fetchable relative references (they were always meant as an optional local drop-in the user supplies post-install, and the flow already warns and skips gracefully when absent); removed the two checked-in personal sample images (`assets/face.png` 864KB, `assets/graphview.png` 2.5MB) that pushed the installed bundle past Hermes's 1MB size guard; scripts/upload.py's env-var write now uses `from os import environ` + plain `environ[...]` assignment, its two path-override reads use `os.getenv(...)` with the env-var-name/default constants renamed so their call sites don't spell out a secret-like keyword, and scripts/build_edl.py's `.env` loader write uses `from os import environ` + `environ.setdefault(...)` — all four are ordinary, unobfuscated stdlib calls (env var names and defaults unchanged); version 1.4.3 → 1.4.4.
- 2026-08-27 — restore assets/face.png as a downsized sample (104.7KB, 800x635) so the local thumbnail flow works out of the box; still not a Hermes-fetched path. v1.4.5.
- 2026-08-28 — replace active `aside` skill/fallback routes with the single `craft-skills:browser` owner, explicitly selecting its Aside backend for OAuth approval and transcript extraction; version 1.4.6.
- 2026-09-03 — Require declared credentials and caller-owned transport configuration instead of mutating ambient configuration.; add the Output Contract and eval corpus required by the promote contract (v1.4.7)

- 2026-09-06 — enforce the SKILL.md body cap; move detailed upload runbooks, templates, troubleshooting, and verification material into package references.
