# Ataraxia Vault Template

[한국어](README.ko.md)

A portable Obsidian vault skeleton derived from a personal knowledge system. It keeps a numbered PARA-like layout, one canonical location per note, and all system rules under `90. Settings`. Personal notes, credentials, plugin caches, plugin binaries, theme binaries, and machine-specific state are not included.

Open this folder as a new vault in Obsidian. Capture into `00. Inbox`, then file each note using [90. Settings/01 Guideline/01. Placement Guide.md](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md). Periodic note templates live under `90. Settings/02 Templates`; home notes, indexes, and standalone Bases files are empty placeholders for you to add.

## Roots

Ten roots are shipped. Do not treat extra personal-vault roots as part of this template.

- `00. Inbox` — unsorted capture; file notes from here as soon as their destination is clear.
- `10. Time` — periodic planning and review (daily, weekly, monthly, quarterly, yearly, plus dashboards).
- `15. Work` — projects with an end condition, ongoing areas, finished work, and tasks.
- `30. Literature Notes` — thinking derived from an external source (research, reviews, meetings).
- `40. Permanent Notes` — self-contained ideas and principles that stand on their own.
- `50. AI` — AI-generated or AI-synthesized material that has no owning project.
- `70. Collections` — reusable catalogs of people, prompts, maps of content, music, places, Excalidraw drawings, organizations, GitHub, and channels. `70. Collections/06 Excalidraw` is present as an empty folder.
- `80. References` — books, papers, and attachments.
- `85. Raw` — captured external originals, regardless of who or what captured them.
- `90. Settings` — vault rules, templates, home, indexes, and bases.

## Shipped settings versus what you must install

`.obsidian/community-plugins.json` is a list of plugin **IDs**. It does not install plugins. This template has no `.obsidian/plugins/` directory.

`.obsidian/appearance.json` sets `cssTheme` to `Minimal` and enables two shipped snippets under `.obsidian/snippets/`. There is no `.obsidian/themes/` directory, so Minimal is not installed until you add it (or change the theme). `obsidian-minimal-settings` is an ID only.

`.obsidian/core-plugins.json` enables core Bases and the core Templates plugin, and leaves **Daily notes disabled**. There is no `.obsidian/daily-notes.json`. Templater settings are not shipped (`templater-obsidian` is an ID only).

`90. Settings/02 Templates/auto/Daily Note.template.md` **is** shipped. Creating a daily note from it can create missing dashboards for yesterday, today, and tomorrow. It does not create weekly, monthly, quarterly, or yearly notes. Wikilinks in the periodic templates are navigation only.

## Daily and weekly naming

Daily notes are titled `YYYY-MM-DD` in `10. Time/01 Daily Notes`. Weekly notes are titled with the ISO week year `GGGG-WW` plus `W` (example: `2026-37W`) in `10. Time/02 Weekly Notes`. Daily notes write `week` as that same weekly title; use it when you create the weekly note.

There is no automatic period cascade. Wikilinks in the periodic templates are navigation only.

Folder, format, and Templater steps are in [90. Settings/02 Templates/README.md](90.%20Settings/02%20Templates/README.md).

## How to start

1. Copy or clone this directory and open it as an Obsidian vault.
2. Read [90. Settings/01 Guideline/01. Placement Guide.md](90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md) before filing the first note.
3. Install only the community plugins and theme you will use. In Obsidian, install plugins from **Settings → Community plugins** and themes from **Appearance → Themes**. [Templater](https://github.com/SilentVoid13/Templater) is required for the `auto/` and `manual/` templates to run. Dataview is required for the Dashboard Overdue query. Excalidraw is required only if you store drawings in `70. Collections/06 Excalidraw`. The [Minimal](https://github.com/kepano/obsidian-minimal) theme is named in `appearance.json` but not shipped as files. IDs in `community-plugins.json` are not a substitute for installation.
4. Configure Templater and, if you want the Daily notes command, enable and configure core Daily notes. Exact folder, format, and template paths are in [90. Settings/02 Templates/README.md](90.%20Settings/02%20Templates/README.md).
5. Drop unsorted capture into `00. Inbox`.
6. Create work under `15. Work/01 Project` or `15. Work/02 Area` when a note has an owner.
7. Keep captured originals in `85. Raw`; keep system files in `90. Settings`.

These steps are setup instructions, not a claim that periodic creation, Bases views, or theme appearance were end-to-end verified in Obsidian.
