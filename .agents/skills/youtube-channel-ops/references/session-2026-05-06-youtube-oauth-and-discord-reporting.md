# 2026-05-06 — YouTube OAuth + Discord reporting baseline

This reference captures the first successful run that motivated `youtube-channel-ops`.

## Credential setup

The user provided OAuth files and approved using them for private channel operations.

Installed paths on m1-pro:

```text
~/.config/youtube-upload/credentials.json
~/.config/youtube-upload/token.json
```

Observed token scope:

```text
https://www.googleapis.com/auth/youtube
```

Do not print credential contents, access tokens, refresh tokens, client secrets, or copied secrets in chat.

## Ataraxia source of truth

`📚 802 Youtube` embeds `YouTube Uploads.base`, whose base condition was:

```yaml
type == ["video"]
tags.contains("youtube/uploaded")
```

The notes analyzed were under:

```text
15. Work/02 Area/Youtube/
```

The Base file was:

```text
90. Settings/05 Bases/YouTube Uploads.base
```

## Initial successful Data API run

Run date: 2026-05-06.

Channel:

- Title: `Beomsu Koh | 고범수`
- Handle: `@beomsukoh`
- Subscribers: 75
- Channel views: initially 23,143, later 23,220 during verification
- Channel videos: 70

Tracked uploaded-video notes:

- Obsidian upload notes: 38
- YouTube API found: 38
- Total views across tracked upload notes: 1,715
- Average views: 45.1
- Median views: 31
- Average velocity: about 3.94–3.95 views/day
- Total likes: 80
- Total comments: 12

Topic-level finding:

- `Obsidian / PKM` had the strongest historical/evergreen average views.
- `AI agents / Hermes` had the strongest recent velocity.
- `Daily build log` was weak when diary-only.

Fastest videos in the initial run:

1. `Claude Code vs Hermes Agent: Why Closed-Loop Agents Get Smarter Every Day`
2. `Hermes Agent First Look — Nous Research's Self-Improving AI Agent`
3. `에르메스 에이전트 리뷰: 독스에서 읽은 셀프 개선 AI의 핵심`
4. `I Need a Second-Brain Agent to Fix My Context Chaos`
5. `Hermes Agent Mental Model: Closed-Loop Memory, Skills, and the Harness Layer`

## User correction: Discord legibility

The user said Discord tables are hard to read. Encode this as a workflow rule:

- Do not use large Markdown tables for Discord reports.
- Prefer compact sections, bullets, and ranked lists.
- Use tables only when writing an Obsidian note or when explicitly requested.

## Limitation discovered

The YouTube Data API can retrieve public stats and metadata. It cannot retrieve CTR, impressions, retention curves, traffic sources, or search terms. Those require YouTube Analytics API scopes and a separate workflow.
