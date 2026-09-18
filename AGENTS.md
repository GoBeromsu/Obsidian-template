# Repository Guidelines

## User context and repository rules

Read the root `Me.md` first for the user's identity, values, thinking methods, AI collaboration preferences, and influences. Its labelled guidance is a prompt, not a statement of the user's beliefs; blank answers mean unknown. Do not invent answers or infer preferences from examples. Keep the public template blank; filled answers belong only in the adopter's own vault.

`Me.md` holds user context, while this `AGENTS.md` and the nearest nested contracts hold repository rules. Context and links do not grant permission to edit or follow linked notes. `CLAUDE.md` is only a pointer to `Me.md` and `AGENTS.md`, not a second rule source.

## Project Overview

This directory is a portable Obsidian vault template. It ships a 10-root skeleton, Templater files (including Daily and `manual/task.template.md`), Excalidraw drawings under `90. Settings/07 Excalidraw`, and portable `.obsidian` JSON (including Daily notes enablement and Templater `data.json`) without personal notes, credentials, plugin caches, plugin or theme binaries, or machine-specific state. Faith (`60. Saint`) and publication (`25. Digital Garden`) roots are intentionally absent. There is no Handbook folder.

Human start, placement, writing/AI, agent-skills, and template guides ship as English/Korean pairs. The two languages are equivalent translations of one contract, not two note homes. Neither language outranks the other. When those instructions change, update both files.

Nearest nested agent contracts: `90. Settings/AGENTS.md` and `90. Settings/02 Templates/AGENTS.md`. Do not add `AGENTS.md` to empty skeleton folders.

## Architecture & Data Flow

Capture starts in `00. Inbox` and is filed with the placement guide by ownership and note kind. Each note has one canonical location. Work, time, source-derived thinking, evergreen thinking, AI, collections, references, raw originals, and settings have separate roots. `85. Raw` keeps captured external originals regardless of which collector produced them; a refined note is separate from its source.

Periodic templates under `90. Settings/02 Templates/auto/` insert navigation wikilinks and, where present, embedded Bases (and one Dataview) views. Those links and views do not create missing notes. The Daily template is the only shipped creator: after it runs, it may add dashboard files for yesterday, today, and tomorrow. It does not cascade into weekly, monthly, quarterly, or yearly notes.

`auto/` templates are for periodic Time notes (folder-template / insert-on-create). `manual/` is on-demand insert (`note.template.md`, `task.template.md`, `project.template.md`, `log.template.md`, `video.template.md`, `book.template.md`). `90. Settings/05 Bases/` ships two standalone Bases, `Video.base` and `Books.base`, which read the property names those two templates stamp (`type`, `author`, `date_published`, `image`; `type`, `author`, `status`, `total_page`, `cover_url`). Title formats, engines, and creation rules live in `90. Settings/02 Templates/AGENTS.md` and the bilingual template READMEs.

The beginner lecture starts with the blank root `Me.md` personal briefing (`# Me` and five `##` sections: Summary Statement, First Principles, How I Think, Working Preferences, 나에게 영향을 주는 사람), a three-question Gemini interview using sanitized excerpts, and the adopter's own Map of Content (MOC) in `70. Collections/03 MoC` linking existing notes with a reason for each link. Each briefing section opens with a Korean `> 역할:` line stating what to write there. Thinking methods are optional examples to explain when and how they are used, not prescribed steps or asserted beliefs; influences are names only, with none supplied. The briefing is not a filled biography or an AI integration; the general project-hub/log workflow in `15. Work/01 Project` remains available but is not part of this beginner path. Keep filled answers in the adopter's vault; `## Thinking` sections elsewhere stay human-only.

## Key Directories

