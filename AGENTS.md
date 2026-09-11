# Repository Guidelines

## Project Overview

This directory is a portable Obsidian vault template. It ships a 10-root skeleton, Templater files (including the Daily note template), an empty Excalidraw collection folder, and portable `.obsidian` JSON without personal notes, credentials, plugin caches, plugin or theme binaries, or machine-specific state. Faith (`60. Saint`) and publication (`25. Digital Garden`) roots are intentionally absent.

Human start, placement, and template guides ship as English/Korean pairs. The two languages are equivalent translations of one contract, not two note homes. Neither language outranks the other. When those instructions change, update both files.

Nearest nested agent contracts: `90. Settings/AGENTS.md` and `90. Settings/02 Templates/AGENTS.md`. Do not add `AGENTS.md` to empty skeleton folders.

## Architecture & Data Flow

Capture starts in `00. Inbox` and is filed with the placement guide by ownership and note kind. Each note has one canonical location. Work, time, source-derived thinking, evergreen thinking, AI, collections, references, raw originals, and settings have separate roots. `85. Raw` keeps captured external originals regardless of which collector produced them; a refined note is separate from its source.

Periodic templates under `90. Settings/02 Templates/auto/` insert navigation wikilinks and, where present, embedded Bases (and one Dataview) views. Those links and views do not create missing notes. The Daily template is the only shipped creator: after it runs, it may add dashboard files for yesterday, today, and tomorrow. It does not cascade into weekly, monthly, quarterly, or yearly notes.

`auto/` templates are for periodic Time notes (folder-template / insert-on-create). `manual/` is on-demand insert. Title formats, engines, and creation rules live in `90. Settings/02 Templates/AGENTS.md` and the bilingual template READMEs.

## Key Directories

| Path | Role |
| --- | --- |
| `00. Inbox/` | Unsorted capture awaiting triage |
| `10. Time/` | Daily, weekly, monthly, quarterly, yearly, and dashboard notes |
| `15. Work/` | Projects, areas, archive, and tasks |
| `30. Literature Notes/` | Source-derived research, reviews, and meetings |
| `40. Permanent Notes/` | Self-contained ideas and principles |
| `50. AI/` | AI-generated or AI-synthesized material without another owner |
| `70. Collections/` | Reusable people, prompts, MOCs, music, places, Excalidraw, organizations, GitHub, and channels |
| `80. References/` | Books, papers, and attachments |
| `85. Raw/` | Captured external originals |
| `90. Settings/` | Rules, templates, home, indexes, and bases |

Do not add, rename, or renumber roots without recording the decision in `90. Settings/01 Guideline/` (both language files). `90. Settings/03 Home/`, `04 Index/`, and `05 Bases/` ship empty.

## Development Commands

Open a copied or cloned template directory as an Obsidian vault. No application build, test suite, index-rebuild, CLI-init, or git-init command is defined for this template, and none of those steps is claimed to have run. When an adopter keeps the template in a Git worktree, `git status --short` and `git diff --check` are optional review commands; no commit or push is mandatory. Do not launch Obsidian implicitly.

## Code Conventions & Common Patterns

- Read this file, then the nearest nested `AGENTS.md`, then the bilingual placement and template guides before creating or moving a note. Placement SSOT: `90. Settings/01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md`.
- Ownership determines placement even when an agent wrote the content. Keep captured originals in `85. Raw` regardless of collector, and never duplicate a note across roots.
- Completed tasks stay in their current project, area, or task path; record completion according to the adopter's task policy instead of requiring a physical move.
- Periodic titles follow `90. Settings/02 Templates` (`YYYY-MM-DD`, `GGGG-WW` plus `W`, `YYYY-MM`, `YYYY-QN`, `YYYY`, `YYYY-MM-DD Dashboard`). Template files use `*.template.md` in `auto/` or `manual/`. Do not invent extra Templater categories.
- Preserve existing YAML provenance and defer metadata field names and values to the adopter's policy. Human-facing templates in this folder already stamp `created_by: user` and `authorship: user`; do not add competing metadata requirements on top of them. Local schema is `created_by: user|agent` and `authorship: user|agent|mixed`.
- Root presence does not grant write permission. Follow the adopter's local policy and exact-note authorization before editing an existing note.
- `## Thinking` sections are human-only. Do not overwrite another writer's note, delete notes to resolve conflicts, or reorganize beyond the current task.
- If an adopter adds symlinks, preserve the target layout and do not move or delete targets without the governing policy decision.

## Important Files

- `README.md` and `README.ko.md` — equivalent start guides (scope, ten roots, shipped versus installed, first-use steps).
- `90. Settings/AGENTS.md` — settings-layer agent contract.
- `90. Settings/01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `90. Settings/02 Templates/AGENTS.md` — template-layer agent contract.
- `90. Settings/02 Templates/README.md` and `README.ko.md` — equivalent Templater and optional core Daily notes setup.
- `90. Settings/02 Templates/auto/Daily Note.template.md` — shipped daily template; may create dashboards only.
- `90. Settings/02 Templates/auto/` and `manual/` — other periodic templates and the on-demand note template.
- `.obsidian/app.json`, `appearance.json`, `core-plugins.json`, and `community-plugins.json` — portable Obsidian settings. Plugin IDs are not installations. `appearance.json` names Minimal; theme files are absent. Two CSS snippets under `.obsidian/snippets/` are shipped. Core Daily notes is off.

## Runtime/Tooling Preferences

- Use Obsidian with Templater for the shipped templates. `periodic-notes` is not in `community-plugins.json` and is not used. Keep templates under `90. Settings/02 Templates`.
- Configure Templater and optional core Daily notes from the bilingual template READMEs. Do not assume folder templates or Daily notes settings are preloaded. Core Templates is enabled in `core-plugins.json` but is not the engine for `<% %>` files; no `templates.json` is shipped.
- `.obsidian/community-plugins.json` contains configured plugin IDs only. It is not an installation manifest. Confirm `.obsidian/plugins/` and `.obsidian/themes/` before depending on a plugin or theme; this template ships neither.
- Core Bases is enabled and is what the embedded ` ```base ` blocks use. Custom `type: timeline` views are not shipped. Dashboard Overdue uses Dataview, which is an ID only until installed.
- The template intentionally includes no external tool integrations or personal runtime state. Apply an adopter's local permission and provenance policy before writing notes.

## Testing & QA

There is no application build or test suite, and no end-to-end Obsidian run is claimed. Perform structural QA by checking all ten roots (including `70. Collections/06 Excalidraw` and `10. Time/01 Daily Notes`), the Daily template file, the intentional absence of `25. Digital Garden` and `60. Saint`, absence of `.obsidian/plugins/` and `.obsidian/themes/`, bilingual guide pairs (neither language treated as primary), nested `AGENTS.md` only under `90. Settings/` and `90. Settings/02 Templates/`, placement-guide/template paths, preserved provenance, protected `## Thinking`, no machine-home paths, and no claim that plugin IDs or `cssTheme: Minimal` mean those packages are installed. Formatters, commits, pushes, and index rebuilds are not mandatory for guide edits.
