# Marketing strategy and packaging playbook

Use this reference after the core Analytics API snapshot is collected. It turns metrics into marketing/branding decisions for Beomsu's YouTube channel.

This file absorbs the useful strategy patterns from the external repositories Beomsu shared while keeping the runtime workflow grounded in Beomsu's own data.

## Source order

Never start with creative ideas. Start with evidence:

1. YouTube Analytics API: views, watch time, retention, traffic source, subscribers gained.
2. YouTube Data API: current public stats, titles, dates, comments count, thumbnails.
3. Ataraxia uploaded-video notes: transcript, feedback, intent, production context.
4. Optional exports: YouTube Studio CTR/impressions/search-term CSV.
5. Optional external research: YouTube SERP, competitor titles, Google keyword volume, DataForSEO if available.

If a source is missing, label the conclusion as a proxy/hypothesis.

## Strategy modules

### Module A — Channel audit

Inputs:

- `scripts/fetch_youtube_stats.py` public snapshot.
- `scripts/analyze_youtube_channel.py` private Analytics output.
- Ataraxia upload notes when qualitative diagnosis is needed.

Questions:

- Which topics bring views?
- Which topics retain attention?
- Which videos convert subscribers?
- Which traffic source dominates: Search, Browse, Suggested, Shorts, External?
- Does the current audience match the intended brand: Obsidian/PKM + AI agents + builder journey?

Use the script's `derived.diagnosis_buckets`:

- `high_retention_low_views__repackage_or_distribute`: content is probably good; fix title/thumbnail/search framing or distribution.
- `high_views_low_retention__tighten_hook_or_promise`: packaging or keyword pulls clicks, but the video loses people; fix opening promise, pacing, or mismatch.
- `subscriber_efficiency_best__series_candidates`: topics that build audience; make sequels/playlists.
- `engagement_efficiency_best__comment_mining_candidates`: videos where comments may reveal pain points and next ideas.

### Module B — Topic and keyword gap

Use only after channel audit.

Evidence hierarchy:

1. Exact YouTube Studio search terms if exported.
2. Analytics traffic-source rows and title keyword proxy.
3. YouTube SERP for target terms.
4. Competitor title/format patterns.
5. Generic keyword-volume tools.

Opportunity score heuristic:

```text
opportunity =
  channel_momentum        # similar topics already retain or convert
+ search_or_SERP_demand   # target term has visible YouTube demand
+ freshness_gap           # top SERP videos are old or outdated
+ differentiation_gap     # Beomsu can show an Obsidian/AI-agent workflow others cannot
+ production_fit          # can make it with available demos/notes this week
- promise_mismatch_risk   # topic attracts viewers who will not care about the channel's core arc
```

For Beomsu, strong angles usually look like:

- concrete Obsidian workflow before/after
- AI agent actually doing useful work, not abstract agent talk
- local-first/personal operating system angle
- build-in-public lesson from using Hermes/Ataraxia daily
- English/creator practice only when tied to a clear audience problem

### Module C — Packaging refresh

Run this when a video has high retention but low views, or when the user asks about title/thumbnail/branding.

Grounding requirements:

- Verify exact video title, topic, and current thumbnail before suggesting changes.
- If transcript exists, check whether the title promise is fulfilled in the first 30-60 seconds.
- If CTR/impressions are absent, say packaging is a hypothesis.

Generate 3 distinct variants:

1. **Result showcase** — thumbnail shows the final workflow/result; title names the searchable problem.
2. **Before/after** — thumbnail contrasts messy/manual vs automated/clean; title names the transformation.
3. **Bold claim/problem** — thumbnail carries 2-3 power words; title anchors the keyword and avoids pure clickbait.

Title-thumbnail synergy rule:

- Title = searchable intent + specific promise.
- Thumbnail = visual proof/emotion.
- If both say the same thing, one signal is wasted.

Thumbnail QA:

- Readable at mobile size.
- One focal point.
- Max 0-4 words.
- High contrast.
- Avoid generic screenshots unless zoomed/cropped to the actual result.
- For trust-based educational content, do not overuse shock/fear if it harms credibility.

### Module D — Retention/script diagnosis

Run this when average view percentage is weak, retention curve drops early, or views are high but conversion is low.

First 42 seconds:

- 0-10s: show result or name the painful problem.
- 10-28s: promise what the viewer will be able to do/understand.
- 28-42s: stakes — why this matters now.

Body pacing:

- Pattern interrupt every 60-90 seconds for long tutorials.
- For screen recordings, alternate demo, explanation, problem/solution, result reveal, and context.
- Avoid three consecutive explanation-only segments.
- Place soft CTA before the observed average view duration, often around 25% of video length.

Diagnosis mapping:

- High search + low retention: keyword works; content/promise does not.
- Low search + high retention: content works; packaging/distribution does not.
- High AVD but low average percentage on very long videos: consider shorter sequel/clip series.
- Average percentage above 100%: likely replay/short behavior; do not compare directly to long-form.

### Module E — Comment intelligence

Run when comments are available and the question is about next topics, branding, or audience language.

Mine comments for:

- feature requests: "can you make...", "does this work with..."
- pain points: "I've been trying to...", "I couldn't figure out..."
- repeated questions: 3-5 repeats can justify a follow-up video.
- competitor mentions: tools/workflows viewers compare against.
- conversion signals: "I subscribed because...", "this made me try..."

Use direct phrases from comments as title/description language. Do not invent audience wording.

### Module F — Shorts and repurposing

Use only after long-form analysis. Shorts are not a replacement for evergreen search videos.

Good clip candidates:

- hook/result visible in first 2 seconds
- self-contained without context
- one clear wow moment, tip, or before/after
- points to a long-form video or playlist for deeper learning

Bad candidates:

- setup-only explanations
- inside jokes from a long stream
- clips that require previous context
- clips whose retention would not help the core channel positioning

## SEO metadata QA

Use this as a checklist, not as a ranking guarantee.

- Title under about 70 characters.
- Primary keyword/problem appears early.
- Description first 2-3 lines explain the concrete promise.
- 200+ characters of natural, non-stuffed prose.
- Chapters use meaningful labels, not generic `Intro`, `Part 1`.
- 3-5 hashtags max unless there is a clear reason.
- Tags are secondary; do not optimize tags at the expense of title/thumbnail/hook.
- Never use random emotional trigger words as final copy.

## Output formats

### Strategy summary

```markdown
**한 줄 결론**
> ...

**근거**
- traffic: ...
- retention: ...
- conversion: ...
- qualitative: ...

**진단**
- repackage 후보: ...
- hook 점검 후보: ...
- series 후보: ...

**다음 실험**
1. ... — metric reason
2. ... — metric reason
3. ... — metric reason
```

### Packaging brief

```markdown
**현재 패키징 진단**
- title: ...
- thumbnail: ...
- first 30s promise match: yes/no/unknown
- CTR/impressions: exact/proxy unavailable

**Variant A — Result showcase**
- title:
- thumbnail brief:
- why:

**Variant B — Before/after**
...

**Variant C — Bold claim/problem**
...
```

## Red flags

- Starting with viral title generation before metrics.
- Reporting exact CTR/search terms without Studio/API support.
- Copying competitor wording without matching Beomsu's actual promise.
- Treating external benchmark tables as truth for Beomsu's channel.
- Mutating live metadata during analysis.
- Using mock analytics.
- Recommending clickbait that will damage retention/trust.
