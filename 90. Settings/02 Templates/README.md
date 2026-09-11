# Templates

[English](README.md) · [한국어](README.ko.md)

Related: [Start (English)](../../README.md) · [시작 (한국어)](../../README.ko.md) · [Placement Guide](../01%20Guideline/01.%20Placement%20Guide.md) · [배치 가이드](../01%20Guideline/01.%20Placement%20Guide.ko.md) · [Agent contract](AGENTS.md)

These are [Templater](https://github.com/SilentVoid13/Templater) templates. The `periodic-notes` plugin is not in this template's plugin ID list and is not used.

`community-plugins.json` listing `templater-obsidian` (or Dataview, Excalidraw, Minimal Theme Settings) does **not** install those plugins. This vault ships **no** `.obsidian/plugins/` directory and **no** `.obsidian/themes/` directory. Install Templater before any `<% %>` template will run.

## `auto/` versus `manual/`

| Folder | Role |
| --- | --- |
| `auto/` | Periodic templates. Point Templater **Folder templates** (or an equivalent insert-on-create path) at these files. |
| `manual/` | On-demand templates. Invoke from the Templater insert modal. |

`auto/` is a folder name, not an automatic runner. Nothing in this template executes these files by itself. Core Daily notes is currently **disabled** in `.obsidian/core-plugins.json`, and this template does not ship Templater `data.json` or core `daily-notes.json`. Until you install Templater and configure the exact paths below, creating a file under `10. Time/` does not apply these templates.

Every shipped template file uses the `*.template.md` suffix:

- `auto/Daily Note.template.md`
- `auto/Weekly Notes.template.md`
- `auto/Monthly Notes.template.md`
- `auto/Quarterly Notes.template.md`
- `auto/Yearly Note.template.md`
- `auto/Dashboard.template.md`
- `manual/note.template.md`

## Engine setup (not preloaded)

This template does not ship Templater `data.json` or core `daily-notes.json`. Core Daily notes is **disabled** in `.obsidian/core-plugins.json`. Core Templates is enabled there, but no `templates.json` is shipped; do not confuse it with Templater. The steps below are what the files are written for, not a verified live vault.

### Templater

1. Install and enable Templater.
2. Set **Template folder location** to `90. Settings/02 Templates` (vault-relative). That is the folder for the insert modal; `auto/` and `manual/` both sit under it.
3. Enable **Trigger Templater on new file creation**.
4. Add **Folder templates** for each row in the tables below that you actually create by dropping a file into that folder (or by a command that creates the file there first).

If both a folder template and another mechanism apply the same file, Templater can run twice. Pick one applicator per folder.

### Core Daily notes (optional)

Use this only if you want Obsidian's Daily notes command. It is off until you enable it.

1. Enable the core **Daily notes** plugin.
2. New file location: `10. Time/01 Daily Notes`
3. Date format: `YYYY-MM-DD` (the Daily template parses that title)
4. Template file: leave empty if a Templater folder template already targets `10. Time/01 Daily Notes`. Otherwise set it to `90. Settings/02 Templates/auto/Daily Note.template.md`.

Core Daily notes creates daily files only. It does not create weekly, monthly, quarterly, yearly, or dashboard notes.

## Navigation versus creation

Wikilinks in frontmatter and bodies (`week`, `month`, `year`, `quarter`, previous/next period, dashboard `up`, and so on) are **navigation**. They do not create the target note.

The planning hierarchy is Year → Quarter → Month → Week → Day. Period notes point along that chain with explicit wikilinks. There is no automatic period cascade.

The Daily template is the only shipped creator besides the note you just opened. After the daily note is written, it tries to create missing files:

- `10. Time/06 Dashboard/YYYY-MM-DD Dashboard.md` for yesterday, today, and tomorrow

using `auto/Dashboard.template.md` via Templater `tp.file.create_new`. It does **not** create weekly, monthly, quarterly, or yearly notes.

If you also set a Templater folder template on `10. Time/06 Dashboard`, dashboard files created by that Daily hook may be processed twice. Do not combine the Daily hook with a Dashboard folder template unless you accept double processing.

## Title formats

Title formats are what the scripts parse from `tp.file.title`; untitled-then-rename races fall back to "now".

| Period | Folder | Title format | Example |
| --- | --- | --- | --- |
| Day | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | `2026-09-11` |
| Week | `10. Time/02 Weekly Notes` | ISO week year `GGGG-WW` plus `W` | `2026-37W` |
| Month | `10. Time/03 Monthly Notes` | `YYYY-MM` | `2026-09` |
| Quarter | `10. Time/05 Quarterly Notes` | `YYYY-Qn` | `2026-Q1` |
| Year | `10. Time/04 Yearly Notes` | `YYYY` | `2026` |
| Dashboard | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | `2026-09-11 Dashboard` |

Weeks are ISO weeks (Monday–Sunday), matching Daily `week` values (`GGGG-WW` plus `W`). Do not use a Sunday-start week, and do not treat Sunday as belonging to the next week. Daily notes write `week` as that same title; use it when creating the weekly note.

## YAML conventions

Reuse the fields each template already emits. Do not overlay a personal metadata schema.

- Keys are `snake_case` (`created_by`, `date_created`, `date_modified`).
- Wikilink values are quoted YAML strings, for example `week: "[[2026-37W]]"` and `up: "[[2026-09-11 Dashboard]]"`.
- Plain ISO dates are unquoted, for example `date_created: 2026-09-11`.
- Human-facing stamps remain `created_by: user` and `authorship: user`.

Keep the current keys: Daily (`up`, `week`, `month`, `type`, `created_by`, `authorship`, `tags`); Weekly (`created_by`, `authorship`, `tags`, `month`, `quarter`, `roundup`, `type`); Monthly (`year`, `quarter`, `created_by`, `authorship`, `tags`); Quarterly (`year`, `quarter`, `created_by`, `authorship`, `tags`, `type`); Yearly (`created_by`, `authorship`, `tags`, `type`); Dashboard (`aliases`, `created_by`, `authorship`, `tags`, `type`, `week`); `manual/note.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`).

