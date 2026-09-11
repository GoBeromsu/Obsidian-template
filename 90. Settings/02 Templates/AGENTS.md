---
created_by: agent
authorship: agent
---
<!-- Parent: ../AGENTS.md -->

# Repository Guidelines

## Project Overview

`02 Templates/` holds shipped Templater files for periodic Time notes (`auto/`) and on-demand insert (`manual/`). Inherit `../AGENTS.md` then `../../AGENTS.md`. Do not copy the ten-root table here.

`README.md` and `README.ko.md` are equivalent translations of one setup contract, not two note homes. Neither language outranks the other. When instructions change, update both files.

## Architecture & Data Flow

These files use Templater `<% %>` syntax. Core Templates is enabled in `../../.obsidian/core-plugins.json` but is not this engine; no `templates.json` is shipped. Core Daily notes is disabled and optional; `periodic-notes` is not in the plugin ID list and is not used. Templater `data.json` and `daily-notes.json` are not shipped.

Wikilinks are navigation only; they do not create targets. After the Daily template runs, it may `tp.file.create_new` missing `10. Time/06 Dashboard/YYYY-MM-DD Dashboard.md` files for yesterday, today, and tomorrow. It does not create weekly, monthly, quarterly, or yearly notes. Scripts parse `tp.file.title`; untitled-then-rename races fall back to "now".

## Key Directories

| Path | Role |
| --- | --- |
| `auto/` | Periodic folder-template / insert-on-create files |
| `manual/` | On-demand insert (`note.template.md` via the Templater modal) |

Only `auto/` and `manual/` are shipped. Do not invent extra Templater categories.

| Template | Folder | Title format |
| --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` plus `W` (example `2026-37W`) |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-QN` |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` |

If both a folder template and another applicator hit the same folder, Templater can run twice. A folder template on `10. Time/06 Dashboard` can double-process dashboards created by the Daily hook.

## Development Commands

No template build, test, CLI-init, or git-init command exists; none is claimed to have run. Do not launch Obsidian to apply templates. Optional Git review belongs to the parent task. Do not edit `<% %>` bodies unless the assignment names those files.

## Code Conventions & Common Patterns

- Keep `*.template.md` names and current engine syntax. Human-facing stamps stay `created_by: user` and `authorship: user`; do not layer a second metadata contract for ordinary template use.
- Preserve `## Thinking` headings in Daily and Dashboard templates. After instantiation, `## Thinking` is human-only.
- Embedded ` ```base ` blocks need core Bases (enabled). Dashboard Overdue needs Dataview installed; the ID in `community-plugins.json` is not install proof. No custom Bases `type: timeline` view is shipped.
- New agent-authored notes outside these templates use the local note convention `created_by: agent` and `authorship: agent`. Report schema conflicts instead of rewriting template frontmatter.

## Important Files

- `../../AGENTS.md` and `../AGENTS.md` — parent agent contracts.
- `README.md` and `README.ko.md` — equivalent engine setup, folder mapping, navigation versus creation.
- `../../README.md` and `../../README.ko.md` — equivalent vault start guides.
- `../01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `auto/Daily Note.template.md` — only shipped creator besides the opened note.
- `manual/note.template.md` — generic insert template (`date_created` / `date_modified` via `tp.date.now("YYYY-MM-DD")`).

## Runtime/Tooling Preferences

Install and enable Templater before `<% %>` runs. Set template folder location to `90. Settings/02 Templates`. Folder-template rows and optional core Daily notes paths are in the bilingual READMEs, not preloaded. `.obsidian/plugins/` and `.obsidian/themes/` are absent; IDs and `cssTheme: Minimal` are not installations. Core Daily notes, if enabled, creates daily files only.

## Testing & QA

Check `auto/` versus `manual/`, title-format parsers, Daily dashboard-only creation (no period cascade), navigation-only wikilinks, preserved Templater syntax and human provenance stamps, protected `## Thinking`, bilingual README pair with no language precedence, and no claim of a live Obsidian end-to-end run or package install from IDs.
