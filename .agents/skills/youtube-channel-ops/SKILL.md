---
name: youtube-channel-ops
description: >-
  Analyze and operate Beomsu's YouTube channel using Ataraxia uploaded-video notes plus YouTube Data API and YouTube Analytics API OAuth stats. Use when the user asks about YouTube channel strategy, retention, 조회수 추이, 검색 유입, 유입 키워드, 트래픽 소스, CTR/impressions, 영상 성과, 마케팅/브랜딩, 제목/썸네일/SEO, 업로드 노트 분석, or next-video experiments. Prefer compact Discord bullets over tables. Load references for deep analysis: `channel-analysis-playbook.md`, `marketing-strategy-and-packaging.md`, `youtube-data-sources-and-limitations.md`, `analytics-query-cookbook.md`, `growth-and-packaging-rubric.md`, and `transcript-and-qualitative-analysis.md`.
compatibility: Requires Ataraxia vault access, YouTube OAuth files at ~/.config/youtube-upload/, and Python network access. Analytics reports require yt-analytics.readonly scope and youtubeanalytics.googleapis.com enabled on the OAuth project.
version: 1.0.1
allowed-tools: [Bash, Read, Write, Grep, Glob, WebFetch]
---

# YouTube Channel Ops

This skill is Beomsu's YouTube channel-analysis runbook. It combines:

- Ataraxia upload notes as the qualitative/source-of-truth layer
- YouTube Data API v3 for public/current video stats
- YouTube Analytics API v2 for private retention, watch-time, traffic-source, geography, and subscriber-conversion metrics
- transcript/feedback review for why a video held or lost attention

Use `youtube-upload` for publishing new videos. Use this skill for analysis, strategy, stats snapshots, and next-video decisions.

## Start here

Ask the runtime's local-file reader for the absolute local path of this loaded
`youtube-channel-ops/SKILL.md`. If it cannot return a readable path, stop rather
than guessing an installation layout or source checkout. With that returned path:

```bash
CHANNEL_SKILL_FILE="<runtime-resolved path of the loaded youtube-channel-ops/SKILL.md>"
test -f "$CHANNEL_SKILL_FILE" || { printf '%s\n' 'ERROR: loaded youtube-channel-ops SKILL.md is unavailable.' >&2; exit 1; }
CHANNEL_SKILL_DIR="$(cd -- "$(dirname -- "$CHANNEL_SKILL_FILE")" && pwd -P)" || exit 1
test -f "$CHANNEL_SKILL_DIR/scripts/fetch_youtube_stats.py" || { printf '%s\n' 'ERROR: loaded youtube-channel-ops scripts are unavailable.' >&2; exit 1; }
```

For a quick public snapshot:

```bash
python3 "$CHANNEL_SKILL_DIR/scripts/fetch_youtube_stats.py" \
  --output /tmp/youtube_summary.json \
  --discord
```

For private Analytics API analysis:

```bash
uv run "$CHANNEL_SKILL_DIR/scripts/analyze_youtube_channel.py" \
  --public-summary /tmp/youtube_summary.json \
  --output /tmp/youtube_channel_analysis.json \
  --discord
```

If OAuth is expired, missing Analytics scope, or points to the wrong Google channel:

```bash
OAUTHLIB_INSECURE_TRANSPORT=1 python3 "$CHANNEL_SKILL_DIR/scripts/youtube_analytics_oauth_login.py"
```

Then open the URL saved in `/tmp/youtube_auth_url.txt`, choose the personal creator channel/account `Beomsu Koh | 고범수`, and verify `/tmp/youtube_oauth_status.json` says `auth_complete` with `yt-analytics.readonly`.

## Mandatory workflow

1. **Clarify the analysis question by action, not by asking first.** If the user says retention/keywords/channel analysis, run public snapshot + Analytics API if credentials are available.
2. **Check data-source limits before claiming facts.** Exact search terms, CTR, and impressions require API rows or YouTube Studio export; otherwise label keyword/packaging analysis as a proxy.
3. **Verify OAuth channel selection.** `channels?mine=true` must be `Beomsu Koh | 고범수`. A Brand Account can produce a valid token with useless zero Analytics rows.
4. **Separate rankings.** Always distinguish total views, recent velocity, retention, watch time, and subscriber conversion.
5. **Use transcripts/notes for diagnosis.** Metrics identify the symptom; Ataraxia transcript/Feedback explains hook, pacing, English delivery, and title-promise mismatch.
6. **Report in Discord-friendly bullets.** No large Markdown tables unless the user explicitly asks for a table or an Obsidian note.
7. **End with next-video experiments.** Tie each recommendation to a metric signal.

## Output Contract

