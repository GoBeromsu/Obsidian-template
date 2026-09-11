---
created_by: gjc
authorship: agent
---
<!-- Parent: ../AGENTS.md -->

# Repository Guidelines

## Project Overview

`90. Settings/` is vault infrastructure: placement rules, Templater files, and empty home / index / Bases placeholders. Changes here can affect the whole vault. Inherit `../AGENTS.md`. Do not copy the ten-root table here.

Human guides in this tree are English/Korean pairs: equivalent translations of one contract, not two note homes. Neither language outranks the other. When instructions change, update both files.

## Architecture & Data Flow

Placement SSOT is the bilingual Placement Guide under `01 Guideline/`. Templates live under `02 Templates/` (`auto/` periodic, `manual/` on-demand). Standalone home, index, and Bases folders ship empty; periodic views that exist are embedded in templates. `.obsidian/` is a sibling of this folder at vault root, not inside it.

Do not add Handbook folders, extra Templater categories, or nested `AGENTS.md` under `03 Home/`, `04 Index/`, or `05 Bases/`. Child agent contract: `02 Templates/AGENTS.md`.

## Key Directories

| Path | Role |
| --- | --- |
| `01 Guideline/` | Placement Guide pair (`01. Placement Guide.md`, `01. Placement Guide.ko.md`) |
| `02 Templates/` | Templater root: `auto/`, `manual/`, bilingual README, nested `AGENTS.md` |
| `03 Home/` | Empty home placeholder |
| `04 Index/` | Empty index placeholder |
| `05 Bases/` | Empty standalone Bases placeholder |

## Development Commands

No Settings-specific build, test, CLI-init, or git-init command exists; none is claimed to have run. Optional review, if the adopter uses Git: `git status --short` and `git diff --check`. Do not launch Obsidian. Parent verification owns formatters and index checks.

## Code Conventions & Common Patterns

- Read `../AGENTS.md`, this file, then `02 Templates/AGENTS.md` before editing settings or templates.
- Existing notes need exact-path or deterministic-manifest authorization. Preserve YAML provenance. Authorized edits to user-created notes keep `created_by: user` and set `authorship: mixed`.
- `## Thinking` is human-only. Do not overwrite another writer's note, delete to resolve conflicts, or reorganize beyond the task.
- Keep Templater syntax and `.base` files as they are. Do not layer a second metadata schema on human template stamps (`created_by: user`, `authorship: user`).
- Record root add/rename/renumber decisions in both Placement Guide files. Do not treat empty placeholders as populated.

## Important Files

- `../AGENTS.md` — template-root agent contract and ten-root map.
- `../README.md` and `../README.ko.md` — equivalent start guides.
- `01 Guideline/01. Placement Guide.md` and `01. Placement Guide.ko.md` — equivalent placement contracts.
- `02 Templates/AGENTS.md` — auto/manual, engines, dates.
- `02 Templates/README.md` and `README.ko.md` — equivalent Templater and optional Daily notes setup.

## Runtime/Tooling Preferences

Plugin IDs live in `../.obsidian/community-plugins.json`; they are not installations. Confirm `../.obsidian/plugins/` and `../.obsidian/themes/` before depending on a plugin or theme; this template ships neither. `appearance.json` names Minimal; two snippets under `../.obsidian/snippets/` are shipped. Core Bases is on; core Daily notes is off; no `daily-notes.json` or Templater `data.json` is shipped. `periodic-notes` is unused. Configure engines from the bilingual template READMEs, not by assuming preloaded folder templates.

## Testing & QA

Confirm inheritance to `../AGENTS.md`, bilingual pairs updated together, no duplicated root taxonomy, empty `03 Home/` / `04 Index/` / `05 Bases/`, no extra `AGENTS.md` in those folders, no Handbook path, preserved provenance and `## Thinking`, unchanged template/config files unless assigned, and no claim that plugin IDs or `cssTheme: Minimal` mean packages are installed.