## `auto/` — periodic notes

Point Templater folder templates (or an equivalent insert-on-create path) at these files.

| Template | Folder | Title format |
| --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` plus `W` (example: `2026-37W`) |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-Qn` (example: `2026-Q1`) |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` |

Section headings in these templates are English for portability. Frontmatter they insert is for human-created notes (`created_by: user`, `authorship: user`); do not layer a second metadata contract on top of that for ordinary template use.

## Embedded Bases and Dataview

`90. Settings/05 Bases/` ships empty. Views that exist are **embedded** in the periodic templates.

| Location | What it is | Needs | Creates notes? |
| --- | --- | --- | --- |
| Weekly `Daily Notes` | Core Bases **table** of files in `10. Time/01 Daily Notes` whose basename falls in that week's date range | Core Bases (already enabled in `core-plugins.json`); matching daily files | No |
| Monthly `Weeks in This Month` | Core Bases **table** of notes tagged for weekly plans whose `month` property contains the monthly title | Core Bases; weekly notes that match the filter | No |
| Quarterly `Months in Quarter` | Core Bases **table** of monthly-plan notes in `10. Time/03 Monthly Notes` | Core Bases; matching monthly files | No |
| Dashboard `Tasks` | Core Bases **tables** filtered on `type == "task"` | Core Bases; task notes with those properties | No |
| Dashboard `Timeline` | Core Bases **tables** named Created Today and Modified Today | Core Bases | No |
| Dashboard `Overdue` | Dataview `TASK` query over `10. Time/01 Daily Notes` | Dataview installed and enabled | No |

There is no custom Bases `type: timeline` view in this template, and no timeline-for-bases (or equivalent) plugin ID. If you expected Gantt or timeline bars, they are excluded; the Dashboard Timeline section is ordinary tables. Empty folders produce empty views. None of this was end-to-end verified in the Obsidian UI.

Yearly notes have previous/next and quarter wikilinks only. No embedded Base.

## `manual/` — on demand

`manual/note.template.md` is the generic new-note template. Invoke it from the Templater insert modal.