Produce a compact Discord-friendly channel analysis from the public snapshot and, when authorized, Analytics API data; save temporary JSON outputs at the caller-selected paths such as `/tmp/youtube_summary.json` and `/tmp/youtube_channel_analysis.json`. Separate total views, recent velocity, retention, watch time, traffic source, and subscriber conversion, and label unavailable exact keywords, CTR, impressions, or private Analytics data as limitations. Verify the selected channel is `Beomsu Koh | 고범수` before treating private metrics as usable, and never include credentials, tokens, or OAuth callback data in the report. End the completion summary with the data period, sources used, key metric findings, limitations, and metric-linked next-video experiments. When credentials, Analytics scope, or channel verification are missing, stop the private analysis, report the safe status artifact, and limit conclusions to available public data.

## Data-source map

Read `references/youtube-data-sources-and-limitations.md` when choosing sources.

Key paths:

- Vault: `${OBSIDIAN_VAULT_PATH}`
- Upload notes: `15. Work/02 Area/Youtube/`
- MoC: `70. Collections/03 MoC/📚 802 Youtube.md`
- Base: `90. Settings/05 Bases/YouTube Uploads.base`
- OAuth: `~/.config/youtube-upload/credentials.json` and `~/.config/youtube-upload/token.json`

Never print credential JSON, access tokens, refresh tokens, client secrets, OAuth callback URLs containing `code=`, or full token contents.

## Analysis playbook

Read `references/channel-analysis-playbook.md` for the full strategy. The short version:

- Discovery: traffic sources, search share, keyword/title proxy
- Packaging: CTR/impressions if available; otherwise hypothesis only
- Retention: average view duration, average view percentage, retention curve points
- Conversion: subscribers gained, comments, likes, shares
- Strategy: evergreen validation vs recent momentum vs Beomsu's Obsidian/PKM + AI-agent positioning
- Marketing/branding: use `marketing-strategy-and-packaging.md` to turn metric signals into packaging, topic-gap, comment-intel, and next-video experiments

## API cookbook

Read `references/analytics-query-cookbook.md` for exact working query shapes.

Known-good reports:

- overall channel metrics
- by-video metrics
- traffic source
- subscribed status
- country
- day trend
- per-video retention curve

Known caveats:

- direct search-term query may be unsupported
- `impressions`/CTR may require Studio export
- month dimensions need aligned dates; use day and aggregate manually if unsure

## Growth and qualitative rubric

Read:

- `references/growth-and-packaging-rubric.md` for retention benchmarks, hook/title/thumbnail/description heuristics, and tech-channel growth rules.
- `references/marketing-strategy-and-packaging.md` for the absorbed marketing/branding playbooks: audit buckets, keyword/topic gap, packaging refresh, comment intelligence, Shorts/repurpose, and SEO QA.
- `references/transcript-and-qualitative-analysis.md` for transcript, chapter, speaker, and English-delivery diagnosis.
- `references/external-marketing-skill-absorption-2026-05-24.md` for what was absorbed from Beomsu's three shared GitHub repositories and what was intentionally rejected.
- `references/hub-skill-review-2026-05-24.md` for what was absorbed from shared/hub skills and what was intentionally kept out.

Current working hypothesis for Beomsu's channel:

> Obsidian credibility + AI Agent novelty + concrete workflow demo + personal builder journey.

Update this if future API data contradicts it.

## Discord report shape

```markdown
형님, 채널 분석 요약입니다.

**한 줄 결론**
> ...

**어디서 들어오나**
- Search: N views / N% / AVD Ns
- Shorts: ...

**리텐션 좋은 영상**
1. Title
   - retention: N%, AVD Ns, views N, subs +N
   - 해석: ...

**키워드 proxy / 정확 키워드 여부**
- exact search terms: available/unavailable
- proxy terms: ...

**전략 진단 버킷**
- repackage/distribute 후보: ...
- hook/promise 점검 후보: ...
- series 후보: ...

**다음 실험**
1. Title idea — metric reason
```

## Red flags

- Reporting CTR, impressions, search terms, or retention from Data API alone
- Treating a valid OAuth token as proof the correct channel was selected
- Printing secrets or auth callback URLs containing codes
- Using large Discord tables
- Combining Shorts/replayed clips with long-form retention without caveat
- Treating views/day on a very new video as stable
- Updating Ataraxia notes/frontmatter unless the user explicitly asks to persist stats

## Verification

Before final response:

- Credential/token status checked without exposing secrets, or limitation explained
- Correct channel verified as `Beomsu Koh | 고범수`
- Uploaded-note count and API-found count reported when using Ataraxia snapshot
- Analytics period stated
- Traffic-source, retention, watch-time, subscriber-conversion, and recent velocity separated
- Exact keyword/CTR availability stated honestly
- Recommendations tied to metric signals
- Discord output is compact and table-free
