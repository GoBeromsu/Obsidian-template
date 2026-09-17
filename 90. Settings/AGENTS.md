---
created_by: agent
authorship: agent
---
<!-- Parent: ../AGENTS.md -->

# Repository Guidelines

## Project Overview

`90. Settings/` is vault infrastructure: placement rules, Templater files, empty home / index / Bases placeholders, and Excalidraw drawings. Changes here can affect the whole vault. Inherit `../AGENTS.md`. Do not copy the ten-root table here.

Human guides in this tree are English/Korean pairs: equivalent translations of one contract, not two note homes. Neither language outranks the other. When instructions change, update both files.

## Architecture & Data Flow

Placement SSOT is the bilingual Placement Guide under `01 Guideline/`. Templates live under `02 Templates/` (`auto/` periodic, `manual/` on-demand). Standalone home, index, and Bases folders ship empty; periodic views that exist are embedded in templates. Drawings live under `07 Excalidraw/`. `.obsidian/` is a sibling of this folder at vault root, not inside it.

Do not add Handbook folders, extra Templater categories, or nested `AGENTS.md` under `03 Home/`, `04 Index/`, `05 Bases/`, or `07 Excalidraw/`. Child agent contract: `02 Templates/AGENTS.md`.

## Key Directories

| Path | Role |
| --- | --- |
| `01 Guideline/` | Placement Guide and Writing and AI pairs (English/Korean) |
| `02 Templates/` | Templater root: `auto/`, `manual/`, bilingual README, nested `AGENTS.md` |
| `03 Home/` | Empty home placeholder |
| `04 Index/` | Empty index placeholder |
| `05 Bases/` | Empty standalone Bases placeholder |
| `07 Excalidraw/` | Drawings and Excalidraw assets (number `07` avoids Handbook `06`; no Handbook in this template) |

## Development Commands

No Settings-specific build, test, CLI-init, or git-init command exists; none is claimed to have run. Optional review, if the adopter uses Git: `git status --short` and `git diff --check`. Do not launch Obsidian. Parent verification owns formatters and index checks.

## Code Conventions & Common Patterns

- Read `../AGENTS.md`, this file, then `02 Templates/AGENTS.md` before editing settings or templates.
- Existing notes need exact-path or deterministic-manifest authorization. Preserve YAML provenance. Authorized edits to user-created notes keep `created_by: user` and set `authorship: mixed`.
- `## Thinking` is human-only. Do not overwrite another writer's note, delete to resolve conflicts, or reorganize beyond the task.
- Keep Templater syntax and `.base` files as they are. Do not layer a second metadata schema on human template stamps (`created_by: user`, `authorship: user`).
- Record root add/rename/renumber decisions in both Placement Guide files. Do not treat empty placeholders as populated.
- Excalidraw drawings stay in `07 Excalidraw/`. Do not add a Handbook to hold drawings.

## Important Files

- `../AGENTS.md` — template-root agent contract and ten-root map.
- `../README.md` and `../README.ko.md` — equivalent start guides.
- `01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `01 Guideline/02. Writing and AI.md` and `02. Writing and AI.ko.md` — equivalent public writing, properties, Gemini interview, and AI-boundary guidance; no private automation or schema.
- `02 Templates/AGENTS.md` — auto/manual, engines, dates, Dashboard hook.
- `02 Templates/README.md` and `README.ko.md` — equivalent Templater and Daily notes setup (preloaded JSON, install still required).
- `02 Templates/auto/Daily Note.template.md` — Daily creator; may create dashboards only.
- `02 Templates/manual/task.template.md` — task fields matching Dashboard queries.
- `../.obsidian/daily-notes.json` — preloaded Daily notes folder `10. Time/01 Daily Notes`, format `YYYY-MM-DD`, core template empty.
- `../.obsidian/plugins/templater-obsidian/data.json` — preloaded Templater folder rules; Dashboard not mapped.
- `../.obsidian/plugins/obsidian-excalidraw-plugin/data.json` — Excalidraw folder-path config for `07 Excalidraw/` (config, not binaries). Parent owns plugin path migration.

## Runtime/Tooling Preferences

Plugin IDs live in `../.obsidian/community-plugins.json`; they are not installations. `.obsidian/plugins/` exists as an allowlist for portable **config** (`templater-obsidian/data.json`, `obsidian-excalidraw-plugin/data.json`). That is not a plugin install: binaries, `main.js`, and theme packages are not shipped. Confirm plugin binaries before depending on a plugin or theme. `appearance.json` names Minimal; two snippets under `../.obsidian/snippets/` are shipped.

Core Bases is on. Core Daily notes is on; do not assume a core Daily template. Templater folder templates cover the five period folders only; Dashboard is created once by the Daily hook. Install and enable Templater before `<% %>` runs. `periodic-notes` is unused. No Handbook.

## Testing & QA

Confirm inheritance to `../AGENTS.md`, bilingual pairs updated together, no duplicated root taxonomy, empty `03 Home/` / `04 Index/` / `05 Bases/`, drawings root `07 Excalidraw/` with no Handbook path and no stale Collections Excalidraw route, no extra `AGENTS.md` in Home/Index/Bases/Excalidraw, preserved provenance and `## Thinking`, unchanged template/config files unless assigned, config-versus-binary distinction for `.obsidian/plugins/`, and no claim that plugin IDs, `data.json`, or `cssTheme: Minimal` mean packages are installed.
