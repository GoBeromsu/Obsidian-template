# Shared/hub skill review for YouTube channel analysis — 2026-05-24

Purpose: decide what to absorb into `youtube-channel-ops` for Beomsu's channel-analysis workflow without bloating `SKILL.md`.

## Skills/resources reviewed

### `youtube-upload`

Useful pieces absorbed:

- `references/youtube-best-practices.md`: retention benchmarks, title/thumbnail/description SEO, tech/developer niche heuristics, 15-factor growth checklist.
- Upload note structure: transcripts and `## Feedback` are valuable qualitative analysis inputs.
- Localization/language metadata is upload-side, not analysis-side, but language split should still be reported.

Decision: do not merge upload operations into channel ops. Keep upload/publish flow in `youtube-upload`; absorb analysis rubric into `growth-and-packaging-rubric.md`.

### `baoyu-youtube-transcript`

Useful pieces absorbed:

- robust input formats for YouTube IDs/URLs
- language-priority transcript fetching
- timestamps, chapters, speaker identification as analysis aids
- caching raw transcript/metadata
- fallback hierarchy: direct transcript API/InnerTube → `yt-dlp` → browser/cookies when needed
- explicit error categories for transcript disabled/private/no language/IP block

Decision: no need to install as a hard dependency for channel analytics. Treat it as a reference pattern; use local/vault transcripts first.

### Hermes bundled `youtube-content` docs

Useful pieces absorbed:

- timestamped transcripts are preferred for chapter/summary/quote work
- chunk long transcripts before summarizing
- retry language fallback when transcript output is empty

Decision: absorb into `transcript-and-qualitative-analysis.md`; not a replacement for Analytics API metrics.

### `browse-sh/youtube.com/extract-transcript-loeude`

Useful pieces absorbed:

- read-only transcript extraction stance
- metadata + transcript + auto-generated/human-authored caption distinction
- API-first with browser fallback framing

Decision: useful for third-party transcript extraction, but not central to Beomsu channel analytics.

### `lobehub/epoch-ai` and `lobehub/youtube-summarizer-pro`

Useful pieces absorbed:

- structured summary/key-point output can help review individual videos.

Rejected for core channel analysis:

- generic video summarization does not answer retention, traffic-source, subscriber-conversion, or packaging questions.
- should not replace API-grounded metrics.

Decision: use only as inspiration for qualitative summaries, not as dependency.

### `adjust-copy-for-platforms`

Useful pieces absorbed:

- platform-tailored copy and truncation-safe leads are useful after strategy decisions.

Decision: out of scope for channel analytics; may inform future title/description repackaging work.

### Beomsu-shared marketing/SEO GitHub repositories

Reviewed after the initial hub scan:

- `adityaarsharma/youtube-marketing-skills`
- `Pratham-Prog861/viral-youtube-optimizer-ai`
- `Avinashricky211/Advanced-Youtube-Seo-Generator-2.0`

Decision: absorb the marketing/branding strategy patterns into `references/marketing-strategy-and-packaging.md` and record source-level decisions in `references/external-marketing-skill-absorption-2026-05-24.md`. Do not import their runtimes as required dependencies; Beomsu's workflow remains Ataraxia + YouTube Data API + YouTube Analytics API first.

## Net changes to `youtube-channel-ops`

- Keep `SKILL.md` as the routing/runbook layer.
- Move bulky analysis, source selection, transcript, and growth heuristics into references.
- Add a durable Analytics API script for channel-wide private metrics.
- Make the final report explicitly distinguish exact API data from proxy keyword/packaging analysis.
