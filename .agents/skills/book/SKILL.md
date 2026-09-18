---
name: book
description: Create or update book notes in the Obsidian vault with structured frontmatter, ToC skeleton, and body sections. Use when the user provides a book URL (yes24.com, aladin.co.kr), a book title, says "책 노트", "book note", "이 책 처리해줘", or wants to process a book from the Inbox. Also triggers on update requests like "하이라이트 정리", "목차 넣어줘", "프론트매터 정리".
version: 1.0.1
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob, WebFetch, WebSearch]
compatibility: claude-code, hermes
---

# book

## Overview

Create or update book notes in `80. References/01 Book/`. Three source paths: URL-based (yes24.com), title-only (WebSearch fallback), or classic/historical text (Korean filename convention). Covers both creation and update workflows, including ToC skeleton injection and highlight-to-chapter mapping.

## Vault Access

Load the craft `obsidian` skill's CLI recipe (`cli.md` in that package's references) for reusable create/edit/search/move mechanics, and the second-brain policy for Ataraxia routing, templates, and provenance. Verify the selected binary's help and exact vault mapping: community NotesMD (`obsidian-cli` may be its alias) does not require the app running; the official app CLI has separate prerequisites and syntax. Do not mix their commands or shell out to raw `cat`/`sed` on vault paths.

Write this user-curated Book zone only for the user's explicit book-note request. Instantiate each new note from its matching agent template and resolve its required fields, including `created_by`; the examples below guide the fill, not a replacement frame.

## Output Contract

Return the created or updated book-note path, sourced metadata, preserved user content, and exact readback evidence. If the vault, template, required authority, or source evidence is unavailable, stop the affected write and report the limitation rather than fabricate metadata or claim an unverified note. Distinguish filesystem materialization from CLI, backlink, and index verification.

## When to Use

- Use when the user provides a yes24.com URL or any bookstore link
- Use when the user provides a book title and wants a vault note
- Use when an existing book note needs frontmatter migration or chapter reorganization
- Use when the user says "이 책 노트로 만들어줘", "book note 만들어줘", "업데이트하는데"
- Do not use for paper, article, or video notes

## Process

### Path A: URL provided

1. Run `uv run scripts/fetch_yes24.py <url>` (relative to this skill directory) to extract metadata JSON
2. The script returns: `title`, `subtitle`, `authors`, `cover_url`, `description`, `date_published`, `isbn13`, `categories`, `toc`, `introduce`, `in_book`, `pub_review`
3. If `toc` is empty (JS-rendered), try in order:
   a. `scrapling extract fetch "<url>" /tmp/yes24_toc.html --css-selector "#infoset_toc" --wait-selector "#infoset_toc textarea" --headless` — JS-rendered ToC 직접 추출
   b. If scrapling unavailable or fails, run `uv run scripts/fetch_aladin_toc.py <isbn13>` and OCR the returned image URLs with Claude vision
4. Compose the note for `80. References/01 Book/<filename>.md` through the verified vault-aware create/edit operation from the CLI recipe. Check existing target content before writing and verify the exact filesystem path plus supported CLI readback afterward. If that CLI is unavailable or returns success without materializing the note, a bounded direct write to the already-verified exact path is acceptable within the same note-write authority; preserve existing content and disclose unavailable CLI/index verification. This fallback does not authorize raw filesystem rename, deletion, or registration changes.

### Path B: Title only

1. WebSearch: `"<title>" site:yes24.com` to locate the product page
2. If found, follow Path A
3. If not found, WebSearch: `"<title>" site:aladin.co.kr` and extract metadata via WebFetch (the `fetch_yes24.py` script only works with yes24.com URLs)
4. If neither found, gather metadata from publisher sites, Wikipedia, book databases via WebSearch + WebFetch; populate at minimum `title`, `author`, `date_published`, `description`, and generate the 3줄 요약

### Path C: Classic/historical text

1. Use the most recognized Korean title as the filename (e.g., `기독교 강요.md`, `국부론.md`)
2. Include the original-language title in `aliases`
3. Separate original author and translator in the `author` field

### File Naming

Use the **original title language** as the filename; put the published Korean translation in `aliases`.

- Korean original: `우리가 빛의 속도로 갈 수 없다면.md`
- English original: `Antifragile.md` → `aliases: ["안티프래질"]`
- Japanese original: `君たちはどう生きるか.md`
- Classic exception: `기독교 강요.md` → `aliases: ["Institutio Christianae Religionis"]`

### Frontmatter

