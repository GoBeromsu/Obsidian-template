# YouTube Analytics API query cookbook

Use this reference for exact query shapes that worked or failed in Beomsu's environment.

## Token/channel preflight

Before private analytics, verify:

- token scopes include `https://www.googleapis.com/auth/yt-analytics.readonly`
- `channels.list(part=snippet,statistics,mine=true)` returns `Beomsu Koh | 고범수`
- Analytics overall query returns nonzero rows for `channel==MINE`

If `channels?mine=true` shows a Brand Account with zero Analytics rows, re-run OAuth and choose the personal channel/account.

## Working reports

Base params:

```text
ids=channel==MINE
startDate=<YYYY-MM-DD>
endDate=<YYYY-MM-DD>
```

### Overall

```text
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares
```

### By video

```text
dimensions=video
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,comments,shares
sort=-views
maxResults=200
```

Join `video` IDs to Data API `videos.list(part=snippet,statistics,contentDetails,status)` for titles and current public stats.

### Traffic source

```text
dimensions=insightTrafficSourceType
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage
sort=-views
```

Report both view share and watch-time share.

### Retention curve per video

```text
dimensions=elapsedVideoTimeRatio
filters=video==<video_id>
metrics=audienceWatchRatio,relativeRetentionPerformance
sort=elapsedVideoTimeRatio
```

Use this for selected videos only; choose top views, top retention, and recent velocity leaders. Summarize key points such as 0%, 25%, 50%, 75%, 95% rather than dumping all rows to Discord.

### Day trend

```text
dimensions=day
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage
sort=day
```

Use day and aggregate manually for month/week. Direct `month` requires month-aligned start/end dates and can fail if the range starts mid-month.

### Country / subscribed status

```text
dimensions=country
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage
sort=-views
```

```text
dimensions=subscribedStatus
metrics=views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage
sort=-views
```

## Known caveats

### Search terms

Queries using `insightTrafficSourceDetail` with `filters=insightTrafficSourceType==YT_SEARCH` returned unsupported-query errors in this environment. Do not claim exact keyword data unless rows are returned; fall back to title/topic proxy or Studio export.

## Reporting API and Studio export escalation

When exact YouTube search terms / CTR / impressions are needed and Analytics API rows are unavailable:

1. Verify the OAuth project from the token error context or `gcloud projects list` if needed.
2. Enable `youtubereporting.googleapis.com` on that project when the API returns `SERVICE_DISABLED`.
3. Probe `https://youtubereporting.googleapis.com/v1/jobs` with the refreshed YouTube OAuth token.
4. If `jobs` returns `{}` or an empty list, do **not** expect historical CSV reports to exist yet; Reporting API only exposes configured jobs/reports, not an instant replacement for Studio exports.
5. Escalate to YouTube Studio Advanced Mode CSV export for exact search terms / CTR / impressions, then merge the export with API-derived 30/90 day channel analysis.

Studio-visible snapshot values are useful for sanity checks, but avoid treating them as the exact same period as API scripts unless the date range matches. Studio defaults can be Last 28 days, while scripts often use 30/90 days.

Implementation note from 2026-05-24: do **not** add `maxResults` to this probe. It can surface a misleading `FIELD_UNKNOWN_VALUE` on `max-results` before the real unsupported-query caveat. The script intentionally stores the unsupported-query error in JSON so reports stay honest.

Fallback proxy:

- traffic-source totals (`YT_SEARCH` share)
- title/topic keyword aggregation over videos
- Ataraxia note topics and transcript terms
- public velocity of keyword-bearing videos

### Impressions / CTR

`impressions` was not accepted by the Analytics query tested here. For exact CTR/impressions, ask for or use YouTube Studio export. Without it, label title/thumbnail conclusions as hypotheses.

### Error handling

- 403 API disabled → enable `youtubeanalytics.googleapis.com` on the OAuth project.
- zero rows with valid token → likely wrong channel/Brand Account selection.
- `invalid_grant` → re-authorize; do not print token contents.
