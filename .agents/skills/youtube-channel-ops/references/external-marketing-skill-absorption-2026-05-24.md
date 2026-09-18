# External marketing skill absorption — 2026-05-24

Purpose: absorb the useful parts of the three repositories Beomsu surfaced into `youtube-channel-ops` without making `SKILL.md` bulky or importing unsafe/unverified behavior.

## Reviewed sources

### 1. `adityaarsharma/youtube-marketing-skills`

- Origin: https://github.com/adityaarsharma/youtube-marketing-skills
- Local review path: `/tmp/youtube-skill-repos/youtube-marketing-skills`
- Reviewed commit: `d1391c1`
- Shape: agent-oriented YouTube growth command suite with 21 sub-skills and 9 references.

Relevant sub-skills reviewed:

- `analyze.md` — channel/video analysis framing.
- `audit.md` — channel audit framing.
- `strategy.md` — strategic recommendation format.
- `ideate.md` — idea scoring using top videos, traffic sources, SERP gap, volume, differentiation.
- `competitor.md` — SERP competitor map, keyword gap, format gap, title/hook pattern analysis.
- `comment-intel.md` — comments as feature requests, pain points, FAQ, competitor mentions, conversion signals.
- `hook.md` / `script.md` — hook and retention-aware script structure.
- `thumbnail.md` — 3 A/B thumbnail brief archetypes and title-thumbnail synergy.
- `seo.md` / `metadata.md` — title, description, tag, hashtag, chapter metadata QA.
- `shorts-from-long.md` / `shorts.md` — extracting Shorts moments from long-form.

Useful patterns absorbed:

- Treat analysis as modules: audit → retention → traffic/discovery → packaging → comments → competitors → experiments.
- Idea scoring should combine channel momentum, search/SERP demand, differentiation, and fit with Beomsu's strategic narrative.
- Separate `high retention + low views` from `high views + low retention` because they imply opposite fixes.
- Use comments as natural-language search-intent data, not merely engagement numbers.
- For thumbnail/title, generate multiple variants with different jobs: result showcase, before/after, bold claim/problem.
- For scripts, diagnose the first 28-42 seconds and add pattern interrupts every 60-90 seconds for long tutorials.
- For Shorts, only extract self-contained result/wow/tip moments; do not use Shorts metrics as proof that long-form is healthy.

Rejected or downgraded:

- Do not require DataForSEO MCP as a hard dependency; Beomsu's current channel analysis should work with YouTube OAuth + Ataraxia first.
- Do not copy WordPress/Elementor-specific assumptions into Beomsu's Obsidian/AI-agent channel.
- Treat upstream benchmark claims as heuristic defaults unless verified against Beomsu's own Analytics or Studio export.
- Do not include bulk metadata-writing flows in channel analysis unless Beomsu explicitly asks to change published videos.

Where absorbed:

- `references/marketing-strategy-and-packaging.md`
- `references/growth-and-packaging-rubric.md`
- `scripts/analyze_youtube_channel.py` derived `diagnosis_buckets`

### 2. `Pratham-Prog861/viral-youtube-optimizer-ai`

- Origin: https://github.com/Pratham-Prog861/viral-youtube-optimizer-ai
- Local review path: `/tmp/youtube-skill-repos/viral-youtube-optimizer-ai`
- Reviewed commit: `3f87311`
- Shape: Gemini-powered URL/channel optimizer that returns JSON suggestions for titles, descriptions, thumbnails, and banner concepts.

Useful patterns absorbed:

- Strict grounding before creative suggestions: verify exact video title, channel, transcript/description, and current thumbnail before proposing assets.
- Packaging refresh must explicitly critique the current thumbnail/title before proposing alternatives.
- Output should be structured JSON or compact sections so downstream agents can compare variants.
- Thumbnail concepts should be visually distinct, not three wording variations of the same idea.
- Preserve source links/citations when a web/search model is used.

Rejected or downgraded:

- Do not let a model guess video contents from URL alone.
- Do not treat "viral" wording as evidence of likely performance.
- Do not generate image assets unless Beomsu explicitly asks; for analysis, generate briefs/specs only.
- Avoid face-heavy or MrBeast-style assumptions unless the actual channel brand supports it.

Where absorbed:

- `references/marketing-strategy-and-packaging.md` packaging-refresh workflow.
- `references/transcript-and-qualitative-analysis.md` grounding requirement.

### 3. `Avinashricky211/Advanced-Youtube-Seo-Generator-2.0`

- Origin: https://github.com/Avinashricky211/Advanced-Youtube-Seo-Generator-2.0
- Local review path: `/tmp/youtube-skill-repos/Advanced-Youtube-Seo-Generator-2.0`
- Reviewed commit: `18df527`
- Shape: Python SEO generator using YouTube Data API, NLTK, spaCy, TextBlob, and random title/description/tag generation.

Useful patterns absorbed:

- Use Data API to collect top videos for a query before writing SEO metadata.
- Extract common words/phrases from successful titles/descriptions as a keyword proxy.
- Keep title length under roughly 70 characters.
- Treat description length, tag count, and hashtag count as metadata QA checks.
- Include tags/hashtags as support signals, not the main strategy.

Rejected or downgraded:

- Do not hard-code API keys in scripts.
- Do not use random emotional trigger words as final titles.
- Do not use mock analytics as if they are metrics.
- Do not require heavy NLP dependencies for the core skill; the current analyzer should remain lightweight.
- Do not run interactive scripts in agent workflows when deterministic JSON output is better.

Where absorbed:

- `references/marketing-strategy-and-packaging.md` SEO QA section.
- Potential future script: metadata audit only, never mock analytics.

## Final integration decision

`youtube-channel-ops` remains API-grounded and Beomsu-specific:

1. Use YouTube Data API + Analytics API + Ataraxia as the ground truth.
2. Use external marketing repos as strategic rubrics, not as unverified data sources.
3. Keep heavy frameworks in `references/`; keep `SKILL.md` as a routing/runbook layer.
4. Add only deterministic helper logic to scripts.
5. Never mutate live YouTube metadata during analysis unless Beomsu explicitly requests a publish/update action.
