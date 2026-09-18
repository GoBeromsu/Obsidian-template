# YouTube data sources and limitations

Use this reference to choose the right source before analyzing Beomsu's channel.

## Ataraxia uploaded-video notes

Source of truth for Beomsu's own upload context:

- Vault: `${OBSIDIAN_VAULT_PATH}`
- Folder: `15. Work/02 Area/Youtube/`
- MoC: `70. Collections/03 MoC/📚 802 Youtube.md`
- Base: `90. Settings/05 Bases/YouTube Uploads.base`
- Base condition: `type == ["video"]` and `tags.contains("youtube/uploaded")`

Use notes for:

- uploaded video IDs and YouTube URLs
- intended title/topic/language/duration
- transcript and `## Feedback` qualitative review
- production context that YouTube APIs do not know

Do not mutate these notes unless the user explicitly asks to persist stats or edits.

## YouTube Data API v3

Use for public/current metadata:

- `channels.list(part=snippet,statistics,mine=true)`
- `videos.list(part=snippet,statistics,contentDetails,status&id=...)`

Good for:

- current public views/likes/comments
- publish date, duration, title, channel ownership
- recent velocity when joined with publish date
- detecting private/deleted/missing videos

Not available from Data API:

- CTR
- impressions
- retention curves
- traffic sources
- search terms
- audience geography
- subscribers gained per video

Never report those as Data API facts.

## YouTube Analytics API v2

Requires OAuth token with `https://www.googleapis.com/auth/yt-analytics.readonly` and the Cloud project API `youtubeanalytics.googleapis.com` enabled.

Good for:

- `views`, `estimatedMinutesWatched`, `averageViewDuration`, `averageViewPercentage`
- `subscribersGained`, `subscribersLost`
- `likes`, `comments`, `shares`
- dimensions: `video`, `day`, `country`, `subscribedStatus`, `insightTrafficSourceType`
- retention curves with `elapsedVideoTimeRatio` + `audienceWatchRatio`

Caveats:

- Direct owner search-term queries using `insightTrafficSourceDetail` may be unsupported. If it returns no rows/errors, say exact search terms are unavailable and use proxy analysis.
- Month reports require month-aligned date ranges; use `day` and aggregate manually when unsure.
- Impressions/CTR may not be available from the Analytics API query set in this environment. Prefer YouTube Studio export if the user needs exact packaging metrics.

## YouTube Studio export

Best source when the user wants exact:

- impressions
- CTR
- exact YouTube search terms
- thumbnail/title experiment data
- audience retention UI screenshots/export not exposed by API

If not available, clearly label API-derived estimates as proxies.

## Transcript / qualitative sources

Preferred order for Beomsu's own videos:

1. Existing Ataraxia upload note transcript and `## Feedback`.
2. YouTube page extraction/Defuddle for watch URLs when available.
3. Transcript extraction tool/skill (InnerTube or `youtube-transcript-api`) with `yt-dlp` fallback.
4. Audio transcription from the original mp4 if local source exists.

Use transcripts to explain *why* retention changed: hook timing, pacing, promise mismatch, dead air, unclear screen recording, English delivery friction.
