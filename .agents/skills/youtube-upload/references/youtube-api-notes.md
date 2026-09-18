# YouTube Data API v3 — Upload Notes

## OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select or create a project (can reuse an existing project)
3. Enable **YouTube Data API v3** under APIs & Services → Library
4. Create **OAuth client ID** under APIs & Services → Credentials
   - Application type: **Desktop app**
   - Download the JSON file
5. Save as `~/.config/youtube-upload/credentials.json`
6. Run `python upload.py --auth-only` to complete the consent flow
7. Token is saved to `~/.config/youtube-upload/token.json`

## Quota

- `videos.insert` costs **1600 quota units** per upload
- Default daily quota: **10,000 units** (~6 uploads/day)
- Request quota increase if needed via Cloud Console

## Visibility Restriction

**Important**: API projects created after 2020-07-28 that have NOT passed
Google's audit restrict all uploads to **private** visibility, regardless of
what `privacyStatus` is set to.

Workaround:
- Upload as private (default)
- Manually change visibility in YouTube Studio
- OR request an API audit from Google

## Scopes

This skill uses: `https://www.googleapis.com/auth/youtube.upload`

Blog-writer uses different scopes (`blogger`, `webmasters`) — tokens are NOT
interchangeable. Each tool needs its own `token.json`.

## Resumable Upload

The upload script uses resumable upload (5MB chunks) for reliability. This
handles network interruptions gracefully. Large files (>1GB) may take several
minutes.

## Category IDs

Common categories:
- 22: People & Blogs (default)
- 27: Education
- 28: Science & Technology
- 24: Entertainment
- 10: Music
