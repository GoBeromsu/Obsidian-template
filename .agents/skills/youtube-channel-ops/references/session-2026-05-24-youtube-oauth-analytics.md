# 2026-05-24 YouTube OAuth + Analytics API lessons

## Context

During YouTube channel analysis, the existing `~/.config/youtube-upload/token.json` refresh failed with `invalid_grant` / `Token has been expired or revoked`, so a fresh OAuth login was required for Analytics data.

## Durable lessons

- Request both scopes when retention/search-term analytics are needed:
  - `https://www.googleapis.com/auth/youtube`
  - `https://www.googleapis.com/auth/yt-analytics.readonly`
- Do not use `include_granted_scopes=true` in the ad-hoc OAuth flow if Google returns `Scope has changed ...` during token exchange. Start a clean consent flow with only the needed scopes.
- A local OAuth callback server should not exit after the first request. Browsers may hit the callback URL without a `code` parameter or leave old callback tabs open. Keep serving until a status file is written or a timeout expires.
- After a successful token with `yt-analytics.readonly`, the Google Cloud project behind the OAuth client must also have `youtubeanalytics.googleapis.com` enabled. If the API returns 403 `YouTube Analytics API has not been used in project ... or it is disabled`, enable it for that exact project number/project ID, then retry after propagation.
- Google OAuth account selection matters. If the user has both a personal channel and Brand Account, choosing the Brand Account can produce a valid token whose `channel==MINE` Analytics reports are empty/zero. Verify the token's active channel by comparing `channels?mine=true` or Analytics totals with known uploaded videos. If it points to the wrong channel, re-run OAuth and choose the personal channel/account that owns the uploaded videos.
- YouTube Data API public video stats can still validate ownership and titles even when Analytics rows are empty. Use `videos?part=snippet,statistics&id=...` to check `channelTitle` / `channelId` for sampled uploaded video IDs.

## Safe verification checklist

1. Confirm token scopes without printing access or refresh tokens.
2. Run a Data API `channels?mine=true` / `videos?...` check to confirm the active channel matches uploaded-video notes.
3. Run a small Analytics probe:
   - overall metrics for `channel==MINE`
   - by-video metrics for `channel==MINE`
   - traffic source and search term queries
4. If Analytics returns zero rows but Data API video IDs belong to another channel, redo OAuth with the correct Google channel/account.

## Pitfalls

- Do not print credential JSON, client secrets, access tokens, refresh tokens, OAuth callback URLs containing `code=`, or full auth URLs in user-facing chat.
- Do not interpret a valid OAuth token as proof it is the correct channel. Brand-account selection can silently produce a valid but strategically useless token.
- Do not report retention/search terms from Data API; those require YouTube Analytics API.
