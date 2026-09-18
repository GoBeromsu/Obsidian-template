# YouTube Analytics API OAuth + analysis lessons

Use this reference when analyzing Beomsu's YouTube channel performance with `youtube-channel-ops`.

## OAuth/account selection
- For channel analytics, OAuth must be granted to the actual creator account/channel, not a Brand account. In this session the correct channel was `Beomsu Koh | 고범수` (`@beomsukoh`), while a Brand account (`Berom - Entertainment`) produced channel==MINE results with zero videos/views.
- Verify after OAuth with both:
  - YouTube Data API `channels.list(part=snippet,statistics,mine=true)`.
  - YouTube Analytics `reports?ids=channel==MINE&metrics=views,...`.
- If Google localhost OAuth redirects to `http://127.0.0.1:<port>/`, set `OAUTHLIB_INSECURE_TRANSPORT=1` inside the local auth script. This is acceptable for installed-app localhost OAuth only.
- Keep the localhost callback server alive until a success/error status is written; browser/favicon or stray requests can otherwise kill a one-shot `handle_request()` server before the OAuth callback.

## Cloud/API prerequisites
- A successful YouTube OAuth token is not enough: the Google Cloud project behind the OAuth client must have `youtubeanalytics.googleapis.com` enabled.
- If Analytics API returns a 403 API-disabled error, enable it with `gcloud services enable youtubeanalytics.googleapis.com --project=<project-id>` if authenticated and authorized.

## Analytics queries that worked
- Overall: `ids=channel==MINE`, metrics `views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares`.
- By video: dimensions `video`, same core metrics, sorted by `-views`; join video IDs to Data API `videos.list(part=snippet,statistics,contentDetails,status)` to get titles/current public stats.
- Traffic source: dimensions `insightTrafficSourceType`, metrics `views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage`.
- Country and day reports worked. Month reports require date ranges aligned to the month dimension; use `day` and aggregate manually if unsure.
- Retention curves: dimensions `elapsedVideoTimeRatio`, filters `video==<id>`, metrics `audienceWatchRatio,relativeRetentionPerformance`.

## Search keyword caveat
- Direct channel-owner search-term queries with `insightTrafficSourceDetail` + `insightTrafficSourceType==YT_SEARCH` may return unsupported-query errors. Do not claim exact keyword data unless the API returns rows or a YouTube Studio export is available.
- If search terms are unavailable, provide a grounded proxy: traffic-source totals + title/topic keyword aggregation + Data API/Ataraxia note joins. Label it clearly as a proxy, not exact search-query data.

## Interpretation pattern for Beomsu
- Separate short/replayed videos from long-form: `averageViewPercentage > 100%` often means repeats/short duration, not long-form retention.
- Report: traffic-source share, watch-time share, top videos by views/watch time/subscriber gain, retention winners/losers, and recent velocity from public stats.
- Translate results into concrete next-video experiments. For Beomsu, prefer API-grounded retention/traffic/search insights that become actionable Obsidian/PKM + AI-agent/Hermes strategy.
