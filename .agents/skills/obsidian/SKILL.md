---
name: obsidian
description: Routes one thick Obsidian skill. Use for in-vault note create/edit/cleanup (“옵시디언 노트 정리”; not filing/taxonomy) with wikilinks/callouts/properties/house style; create/debug `.base` or embedded base blocks, filters/views, `groupBy`/`sort`/`limit`, Dataview-to-Bases; Obsidian JSON Canvas `.canvas` mind maps/flowcharts/nodes/edges; Mermaid that must render in Obsidian; `obsidian-cli` read/create/search/move/property/write/inspect, readback verification, `Vault not found`, wrapper confusion; Web Clipper templates for any site/type (YouTube/GitHub/Recipe/Article), variables/filters/frontmatter; “플러그인 고쳐줘”, silent plugin failures, API skew, Templater `ReferenceError`/`<%`; or headless `ob` Sync (“headless sync 점검”, “obsidian sync status”, “볼트 동기화 복구”, “pull-only로 맞춰줘”, daemon restart). Not for web-page-to-Markdown extraction/scraping, CommonMark, Dataview queries, React Flow, Mermaid CLI/non-Obsidian rendering, outside-vault files, non-plugin core bugs, desktop Sync/Dropbox/other replication, or filing/provenance.
metadata:
  version: 1.2.3
---
# Obsidian

Apply Obsidian-specific mechanics through one package so the requested artifact follows the real format and runtime behavior while preserving unrelated vault content.

## Output contract

Return the verified artifact or runtime state, selected sub-recipe, readback evidence, and every unavailable prerequisite.
If the vault is unresolved, the runtime or command surface is unavailable or unsupported, or readback evidence is missing, stop and report the condition without inventing an operation.

## Requirements

Use only the tools required by the selected sub-recipe:

- `${OBSIDIAN_VAULT_PATH}` for an exact vault root when filesystem readback is required.
- `${OBSIDIAN_CLI_PATH}` or an `obsidian-cli` binary on `PATH` for vault-aware note operations.
- `ob` from `obsidian-headless` for the headless Sync sub-recipe.
- A real browser when Web Clipper selectors must be tested against a page.
- Runtime and release maintenance: record the relevant [Obsidian Help](https://help.obsidian.md/), [Obsidian developer documentation](https://docs.obsidian.md/), and official app, CLI, plugin API, or Sync release source. Use an installed app or CLI version probe only when current official documentation supports that exact probe; otherwise observe the version in the app and record it as unknown to automation. When probe or release evidence shows an app, CLI, plugin API, or Sync runtime form changed, recheck official documentation, rerun affected package evaluations, update the recipe if needed, then bump this package's version and append its CHANGELOG.
- The `init` skill's tool-preflight reference (`tool-preflight.md` under its references) distinguishes the Yakitrak `obsidian-cli` from the separate Obsidian.app `obsidian` binary and records their safe probes and CHANGELOG verification receipt convention.

Never hardcode a host path, vault name, account identifier, remote host, or credential.

## Route the request

| Intent | Load |
|---|---|
| Write, edit, or reformat note prose; wikilinks, embeds, callouts, properties, tags, dates, people links, or house style | [`references/markdown.md`](references/markdown.md) |
| Create, debug, or optimize a `.base` file or `base` code block | [`references/bases.md`](references/bases.md) |
| Create or edit a `.canvas` JSON Canvas graph | [`references/canvas.md`](references/canvas.md) |
| Author or repair Mermaid that must render in Obsidian | [`references/mermaid.md`](references/mermaid.md) |
| Read, create, search, move, or mutate vault notes through `obsidian-cli` | [`references/cli.md`](references/cli.md) |
| Build or debug an Obsidian Web Clipper JSON template | [`references/clipper.md`](references/clipper.md) |
| Diagnose a plugin, Templater template, plugin API, or plugin-driven script | [`references/doctor.md`](references/doctor.md) |
| Bootstrap, inspect, operate, or recover the headless `ob` Sync client | [`references/sync.md`](references/sync.md) |

Load more than one sub-recipe only when responsibilities genuinely compose.
For example, a CLI mutation of note prose uses `cli.md` for the operation and `markdown.md` for the content contract.
A Mermaid fence inside a note uses `mermaid.md` for renderer compatibility and `markdown.md` for surrounding note structure.

## Shared operating contract

1. **Resolve the exact artifact.** Identify the vault, note-relative path, `.base`/`.canvas` file, plugin id, template, or Sync pairing before changing it.
2. **Read before writing.** Preserve unrelated content, metadata, IDs, edge references, and source URLs.
3. **Apply the matching sub-recipe.** Do not substitute generic Markdown, JSON, shell file editing, or browser assumptions for Obsidian-specific behavior.
4. **Use the least destructive surface.** Prefer `obsidian-cli` for vault-aware note operations. Treat delete, unlink, reset, mirror, cleanup, and bulk replacement as destructive operations requiring explicit scope and approval.
5. **Read back the result.** Verify the exact file or runtime state after every mutation. A successful exit code without materialized output is not completion.
6. **Report evidence.** Name the verified artifact and check performed; disclose any unavailable runtime or UI check as unverified.
7. **Ground mutable runtime facts.** For Obsidian app, CLI, plugin API, or Sync behavior, consult official documentation first. Disclose conflicts; a more-specific vault-local contract or reproducible evidence for the matching app/plugin version and platform may override general or stale documentation. If unresolved, keep it unknown and stop or use the sub-recipe's safe fallback — never invent a command or capability.

## Boundaries

This package owns reusable Obsidian mechanics and formats.
A personal knowledge-management skill may own what a note means, where it belongs, required provenance, and which template frame applies; compose that policy with this package rather than duplicating it here.
Static public-page extraction belongs to an extractor such as `defuddle`, not Web Clipper or browser automation.
Generic Mermaid outside Obsidian does not inherit Obsidian’s bundled-renderer compatibility baseline.
Generic file synchronization, Git conflicts, and backup systems are outside the headless Obsidian Sync sub-recipe.

## Anti-patterns

- Loading every reference for every request → load only the selected sub-recipe and any explicitly composing neighbor.
- Editing a vault note with raw shell text tools when `obsidian-cli` is available → use the vault-aware surface and exact readback.
- Treating `.base`, `.canvas`, Mermaid, and Markdown as one syntax → route by artifact type; each has a separate parser and invariant set.
- Trusting a Web Clipper selector without testing the real page → inspect the page and verify every selector before shipping JSON.
- Editing plugin state files or bundled plugin code directly → follow `doctor.md` and use the plugin/runtime’s supported mutation surface.
- Enabling bidirectional or continuous headless Sync before a one-shot pull-only verification → follow `sync.md`’s staged promotion gate.
- Letting this reusable package decide a personal vault’s taxonomy or filing zone → load the personal policy owner for those decisions.

## Verification

- [ ] The request was routed to the correct sub-recipe.
- [ ] The exact target and applicable runtime prerequisites were verified.
- [ ] Unrelated content and metadata were preserved.
- [ ] Destructive operations had explicit approved scope or were skipped.
- [ ] The changed artifact or runtime state was read back exactly.
- [ ] Any composed sub-recipes had distinct responsibilities.