```yaml
---
aliases:
  - "출판된 번역 제목"
author:
  - "[[저자명]]"
cover_url: https://...
date_created: YYYY-MM-DD
date_modified: YYYY-MM-DD
date_published: YYYY-MM-DD
date_started: YYYY-MM-DD
description: ...
isbn: ...
source_url: <book URL>
status: todo
subtitle: ...
tags:
  - reading
  - reading/YYYY
  - <genre tag in English>
title: ...
type: book
---
```

### Body structure

```markdown
> [!summary]+ 3 줄 요약
> - (AI-generated Korean bullet 1)
> - (AI-generated Korean bullet 2)
> - (AI-generated Korean bullet 3)
![표지 설명|240](cover_url)
## Detail
- (User-specific reading context, anecdotes, reading-start notes, or relationship context when supplied)
## Thinking
- 
## 공명
- 
## Linking
- (related wikilinks)
## 목차
#### (main sections from ToC; use H4 entries for compact book-note outlines unless a richer hierarchy is required)
## 책소개
(prose from #infoset_introduce)
## 책 속으로
(prose from #infoset_inBook)
## 출판사 리뷰
(prose from #infoset_pubReivew; third-party quotes as blockquotes)
```

Ataraxia formatting overrides older examples: no H1 (`#`) in book-note bodies, no blank lines between body sections, main sections use `##`, local ToC entries can use `####`, and user-provided anecdotes belong in `## Detail` with wikilinks preserved.

### Updating an Existing Note

Trigger: user says "update", "업데이트", or asks to organize highlights under chapters.

1. Read the existing note — collect all frontmatter, quotes, and personal notes
2. Get ToC via `uv run scripts/fetch_yes24.py <source_url>`; fall back to `uv run scripts/fetch_aladin_toc.py <isbn13>` + OCR
3. Migrate deprecated frontmatter fields:
   - `publish_date` → `date_published`, `start_read_date` → `date_started`
   - `my_rate`, `book_note`, `category`, `total_page` → remove
   - `author` strings → `"[[Author Name]]"` wikilink format
4. Classify content: personal notes (date-stamped `[[YYYY-MM-DD]]` bullets, first-person) vs book quotes (blockquotes)
5. Map each highlight to the most thematically relevant chapter heading
6. Deduplicate: keep the instance with more context; remove bare duplicates
7. If the current filename is a Korean translation of a foreign-language original, use the selected CLI recipe's verified vault-aware move operation and move the Korean title into `aliases`; verify the destination and affected links. Do not substitute another binary's move syntax.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The title is close enough; I can skip metadata cleanup." | Inconsistent metadata makes notes hard to search and deduplicate. |
| "I'll create a second note instead of renaming the first one." | Duplicate book notes cause vault drift and broken wikilinks. |
| "A storefront summary is enough; I don't need the ToC." | A note with accumulated highlights but no chapter structure is as unfinished as a blank template. |
| "I can use `mv` to rename the file." | Use the verified vault-aware move operation and check affected backlinks; raw filesystem movement is not the content-write fallback. |
| "The script failed, so I'll skip metadata and just create a stub." | Try at least 2 alternative sources (aladin script, publisher site, WebSearch) before falling back to manual metadata. |

## Red Flags

- The workflow creates duplicate notes instead of renaming or updating in place
- Filename and alias rules are mixed up (Korean title as filename for foreign-language original)
- Required frontmatter fields are missing after creation
- Filesystem `mv`/`cp` used instead of the verified vault-aware move operation
- ToC sourcing skipped when yes24 `toc` field is empty

## Verification

After completing the workflow, confirm:

- [ ] Metadata resolved from at least one authoritative source (yes24, aladin, publisher, or WebSearch)
- [ ] Filename follows original-language convention; Korean translation in `aliases`
- [ ] Frontmatter includes all required fields: `title`, `author` (wikilink format `[[Name]]`), `type: book`, `status`, `tags` (reading, reading/YYYY), `date_created`, `isbn`
- [ ] Body has: 3줄 요약 callout, optional cover embed, `## Detail` when user-specific context exists, `## Linking`, `## 목차`
- [ ] Body obeys Ataraxia markdown rules: no H1/H5+, no blank lines between body sections, hyphen bullets with tab indentation for nested bullets
- [ ] Existing highlight content preserved or mapped to chapters (update flow)
- [ ] Note created/updated at `80. References/01 Book/<filename>.md` and verified with `obsidian-cli print --vault Ataraxia "80. References/01 Book/<filename>.md"`
- [ ] No Inbox placeholder left behind after processing
- [ ] Run `qmd update && qmd embed` after Ataraxia edits; if `qmd update` times out after updating `obsidian`, check `qmd status` and run `qmd embed` to finish pending embeddings before reporting search verification
