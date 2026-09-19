---
name: video
description: Create a YouTube/video note in the Obsidian vault from a URL using the vault's video template and property names, so it appears in Video.base. Use when the user gives a YouTube URL or video id and says "영상 노트", "video note", "이 영상 저장해 줘", "유튜브 정리해 줘", or asks to add a video to the vault.
version: 1.0.0
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch]
compatibility: antigravity, claude-code, codex, hermes
---

# video

## Overview

Turn one YouTube URL into one note at `85. Raw/02 Videos/<title>.md` with the same frontmatter as `90. Settings/02 Templates/manual/video.template.md`. `90. Settings/05 Bases/Video.base` reads `author`, `date_published`, and `image`, so a note written with these names shows up as a card immediately. Create one note per request and report the path.

## Workflow

1. **Get metadata** (no login, no extra install):
   - Run `python3 .agents/skills/video/scripts/fetch_youtube_meta.py "<url>"` and read the JSON.
   - If Python is unavailable, fetch `https://www.youtube.com/oembed?url=<encoded url>&format=json` for `title`, `author_name`, and use `https://img.youtube.com/vi/<video_id>/maxresdefault.jpg` as `image`. Leave `date_published` and `duration_seconds` empty if you cannot read the watch page.
2. **Read the template** `90. Settings/02 Templates/manual/video.template.md` and keep every property name exactly. Replace the two `<% tp.date.now("YYYY-MM-DD") %>` values with today's date (`YYYY-MM-DD`).
3. **Write the note** to `85. Raw/02 Videos/<safe title>.md`:
   - filename: the video title with `/ \ : * ? " < > |` removed; keep Korean and English as-is
   - `title`: quoted original title · `author`: channel name · `speaker`: leave empty unless the user names one
   - `description`: one line from the video description or the user's words · `source_url`, `image`, `video_id`, `duration_seconds`, `language`, `date_published` from step 1
   - `status: todo`, `type: video`, tags `reference` and `reference/video`, `created_by: user`, `authorship: user`
   - body: keep the template's headings `## 공명`, `## 핵심`, `## 내 말로`, `## 다음 질문`, `## Transcript`; fill `## 핵심` with the video's public description or chapter list when available; leave `## 공명`, `## 내 말로`, `## 다음 질문` for the user
4. **Verify**: read the file back, confirm the frontmatter parses (no tabs, quoted title), and tell the user to open `90. Settings/05 Bases/Video.base` to see the card.

## Rules

- Do not paste a transcript unless the user provides one or asks for it; `## Transcript` stays empty by default.
- Do not invent `date_published`, `duration_seconds`, or `description`; leave a field empty when the source does not provide it.
- Do not create a people note for the channel; `author` is plain text. The user may turn it into a wikilink later.
- Do not touch other notes, the template, or the Base. One request, one file.
- If a note with the same `video_id` already exists in `85. Raw/02 Videos/`, report it and stop instead of duplicating.

## Example

Request: `이 영상 노트 만들어 줘 https://www.youtube.com/watch?v=LWd5J-srk9w`

Result: `85. Raw/02 Videos/모두가 '나를 아는 AI OS'를 설계하는 시대, 격차는 어디서 오는가.md` with `author: Brian's Brain Trinity`, `date_published: 2026-09-18`, `duration_seconds: 2409`, `image: https://img.youtube.com/vi/LWd5J-srk9w/maxresdefault.jpg`, then a card in `Video.base`.

## Checklist

- [ ] Property names identical to `manual/video.template.md`
- [ ] `title` quoted; `type: video`; tags include `reference/video`
- [ ] `image` is a thumbnail URL, not a page URL
- [ ] File under `85. Raw/02 Videos/`; path reported; no duplicate `video_id`
- [ ] Transcript only when supplied or requested
