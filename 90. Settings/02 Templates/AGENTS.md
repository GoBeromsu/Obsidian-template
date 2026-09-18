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

These files use Templater `<% %>` syntax. Core Templates is enabled in `../../.obsidian/core-plugins.json` but is not this engine; no `templates.json` is shipped. Core Daily notes is enabled; `../../.obsidian/daily-notes.json` sets folder `10. Time/01 Daily Notes`, format `YYYY-MM-DD`, and no core template. `periodic-notes` is not in the plugin ID list and is not used.

Templater folder rules are preloaded in `../../.obsidian/plugins/templater-obsidian/data.json`: template folder `90. Settings/02 Templates`, `trigger_on_file_creation_mode: folder`, and folder templates for Daily / Weekly / Monthly / Quarterly / Yearly only. There is **no** folder template for `10. Time/06 Dashboard`. That `data.json` is config, not the Templater binary; install and enable Templater before `<% %>` runs.

Wikilinks are navigation only; they do not create targets. After the Daily template runs, it may `tp.file.create_new` missing `10. Time/06 Dashboard/YYYY-MM-DD Dashboard.md` files for yesterday, today, and tomorrow. It does not create weekly, monthly, quarterly, or yearly notes. Scripts parse `tp.file.title`; untitled-then-rename races fall back to "now".

## Key Directories

| Path | Role |
| --- | --- |
| `auto/` | Periodic files. Folder templates (except Dashboard) are preloaded in Templater `data.json`. |
| `manual/` | On-demand insert (`note.template.md`, `task.template.md`, `project.template.md`, `log.template.md`, `video.template.md`, `book.template.md` via the Templater modal) |

Only `auto/` and `manual/` are shipped. Do not invent extra Templater categories.

| Template | Folder | Title format | Folder template? |
| --- | --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | Yes |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` plus `W` (example `2026-03W`) | Yes |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` | Yes |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-QN` | Yes |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` | Yes |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | **No** — Daily hook only |

If both a folder template and another applicator hit the same folder, Templater can run twice. Do not add a folder template on `10. Time/06 Dashboard`; dashboards created by the Daily hook would double-process.

## Development Commands

No template build, test, CLI-init, or git-init command exists; none is claimed to have run. Do not launch Obsidian to apply templates. Optional Git review belongs to the parent task. Do not edit `<% %>` bodies unless the assignment names those files.

Documented adopter commands (not executed here): command palette **Daily notes: Open today's daily note**; create `10. Time/01 Daily Notes/2026-01-15.md` for a generic dated example; **Templater: Insert Template** → `manual/task.template.md` into `15. Work/04 Tasks/`. Example dates `2026-01-14` / `2026-01-15` / `2026-01-16` are documentation only.

## Code Conventions & Common Patterns

- Keep `*.template.md` names and current engine syntax. Human-facing stamps stay `created_by: user` and `authorship: user`; do not layer a second metadata contract for ordinary template use.
- Preserve `## Thinking` headings in Daily and Dashboard templates. After instantiation, `## Thinking` is human-only.
- Embedded ` ```base ` blocks need core Bases (enabled). Dashboard Overdue needs Dataview installed; the ID in `community-plugins.json` is not install proof. No custom Bases `type: timeline` view is shipped.
- `manual/task.template.md` fields that Dashboard Tasks query: `type` (`task`), `done`, `gtd`, `project`, `plan`, `due`, plus `aliases`, `date_created`, `date_modified`, `date_finished`, `created_by`, `authorship`, `tags`. Views: Today (`done != true` and `plan` or `due` ISO-date ≤ today), Due soon (`due` set), Delegation (`gtd == "delegation"`). There is no `scheduled` key.
- New agent-authored notes outside these templates use the local note convention `created_by: agent` and `authorship: agent`. Report schema conflicts instead of rewriting template frontmatter.

## Important Files

- `../../AGENTS.md` and `../AGENTS.md` — parent agent contracts.
- `README.md` and `README.ko.md` — equivalent engine setup, folder mapping, navigation versus creation, example workflow.
- `../../README.md` and `../../README.ko.md` — equivalent vault start guides.
- `../01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `auto/Daily Note.template.md` — only shipped creator besides the opened note (dashboards for yesterday/today/tomorrow).
- `auto/Dashboard.template.md` — applied by that Daily hook, not by a folder template.
- `manual/note.template.md` — generic insert template (`date_created` / `date_modified` via `tp.date.now("YYYY-MM-DD")`).
- `manual/task.template.md` — task insert whose fields match Dashboard Tasks.
- `manual/project.template.md` and `manual/log.template.md` — minimal project hub and dated log inserts; no automatic creation or folder mapping. Link the adopter's reviewed `me` context, not a duplicate profile.
- `manual/video.template.md` (`type: video`; `author`, `source_url`, `date_published`, `image`) and `manual/book.template.md` (`type: book`; `author`, `status`, `total_page`, `cover_url`) — source-note inserts whose property names are read by `../05 Bases/Video.base` and `Books.base`. Keep the names identical on both sides; a renamed property empties the Base view.
- `../../.obsidian/daily-notes.json` — preloaded Daily notes folder and format; core template empty.
- `../../.obsidian/plugins/templater-obsidian/data.json` — preloaded Templater folder rules (config, not binaries).

## Runtime/Tooling Preferences

Install and enable Templater before `<% %>` runs. Folder location and the five period folder templates (not Dashboard) are preloaded; do not treat `data.json` as an installed plugin. `.obsidian/plugins/` holds allowlisted `data.json` files only; plugin binaries and `.obsidian/themes/` are not shipped. IDs and `cssTheme: Minimal` are not installations. Core Daily notes creates daily files only; the Daily hook creates dashboards once.

Drawings belong in `../07 Excalidraw` (`90. Settings/07 Excalidraw`). Excalidraw `data.json` is path config; parent owns plugin path migration. No Handbook.

## Testing & QA

Check `auto/` versus `manual/`, title-format parsers, Daily dashboard-only creation (no period cascade), Dashboard **not** folder-mapped, navigation-only wikilinks, preserved Templater syntax and human provenance stamps, protected `## Thinking`, task fields matching Dashboard queries, bilingual README pair with no language precedence, config-versus-binary distinction for `.obsidian/plugins/`, drawings root `90. Settings/07 Excalidraw` with no stale Collections Excalidraw route, and no claim of a live Obsidian end-to-end run or package install from IDs or `data.json`.
