# YouTube Analytics OAuth re-auth pattern

Use this when YouTube upload credentials exist but Analytics calls fail with `invalid_grant`, `Token has been expired or revoked`, or the token lacks `yt-analytics.readonly`.

## Durable lesson from session

For channel performance analysis, public `yt-dlp` metadata can give a useful first-pass proxy, but retention, watch time, traffic source, search terms, impressions, and CTR require YouTube Analytics OAuth scope.

Required scopes for combined upload/channel ops + analytics reads:

- `https://www.googleapis.com/auth/youtube`
- `https://www.googleapis.com/auth/yt-analytics.readonly`

## Re-auth workflow

1. Keep using the existing OAuth client credentials file, normally:
   - `~/.config/youtube-upload/credentials.json`
2. Treat the old token as disposable when refresh returns `invalid_grant`; do not keep retrying refresh forever.
3. Start a local loopback OAuth server on `127.0.0.1:<free-port>` and request `access_type=offline` plus `prompt=consent`.
4. Save the generated auth URL to a temp file such as `/tmp/youtube_auth_url.txt` so the browser step can be resumed after tool interruptions.
5. Save callback result/status to a temp file such as `/tmp/youtube_oauth_status.json`; include success/error state and scopes, but never token values.
6. After approval, write the new token to `~/.config/youtube-upload/token.json`.
7. Verify the stored token includes `yt-analytics.readonly` before running Analytics queries.

## Important pitfall

Avoid `include_granted_scopes=true` for this re-auth flow unless the code explicitly accepts Google returning a superset of scopes. In this session, Google returned previously granted scopes too, causing a `Scope has changed` mismatch during token exchange. Removing `include_granted_scopes` made the requested-scope comparison predictable.

## Safety

- Never print access tokens, refresh tokens, client secrets, or full token JSON to chat/log summaries.
- It is okay to print a Google OAuth URL for the user/browser to open.
- If using browser/computer tools, stop at account/password/permission boundaries unless the user explicitly asked to proceed; do not type secrets.

## Analysis sequence after re-auth

Once OAuth is valid, combine:

1. Ataraxia YouTube upload notes for title/topic/context.
2. Public metadata for broad coverage and missing/private detection.
3. YouTube Analytics API for retention/watch-time/traffic-source/search/impressions/CTR.

Look specifically for:

- Low-view but high-retention videos.
- Search-driven titles/keywords.
- High-impression low-CTR packaging problems.
- Early-retention drop-off formats.
- Repeatable winning formula across topic + format + source.