<div align="center">
  <h1>Obsidian Template</h1>
  <p><strong>A home for your notes. A system for your thinking.</strong></p>
  <p>PARA organization, Zettelkasten thinking, and periodic planning — with shared rules for humans and AI agents.</p>
  <p>
    <strong>English</strong> ·
    <a href="README.ko.md">한국어</a>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Obsidian-7C3AED?style=flat&amp;logo=obsidian&amp;logoColor=white" alt="Obsidian" />
    <img src="https://img.shields.io/badge/Markdown-000000?style=flat&amp;logo=markdown&amp;logoColor=white" alt="Markdown" />
    <img src="https://img.shields.io/badge/EN%20%7C%20KO-bilingual-1F6FEB?style=flat" alt="Bilingual English and Korean" />
  </p>
  <p>
    <a href="90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md">Placement</a>
    ·
    <a href="90.%20Settings/02%20Templates/README.md">Templates</a>
    ·
    <a href="AGENTS.md">Agent guidelines</a>
  </p>
</div>

## Less organizing. More connecting.

Start with a working structure, not someone else's personal notes. Give each note one canonical home, connect ideas across projects, and plan from year to day. Humans and agents share the same placement rules.

- **One home per note.** File by what the note is, not who wrote it or which tool captured it.
- **PARA plus Zettelkasten.** Projects and areas stay separate from literature notes and evergreen ideas.
- **A planning chain that matches review.** Folder numbers are labels; the hierarchy is the period chain.
- **Portable on purpose.** Personal notes, credentials, plugin caches, plugin binaries, theme binaries, and machine-specific state are not included.

## Features

| Feature | What you get |
| --- | --- |
| Numbered PARA layout | Ten roots; one canonical path per note |
| Zettelkasten split | Source-derived thinking in Literature Notes; self-contained ideas in Permanent Notes |
| Periodic planning | Templater `auto/` notes for year, quarter, month, week, day, and dashboards |
| Agent-readable rules | Nested `AGENTS.md` at vault root, Settings, and Templates |
| Embedded views | Core Bases tables in period templates; Dashboard Overdue needs Dataview |
| Empty placeholders | Home, indexes, and standalone Bases folders are yours to fill |

## Capture to work

This is a filing model, not an automatic pipeline. Nothing here moves notes for you.

**Capture** (`00. Inbox`) → **original** (`85. Raw`) · **interpretation** (`30. Literature Notes`) · **idea** (`40. Permanent Notes`) · **work** (`15. Work`)

Keep captured originals in Raw regardless of collector. Create work under a project or area only when the note has an owner. Read the [Placement Guide](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md) before filing the first note.

## Roots

Ten roots are shipped. Extra folders from a personal vault are not part of this template.

| Root | Role |
| --- | --- |
| `00. Inbox` | Unsorted capture |
| `10. Time` | Daily, weekly, monthly, quarterly, yearly, and dashboards |
| `15. Work` | Projects, areas, archive, and tasks |
| `30. Literature Notes` | Research, reviews, and meetings derived from a source |
| `40. Permanent Notes` | Ideas and principles that stand on their own |
| `50. AI` | AI-generated or synthesized material with no owning project |
| `70. Collections` | People, prompts, MOCs, music, places, Excalidraw, organizations, GitHub, channels |
| `80. References` | Books, papers, and attachments |
| `85. Raw` | Captured external originals |
| `90. Settings` | Rules, templates, home, indexes, and bases |

`70. Collections/06 Excalidraw` is present as an empty folder.

## Time

Planning hierarchy: **Year → Quarter → Month → Week → Day**. Folder numbers are not that hierarchy.

Daily titles are `YYYY-MM-DD`. Weekly titles are ISO week year `GGGG-WW` plus `W` (example `2026-37W`). Period wikilinks are navigation only. Creating a daily note can create missing dashboards for yesterday, today, and tomorrow; it does not create week, month, quarter, or year notes.

Formats, ISO weeks, and Templater mapping: [Placement Guide](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md) · [Templates](90.%20Settings/02%20Templates/README.md).

## Quick start

1. **Clone and open as a vault**

   ```sh
   git clone https://github.com/GoBeromsu/Obsidian-template.git
   ```

   Open the cloned folder as a new vault in Obsidian. Copying the directory works the same way.

2. **Install what the templates need**

   In Obsidian, install community plugins from **Settings → Community plugins**. [Templater](https://github.com/SilentVoid13/Templater) is required for `auto/` and `manual/` templates to run. Install Dataview if you want the Dashboard Overdue query. IDs in `community-plugins.json` are not installations.

3. **Configure paths**

   Follow [Templates](90.%20Settings/02%20Templates/README.md) for Templater (template folder `90. Settings/02 Templates`, then folder templates) and, if you want the Daily notes command, for enabling core Daily notes. Core Daily notes is off until you configure it. Core Bases is already enabled.

4. **Capture, then file**

   Read the [Placement Guide](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md) first. Drop unsorted capture into `00. Inbox`. Create work under `15. Work/01 Project` or `15. Work/02 Area` when a note has an owner. Keep system files in `90. Settings`.

These steps are setup instructions, not a claim that periodic creation, Bases views, or theme appearance were end-to-end verified in Obsidian.

## Agent guidelines

Read the nearest contract before creating or moving a note. Human guides ship as English/Korean pairs; neither language outranks the other.

| Layer | Role |
| --- | --- |
| [Vault](AGENTS.md) | Ten-root map and vault-wide conventions |
| [Settings](90.%20Settings/AGENTS.md) | Placement SSOT, empty home/index/bases, settings-layer rules |
| [Templates](90.%20Settings/02%20Templates/AGENTS.md) | `auto/` vs `manual/`, title formats, navigation vs creation |

<details>
<summary>Plugins, theme, and setup limits</summary>

`.obsidian/community-plugins.json` lists plugin **IDs** only. This template has no `.obsidian/plugins/` directory.

`.obsidian/appearance.json` sets `cssTheme` to `Minimal` and enables two shipped snippets under `.obsidian/snippets/`. There is no `.obsidian/themes/` directory. Install [Minimal](https://github.com/kepano/obsidian-minimal) yourself if you want that theme, or change the theme. `obsidian-minimal-settings` is an ID only.

`.obsidian/core-plugins.json` enables core Bases and core Templates, and leaves **Daily notes disabled**. There is no `.obsidian/daily-notes.json`. Templater settings are not shipped (`templater-obsidian` is an ID only). Core Templates is not the engine for `<% %>` files.

Excalidraw is required only if you store drawings in `70. Collections/06 Excalidraw`. The `periodic-notes` plugin is not in the ID list and is not used.

</details>

<details>
<summary>Periodic links do not cascade</summary>

Wikilinks in the periodic templates are navigation only. There is no automatic period cascade.

The shipped Daily template can create missing dashboards for yesterday, today, and tomorrow. It does not create weekly, monthly, quarterly, or yearly notes. See [Templates](90.%20Settings/02%20Templates/README.md).

Core Daily notes, if you enable it, creates daily files only.

</details>