| Path | Role |
| --- | --- |
| `00. Inbox/` | Unsorted capture awaiting triage |
| `10. Time/` | Daily, weekly, monthly, quarterly, yearly, and dashboard notes |
| `15. Work/` | Projects, areas, archive, and tasks |
| `30. Literature Notes/` | Source-derived research, reviews, and meetings |
| `40. Permanent Notes/` | Self-contained ideas and principles |
| `50. AI/` | AI-generated or AI-synthesized material without another owner |
| `70. Collections/` | Reusable people, prompts, MOCs, music, places, organizations, GitHub, and channels |
| `80. References/` | Books, papers, and attachments |
| `85. Raw/` | Captured external originals |
| `90. Settings/` | Rules, templates, home, indexes, bases, and Excalidraw drawings (`07 Excalidraw`) |
| `.agents/skills/` | Vendored Agent Skills; real directory read by Codex and Antigravity |
| `.claude/skills/` | Symlink to `.agents/skills/`; read by Claude Code |

Do not add, rename, or renumber roots without recording the decision in `90. Settings/01 Guideline/` (both language files). `90. Settings/03 Home/` and `04 Index/` ship empty; `05 Bases/` ships `Video.base` and `Books.base` as worked examples, and `85. Raw/02 Videos/` ships one real public-metadata video note (Brian's Brain Trinity, Seoul Metaweek 2026 talk) so `Video.base` renders a card out of the box. Both Bases exclude `90. Settings/02 Templates` so template files never appear as results.

## Development Commands

Open a copied or cloned template directory as an Obsidian vault. No application build, test suite, index-rebuild, CLI-init, or git-init command is defined for this template, and none of those steps is claimed to have run. When an adopter keeps the template in a Git worktree, `git status --short` and `git diff --check` are optional review commands; no commit or push is mandatory. Do not launch Obsidian implicitly.

## Code Conventions & Common Patterns

- Read root `Me.md` for user context first, then this file, the nearest nested `AGENTS.md`, and the bilingual placement and template guides before creating or moving a note. Placement SSOT: `90. Settings/01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md`.
- Ownership determines placement even when an agent wrote the content. Keep captured originals in `85. Raw` regardless of collector, and never duplicate a note across roots.
- Completed tasks stay in their current project, area, or task path; record completion according to the adopter's task policy instead of requiring a physical move.
- Periodic titles follow `90. Settings/02 Templates` (`YYYY-MM-DD`, `GGGG-WW` plus `W`, `YYYY-MM`, `YYYY-QN`, `YYYY`, `YYYY-MM-DD Dashboard`). Template files use `*.template.md` in `auto/` or `manual/`. Do not invent extra Templater categories. Human-facing stamps stay `created_by: user` and `authorship: user`.
- Preserve existing YAML provenance and defer metadata field names and values to the adopter's policy. Human-facing templates in this folder already stamp `created_by: user` and `authorship: user`; do not add competing metadata requirements on top of them. Local schema is `created_by: user|agent` and `authorship: user|agent|mixed`.
- Root presence does not grant write permission. Follow the adopter's local policy and exact-note authorization before editing an existing note.
- `## Thinking` sections are human-only. Do not overwrite another writer's note, delete notes to resolve conflicts, or reorganize beyond the current task.
- If an adopter adds symlinks, preserve the target layout and do not move or delete targets without the governing policy decision.
- The vendored skill under `.agents/skills/obsidian/` is upstream content kept verbatim. Fix problems upstream and re-vendor, rather than editing the copy in place. The skill teaches generic Obsidian mechanics and never overrides this vault's own placement, writing, or permission guides.

## Important Files

- `README.md` and `README.ko.md` — equivalent start guides (scope, ten roots, shipped versus installed, first-use steps).
- `90. Settings/AGENTS.md` — settings-layer agent contract.
- `90. Settings/01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `90. Settings/01 Guideline/02. Writing and AI.md` and `02. Writing and AI.ko.md` — equivalent writing, minimal properties, privacy, and AI-boundary guidance.
- `90. Settings/01 Guideline/03. Agent Skills.md` and `03. Agent Skills.ko.md` — equivalent guides to the vendored skill's setup, discovery paths, and boundaries.
- `.agents/skills/README.md` — provenance record for the vendored skill (source, commit, license, update procedure).
- `Me.md` (vault root) — single blank personal briefing with the five `##` sections listed above, each opening with a Korean `> 역할:` line; agent-authored scaffold, not a human-stamped Templater file. It is the one deliberate root-level note exception; do not move it into `00. Inbox`, rename its sections, or add a second `Me` template.
- `CLAUDE.md` — simple pointer to root `Me.md` for user context and `AGENTS.md` for repository rules.
- `90. Settings/02 Templates/AGENTS.md` — template-layer agent contract.
- `90. Settings/02 Templates/README.md` and `README.ko.md` — equivalent Templater and core Daily notes setup (**Engine setup**).
- `90. Settings/02 Templates/auto/Daily Note.template.md` — shipped daily template; may create dashboards only.
- `90. Settings/02 Templates/manual/task.template.md` — on-demand task note; Dashboard query fields `type`, `done`, `gtd`, `project`, `plan`, `due`.
- `90. Settings/02 Templates/auto/` and `manual/` — other periodic templates and the on-demand note, video, and book templates.
- `90. Settings/05 Bases/Video.base` and `Books.base` — standalone Bases that read the video and book template properties; they are examples to copy for other note kinds.
- `.obsidian/app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, and `daily-notes.json` — portable Obsidian settings. Plugin IDs and shipped `data.json` are not installations. `appearance.json` names Minimal; theme files are absent. Two CSS snippets under `.obsidian/snippets/` are shipped. Core Daily notes is on.
- `.obsidian/plugins/templater-obsidian/data.json` and `.obsidian/plugins/obsidian-excalidraw-plugin/data.json` — allowlisted path config only; not plugin binaries.
- `90. Settings/07 Excalidraw` — canonical drawings and assets folder.

## Runtime/Tooling Preferences

- Use Obsidian with Templater for the shipped templates. `periodic-notes` is not in `community-plugins.json` and is not used. Keep templates under `90. Settings/02 Templates`. Keep drawings under `90. Settings/07 Excalidraw`.
- Core Daily notes is enabled (`daily-notes.json`: folder `10. Time/01 Daily Notes`, format `YYYY-MM-DD`, template empty). Templater folder templates for Daily, Weekly, Monthly, Quarterly, and Yearly ship in `templater-obsidian/data.json`. There is no Dashboard folder template; the Daily hook owns dashboards. Core Templates is enabled in `core-plugins.json` but is not the engine for `<% %>` files; no `templates.json` is shipped.
- `.obsidian/community-plugins.json` contains configured plugin IDs only. It is not an installation manifest. Confirm `.obsidian/plugins/` for binaries (`main.js`, `manifest.json`) before depending on a plugin or theme; a plugins directory or `data.json` is not install proof. This template does not ship plugin or theme binaries.
- Core Bases is enabled and is what the embedded ` ```base ` blocks use. Custom `type: timeline` views are not shipped. Dashboard Overdue uses Dataview, which is an ID only until installed.
- The template intentionally includes no external tool integrations or personal runtime state. Apply an adopter's local permission and provenance policy before writing notes.

## Testing & QA

There is no application build or test suite, and no end-to-end Obsidian run is claimed. Perform structural QA by checking all ten roots (including `90. Settings/07 Excalidraw` and `10. Time/01 Daily Notes`), the Daily template file, `manual/task.template.md`, the intentional absence of `25. Digital Garden`, `60. Saint`, and Handbook, bilingual guide pairs (neither language treated as primary), nested `AGENTS.md` only under `90. Settings/` and `90. Settings/02 Templates/`, placement-guide/template paths, preserved provenance, protected `## Thinking`, no machine-home paths, and no claim that plugin IDs, bundled `data.json`, or `cssTheme: Minimal` mean those packages are installed. Formatters, commits, pushes, and index rebuilds are not mandatory for guide edits.
