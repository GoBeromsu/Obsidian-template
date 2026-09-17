# Agent Skills

This directory holds vendored [Agent Skills](https://agentskills.io): one folder per skill, each with a `SKILL.md`.

## What is here

| Skill | Purpose | Source |
| --- | --- | --- |
| `obsidian` | Obsidian mechanics — Markdown and properties, Bases, Canvas, Mermaid, `obsidian-cli`, Web Clipper, plugin doctor, headless Sync | [GoBeromsu/craft-skills](https://github.com/GoBeromsu/craft-skills) |

## Provenance

`obsidian` is a verbatim copy of `skills/obsidian/` from [GoBeromsu/craft-skills](https://github.com/GoBeromsu/craft-skills), MIT-licensed per that repository's README.

- Vendored commit: `84f50f5600cb14c94c95557021181b9efd7af415`
- Package version: `1.2.3` (see `obsidian/CHANGELOG.md`)

Upstream is the source of truth. Send fixes there, then re-vendor here; do not fork the copy in place. To update:

```sh
git clone --depth 1 https://github.com/GoBeromsu/craft-skills.git /tmp/craft-skills
rm -rf .agents/skills/obsidian
cp -R /tmp/craft-skills/skills/obsidian .agents/skills/obsidian
git -C /tmp/craft-skills rev-parse HEAD   # record the new commit above
```

Upstream also publishes 29 other engineering and research skills, plus native plugin installs for several runtimes. Only `obsidian` is vendored here, because it is the one that serves this vault.

## Scope

These skills carry reusable Obsidian mechanics — how a Base, Canvas, or Mermaid block actually works. They do not decide where a note belongs or what it means. Placement stays with [`01. Placement Guide.md`](../../90.%20Settings/01%20Guideline/01.%20Placement%20Guide.md), writing and provenance with [`02. Writing and AI.md`](../../90.%20Settings/01%20Guideline/02.%20Writing%20and%20AI.md), and repository rules with [`AGENTS.md`](../../AGENTS.md). Where they disagree about this vault, the vault's own guides win.

The `obsidian` skill names optional prerequisites — `OBSIDIAN_VAULT_PATH`, an `obsidian-cli` binary, `ob` for headless Sync. The Markdown, Bases, Canvas, and Mermaid recipes need none of them; only the CLI and Sync recipes do. Nothing is installed by placing this folder here.
