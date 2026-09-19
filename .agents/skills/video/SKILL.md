---
name: video
description: Create a YouTube/video note in the Obsidian vault from a URL using the vault's video template and property names, so it appears in Video.base. Use when the user gives a YouTube URL or video id and says "영상 노트", "video note", "이 영상 저장해 줘", "유튜브 정리해 줘", or asks to add a video to the vault. Also handles transcript filling and 3-line summary generation when requested or when subtitles are available.
version: 1.1.0
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
compatibility: antigravity, claude-code, codex, hermes
---

# video

## Overview

Turn one YouTube URL into one note at `85. Raw/02 Videos/<title>.md` with the same frontmatter as `90. Settings/02 Templates/manual/video.template.md`. `90. Settings/05 Bases/Video.base` reads `author`, `date_published`, and `image`, so a note written with these names shows up as a card immediately. Create one note per request and report the path.

## Workflow

1. **Get metadata & content**:
   - Run `python3 .agents/skills/video/scripts/fetch_youtube_meta.py "<url>"` and read the JSON.
   - The script extracts `video_id`, `title`, `author`, `description`, `source_url`, `image`, `date_published`, `duration_seconds`, `language`, `chapters` (list of `{"time": "...", "title": "..."}`), and `transcript` (formatted with timestamps and chapter headings).
   - If Python is unavailable, fetch `https://www.youtube.com/oembed?url=<encoded url>&format=json` for `title`, `author_name`, and use `https://img.youtube.com/vi/<video_id>/maxresdefault.jpg` as `image`. Leave `date_published` and `duration_seconds` empty if you cannot read the watch page.
2. **Read the template** `90. Settings/02 Templates/manual/video.template.md` and keep every property name exactly. Replace the two `<% tp.date.now("YYYY-MM-DD") %>` values with today's date (`YYYY-MM-DD`).
3. **Write or update the note** to `85. Raw/02 Videos/<safe title>.md`:
   - filename: the video title with `/ \ : * ? " < > |` removed; keep Korean and English as-is
   - `title`: quoted original title · `author`: channel name · `speaker`: leave empty unless the user names one
   - `description`: one line from the video description or the user's words · `source_url`, `image`, `video_id`, `duration_seconds`, `language`, `date_published` from step 1
   - `status: todo`, `type: video`, tags `reference` and `reference/video`, `created_by: user`, `authorship: user`
   - `> [!summary]+ 3 줄 요약`:
     - Synthesize a clear, actionable 3-line summary into the callout box based on the transcript, chapters, or description.
   - body sections:
     - `## 공명`: leave default placeholder for the user
     - `## 핵심`: fill with description and chapter breakdown when available
     - `## 내 말로`, `## 다음 질문`: leave default placeholders for the user
     - `## Transcript`: insert the timestamped, chapter-divided transcript if available or requested. If no transcript was extracted, leave empty.
4. **Verify**: read the file back and confirm the frontmatter parses. Wrap `title`, `author`, and `description` in double quotes (escape inner `"` as `\"`), keep `description` to one line with no URL and no `: `, and no tabs anywhere. Then tell the user to open `90. Settings/05 Bases/Video.base` to see the card. If the card does not appear, the frontmatter did not parse; fix quoting first.

## Rules

- Always fill `> [!summary]+ 3 줄 요약` with three substantive bullet points when transcript or video content is available.
- If a transcript is available from the video or script, include it under `## Transcript` formatted with timestamps and chapter headings so the user does not have to ask twice.
- Do not invent `date_published`, `duration_seconds`, or `description`; leave a field empty when the source does not provide it.
- A colon followed by a space inside an unquoted value breaks YAML and hides the note from every Base. Always quote `title`, `author`, and `description`.
- Do not create a people note for the channel; `author` is plain text. The user may turn it into a wikilink later.
- Do not touch other notes, the template, or the Base. One request, one file.
- If a note with the same `video_id` already exists in `85. Raw/02 Videos/` and the user asks to update or fill it (e.g. transcript, summary), update the existing note in place instead of creating a duplicate file.

## Example

Request: `이 영상 노트 만들어 줘 https://www.youtube.com/watch?v=KiJSfVbW1jA`

Result: `85. Raw/02 Videos/평생 자식 위해 살았는데 자식과 멀어지는 부모들의 공통점ㅣ지식인초대석 EP.173 (이호선 교수 2부).md` with metadata, 3-line summary in callout, chapters in `## 핵심`, and formatted transcript under `## Transcript`, then a card in `Video.base`.

## Checklist

- [ ] Property names identical to `manual/video.template.md`
- [ ] `title` quoted; `type: video`; tags include `reference/video`
- [ ] `image` is a thumbnail URL, not a page URL
- [ ] `> [!summary]+ 3 줄 요약` populated with 3 key points
- [ ] File under `85. Raw/02 Videos/`; path reported; no duplicate `video_id`
- [ ] Transcript filled with timestamps and chapter breaks if subtitles exist
