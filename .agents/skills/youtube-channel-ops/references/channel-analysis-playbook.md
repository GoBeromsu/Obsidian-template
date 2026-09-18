# YouTube channel analysis playbook

Use this reference when the user wants strategy, retention, keyword, or channel-growth analysis rather than a simple upload/stat check.

## Analysis goals

Answer four questions separately:

1. **Discovery** — how people enter the channel: traffic-source mix, search share, title/topic keyword proxies, external/referral sources.
2. **Packaging** — whether title/thumbnail/first promise earns clicks: CTR and impressions if a Studio export is available; otherwise use search/velocity/public views as a proxy and label it.
3. **Retention** — whether the video keeps the promise: average view duration, average view percentage, retention curve shape, first-25% drop.
4. **Conversion** — whether the video builds the channel: subscribers gained, comments, likes, shares, repeatable viewer intent.

## Required lenses

Always separate these lenses instead of collapsing them into one ranking:

- **Evergreen validation:** total views, search share, watch time over 90-365 days.
- **Recent momentum:** views/day from public Data API joined with uploaded-video notes.
- **Retention quality:** averageViewPercentage and retention curve; treat >100% as replay/short-form behavior, not long-form proof.
- **Subscriber conversion:** subscribersGained per video and per topic.
- **Strategic fit:** whether the video strengthens Beomsu's Obsidian/PKM + AI-agent builder narrative.

## Standard run sequence

1. Run public snapshot first with `scripts/fetch_youtube_stats.py` to get tracked-note coverage and recent velocity.
2. Verify OAuth channel selection before private analytics. `channels?mine=true` must be `Beomsu Koh | 고범수`, not a Brand Account.
3. Run Analytics reports with `scripts/analyze_youtube_channel.py` for channel-wide private metrics.
4. Join the two outputs mentally or via JSON:
   - public snapshot = Ataraxia note context + current public video stats
   - analytics output = retention, watch time, traffic source, subscribers gained
5. If exact search terms/CTR/impressions are unavailable, say so and use grounded proxies only.
6. End with 3-5 next-video experiments, each tied to a metric signal.

## Report structure for Discord

Use compact bullets, not tables:

```markdown
형님, 채널 분석 요약입니다.

**한 줄 결론**
> ...

**어디서 들어오나**
- Search: N views / N% / AVD Ns
- Shorts: ...

**잘 붙잡는 영상**
1. Title
   - retention: N%, AVD Ns, views N, subs +N
   - 해석: ...

**검색/키워드 proxy**
- Exact search terms: available/unavailable
- Strong proxy terms: ...

**다음 실험**
1. Title idea — metric reason
```

## Interpretation rules

- Do not overfit very new videos: views/day in the first 72h is volatile.
- Do not compare shorts/replayed clips directly against 8-15 minute long-form.
- A high-view low-retention video can still be a good search doorway; pair it with a better follow-up.
- A low-view high-retention video is a packaging/distribution problem, not necessarily a topic problem.
- For Beomsu, the current strategic formula is: **Obsidian credibility + AI Agent novelty + concrete workflow demo + personal builder journey**.

## Action recommendations pattern

Map each recommendation to one metric:

- Low CTR / high retention → repackage title/thumbnail, make sequel.
- High search share / low retention → keep keyword, improve hook/pacing.
- High retention / low search → title around a searched problem; add description chapters.
- High subscriber gain → make a series or playlist.
- High views/day / weak retention → shorten intro, show outcome first, tighten title promise.
