---
created_by: agent
authorship: agent
---
# Templates

[English](README.md) · [한국어](README.ko.md)

Related: [Start (English)](../../README.md) · [시작 (한국어)](../../README.ko.md) · [Placement Guide](../01%20Guideline/01.%20Placement%20Guide.md) · [배치 가이드](../01%20Guideline/01.%20Placement%20Guide.ko.md) · [Agent contract](AGENTS.md)

These are [Templater](https://github.com/SilentVoid13/Templater) templates. The `periodic-notes` plugin is not in this template's plugin ID list and is not used.

`community-plugins.json` listing `templater-obsidian` (or Dataview, Excalidraw, Minimal Theme Settings) does **not** install those plugins. This vault ships allowlisted plugin **config** at `.obsidian/plugins/templater-obsidian/data.json` and `.obsidian/plugins/obsidian-excalidraw-plugin/data.json`. Those files are path and folder-template settings, not plugin binaries. `.obsidian/themes/` is not shipped. Install and enable Templater before any `<% %>` template will run.

## `auto/` versus `manual/`

| Folder | Role |
| --- | --- |
| `auto/` | Periodic templates. Templater **Folder templates** (preloaded except Dashboard) apply these when a file is created in the mapped folder. |
| `manual/` | On-demand templates. Invoke from the Templater insert modal. |

`auto/` is a folder name, not an automatic runner. Nothing in this template executes these files unless Templater is installed and enabled. Core Daily notes is **enabled** in `.obsidian/core-plugins.json` with `.obsidian/daily-notes.json`. Templater folder rules are in `.obsidian/plugins/templater-obsidian/data.json`. Until Templater is installed and enabled, creating a file under `10. Time/` does not apply these templates.

Every shipped template file uses the `*.template.md` suffix:

- `auto/Daily Note.template.md`
- `auto/Weekly Notes.template.md`
- `auto/Monthly Notes.template.md`
- `auto/Quarterly Notes.template.md`
- `auto/Yearly Note.template.md`
- `auto/Dashboard.template.md`
- `manual/note.template.md`
- `manual/task.template.md`
- `manual/project.template.md`
- `manual/log.template.md`

## Engine setup (Daily notes and Templater folders are preloaded)

Core Daily notes settings and the minimal Templater folder-template list are already in the shipped JSON. That is config, not a live plugin install and not a verified Obsidian run. Core Templates is enabled in `core-plugins.json`, but no `templates.json` is shipped; do not confuse it with Templater.

### Templater (install still required)

1. Install and enable Templater. `data.json` does nothing until the plugin binary is present.
2. **Template folder location** is preloaded as `90. Settings/02 Templates` (vault-relative). That is the folder for the insert modal; `auto/` and `manual/` both sit under it.
3. **Trigger on new file creation** is preloaded as folder mode (`trigger_on_file_creation_mode: folder`): Templater runs only for folders in the list below.
4. **Folder templates** are preloaded for these rows only:

| Folder | Template |
| --- | --- |
| `10. Time/01 Daily Notes` | `90. Settings/02 Templates/auto/Daily Note.template.md` |
| `10. Time/02 Weekly Notes` | `90. Settings/02 Templates/auto/Weekly Notes.template.md` |
| `10. Time/03 Monthly Notes` | `90. Settings/02 Templates/auto/Monthly Notes.template.md` |
| `10. Time/05 Quarterly Notes` | `90. Settings/02 Templates/auto/Quarterly Notes.template.md` |
| `10. Time/04 Yearly Notes` | `90. Settings/02 Templates/auto/Yearly Note.template.md` |

**Do not** add a folder template for `10. Time/06 Dashboard`. The Daily hook creates dashboards with `tp.file.create_new` and `auto/Dashboard.template.md` once. Mapping that folder double-applies the Dashboard template.

If both a folder template and another mechanism apply the same file, Templater can run twice. Pick one applicator per folder.

### Core Daily notes (preloaded)

Core **Daily notes** is enabled. `.obsidian/daily-notes.json` is:

- New file location: `10. Time/01 Daily Notes`
- Date format: `YYYY-MM-DD` (the Daily template parses that title)
- Template file: empty (no core template). Templater's Daily folder template applies `auto/Daily Note.template.md`. Do not fill the Daily notes template field, or both engines can run.

Core Daily notes creates daily files only. It does not create weekly, monthly, quarterly, yearly, or dashboard notes. The Daily template's hook creates missing dashboards after the daily note is written.

## Commands and a worked example

Generic example date: **2026-01-15** (yesterday `2026-01-14`, tomorrow `2026-01-16`, ISO week `2026-03W`, month `2026-01`). These dates are documentation only; this is not a claim that an Obsidian UI run was performed.

1. **Create the dated Daily note.** Command palette → **Daily notes: Open today's daily note** when the vault date is that day. For the example date regardless of clock, create `10. Time/01 Daily Notes/2026-01-15.md` in that folder so the Daily folder template runs.
2. **Linked dashboards.** After the Daily template finishes, it tries to create missing files:
   - `10. Time/06 Dashboard/2026-01-14 Dashboard.md`
   - `10. Time/06 Dashboard/2026-01-15 Dashboard.md`
   - `10. Time/06 Dashboard/2026-01-16 Dashboard.md`
   using `auto/Dashboard.template.md` via `tp.file.create_new`. It does **not** create `2026-03W`, `2026-01`, `2026-Q1`, or `2026`.
3. **Task demonstration.** Create `15. Work/04 Tasks/2026-01-15 Example task.md`. Command palette → **Templater: Insert Template** → `manual/task.template.md`. Set `plan: 2026-01-15` and/or `due: 2026-01-15` so Dashboard **Today** and **Due soon** can match; set `gtd: delegation` for **Delegation**. Leave `done: false`.
4. **Open the day's Dashboard.** Open `10. Time/06 Dashboard/2026-01-15 Dashboard.md`. Core Bases **Tasks** views filter `type == "task"` on those fields. That dashboard is not folder-mapped, so the Daily hook is the single Templater pass.
5. **Sample Project hub.** Manual templates do not create files or run automatically. Create the folder `15. Work/01 Project/Sample Project`, then create an empty note named `Sample Project` at `15. Work/01 Project/Sample Project/Sample Project.md`. Command palette → **Templater: Insert Template** → `manual/project.template.md`. Review `00. Inbox/me.md`, then paste a wikilink to that reviewed note under Context (do not leave an unresolved placeholder). Fill Objective, Success criteria, Constraints, and Next action. There is no folder template on `15. Work/01 Project`.
6. **Dated project log.** Create an empty note named `2026-01-15 Sample Project log` at `15. Work/01 Project/Sample Project/2026-01-15 Sample Project log.md`. Command palette → **Templater: Insert Template** → `manual/log.template.md`. Set `project: ["[[Sample Project]]"]` (quoted hub wikilink in the list). Fill Observations, Decision, and Next action. Leave `## Thinking` empty; it is human-only.
7. **Link a project-owned task.** Create a separate task beside the hub, insert `manual/task.template.md`, and set `project: ["[[Sample Project]]"]` so Dashboard Tasks can show the owning project. The unowned task from step 3 stays in `04 Tasks`. Add the log's wikilink under the hub's Linked logs section. Wikilinks do not create the hub or the log.

Daily notes checkboxes stay on the daily note; Dashboard **Overdue** is a Dataview `TASK` query over `10. Time/01 Daily Notes` and needs Dataview installed.

**Plain Markdown without Templater.** If Templater is not installed, `<% %>` does not run. Do not copy unrendered `<% %>` into a note and treat it as valid Markdown. Write the same YAML keys by hand: `type: project` or `type: log`, `created_by: user`, `authorship: user`, unquoted ISO `date_created` / `date_modified` (for example `2026-01-15`), and on logs `project: []` until you add a quoted hub wikilink. Copy section headings from the template body, not the Templater expressions.

## Navigation versus creation

Wikilinks in frontmatter and bodies (`week`, `month`, `year`, `quarter`, previous/next period, dashboard `up`, and so on) are **navigation**. They do not create the target note.

The planning hierarchy is Year → Quarter → Month → Week → Day. Period notes point along that chain with explicit wikilinks. There is no automatic period cascade.

The Daily template is the only shipped creator besides the note you just opened. After the daily note is written, it tries to create missing yesterday / today / tomorrow dashboards only.

## Title formats

Title formats are what the scripts parse from `tp.file.title`; untitled-then-rename races fall back to "now".

| Period | Folder | Title format | Example |
| --- | --- | --- | --- |
| Day | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | `2026-01-15` |
| Week | `10. Time/02 Weekly Notes` | ISO week year `GGGG-WW` plus `W` | `2026-03W` |
| Month | `10. Time/03 Monthly Notes` | `YYYY-MM` | `2026-01` |
| Quarter | `10. Time/05 Quarterly Notes` | `YYYY-Qn` | `2026-Q1` |
| Year | `10. Time/04 Yearly Notes` | `YYYY` | `2026` |
| Dashboard | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | `2026-01-15 Dashboard` |

Weeks are ISO weeks (Monday–Sunday), matching Daily `week` values (`GGGG-WW` plus `W`). Do not use a Sunday-start week, and do not treat Sunday as belonging to the next week. Daily notes write `week` as that same title; use it when creating the weekly note.

## YAML conventions

Reuse the fields each template already emits. Do not overlay a personal metadata schema.

- Keys are `snake_case` (`created_by`, `date_created`, `date_modified`).
- Wikilink values are quoted YAML strings, for example `week: "[[2026-03W]]"` and `up: "[[2026-01-15 Dashboard]]"`.
- Plain ISO dates are unquoted, for example `date_created: 2026-01-15`.
- Human-facing stamps remain `created_by: user` and `authorship: user`.

Keep the current keys: Daily (`up`, `week`, `month`, `type`, `created_by`, `authorship`, `tags`); Weekly (`created_by`, `authorship`, `tags`, `month`, `quarter`, `roundup`, `type`); Monthly (`year`, `quarter`, `created_by`, `authorship`, `tags`); Quarterly (`year`, `quarter`, `created_by`, `authorship`, `tags`, `type`); Yearly (`created_by`, `authorship`, `tags`, `type`); Dashboard (`aliases`, `created_by`, `authorship`, `tags`, `type`, `week`); `manual/note.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`); `manual/task.template.md` (`aliases`, `type`, `done`, `gtd`, `project`, `plan`, `due`, `date_created`, `date_modified`, `date_finished`, `created_by`, `authorship`, `tags`); `manual/project.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `tags`, `aliases`); `manual/log.template.md` (`type`, `created_by`, `authorship`, `date_created`, `date_modified`, `project`, `tags`, `aliases`).

## `auto/` — periodic notes

Templater folder templates are preloaded for every row except Dashboard. Dashboard files are created by the Daily hook, not by a folder mapping.

| Template | Folder | Title format | Folder template? |
| --- | --- | --- | --- |
| `auto/Daily Note.template.md` | `10. Time/01 Daily Notes` | `YYYY-MM-DD` | Yes |
| `auto/Weekly Notes.template.md` | `10. Time/02 Weekly Notes` | `GGGG-WW` plus `W` (example: `2026-03W`) | Yes |
| `auto/Monthly Notes.template.md` | `10. Time/03 Monthly Notes` | `YYYY-MM` | Yes |
| `auto/Quarterly Notes.template.md` | `10. Time/05 Quarterly Notes` | `YYYY-Qn` (example: `2026-Q1`) | Yes |
| `auto/Yearly Note.template.md` | `10. Time/04 Yearly Notes` | `YYYY` | Yes |
| `auto/Dashboard.template.md` | `10. Time/06 Dashboard` | `YYYY-MM-DD Dashboard` | **No** (Daily hook only) |

Section headings in these templates are English for portability. Frontmatter they insert is for human-created notes (`created_by: user`, `authorship: user`); do not layer a second metadata contract on top of that for ordinary template use.

## Embedded Bases and Dataview

`90. Settings/05 Bases/` ships empty. Views that exist are **embedded** in the periodic templates.

| Location | What it is | Needs | Creates notes? |
| --- | --- | --- | --- |
| Weekly `Daily Notes` | Core Bases **table** of files in `10. Time/01 Daily Notes` whose basename falls in that week's date range | Core Bases (already enabled in `core-plugins.json`); matching daily files | No |
| Monthly `Weeks in This Month` | Core Bases **table** of notes tagged for weekly plans whose `month` property contains the monthly title | Core Bases; weekly notes that match the filter | No |
| Quarterly `Months in Quarter` | Core Bases **table** of monthly-plan notes in `10. Time/03 Monthly Notes` | Core Bases; matching monthly files | No |
| Dashboard `Tasks` | Core Bases **tables** filtered on `type == "task"` plus `done`, `plan`, `due`, `gtd`, `project` | Core Bases; task notes with those properties | No |
| Dashboard `Timeline` | Core Bases **tables** named Created Today and Modified Today | Core Bases | No |
| Dashboard `Overdue` | Dataview `TASK` query over `10. Time/01 Daily Notes` | Dataview installed and enabled | No |

Dashboard **Tasks** views in `auto/Dashboard.template.md` (match these fields on `manual/task.template.md`):

| View | Filter |
| --- | --- |
| Today | `type == "task"` and `done != true` and (`plan` is an ISO date on or before today, or `due` is an ISO date on or before today) |
| Due soon | `type == "task"` and `done != true` and `due` is set |
| Delegation | `type == "task"` and `gtd == "delegation"` and `done != true` |

There is no `scheduled` key. Use `plan` and `due` as `YYYY-MM-DD`. Default `gtd` on the task template is `inbox`. `project` is a list (empty `[]` is valid).

There is no custom Bases `type: timeline` view in this template, and no timeline-for-bases (or equivalent) plugin ID. If you expected Gantt or timeline bars, they are excluded; the Dashboard Timeline section is ordinary tables. Empty folders produce empty views. None of this was end-to-end verified in the Obsidian UI.

Yearly notes have previous/next and quarter wikilinks only. No embedded Base.

## `manual/` — on demand

`manual/note.template.md` is the generic new-note template. `manual/task.template.md` is the task note whose fields match Dashboard Tasks. `manual/project.template.md` is the project hub (`type: project`, no `status`). `manual/log.template.md` is the dated log (`type: log`, `project: []` for a quoted hub wikilink). Invoke them from the Templater insert modal after you create and name the file. They do not create files, folders, or other notes, and they do not run automatically. There is no folder template on `15. Work/01 Project` or `15. Work/04 Tasks`.

## Drawings

Excalidraw drawings and assets belong in `90. Settings/07 Excalidraw`, not in a Handbook and not as a Collections catalog. The allowlisted Excalidraw `data.json` is folder-path config (`folder`, library / script / font subpaths). Parent owns plugin path migration. Install the Excalidraw plugin before that config applies. This template does not ship Excalidraw binaries.
