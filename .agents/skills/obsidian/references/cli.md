# obsidian-cli

## Overview

Use the installed community `notesmd-cli` (which may be exposed as `obsidian-cli`) when a vault-aware command is safer than raw filesystem access. Distinguish it from the official app's `obsidian` CLI; commands and runtime prerequisites are not interchangeable.
Treat `${OBSIDIAN_VAULT_PATH}`, `${OBSIDIAN_VAULT_NAME}`, and `${OBSIDIAN_CLI_PATH}` as the source of truth for the vault; never hardcode a host-specific vault root or vault name in skill instructions, scripts, examples, or reports.

## When to Use

- A workflow asks to read, create, search, move, open, or inspect notes in the vault through the Obsidian CLI.
- Another skill requires Obsidian-aware verification after writing a vault note.
- A workflow reports `Vault not found`, missing nested output, stale Obsidian wrapper behavior, or confusing `obsidian` versus `obsidian-cli` command results.
- Use the [`doctor.md`](doctor.md) skill instead when the task is specifically plugin/template/API debugging.

**NOT for:** reading files outside the vault; destructive vault cleanup without explicit current-turn approval; bulk raw asset operations where an Obsidian-aware operation adds no safety.

## Core Process

1. Resolve runtime prerequisites before touching the vault.
   ```bash
   : "${OBSIDIAN_VAULT_PATH:?set OBSIDIAN_VAULT_PATH}"
   : "${OBSIDIAN_VAULT_NAME:?set OBSIDIAN_VAULT_NAME}"
   : "${OBSIDIAN_CLI_PATH:=obsidian-cli}"
   "$OBSIDIAN_CLI_PATH" --version
   "$OBSIDIAN_CLI_PATH" --help
   ```
Use the installed help-supported registry lookup: `list-vaults --json` for names and paths, or `list-vaults --default` when deliberately using the default. Match `${OBSIDIAN_VAULT_NAME}` to `${OBSIDIAN_VAULT_PATH}` before note operations. An explicit `--vault` target need not be the default. If lookup is unsupported or the mapping unresolved, report it rather than guessing. Registration/default changes require task authority.

2. Use the current `obsidian-cli` command surface.
   ```bash
   "$OBSIDIAN_CLI_PATH" list-vaults --json
   "$OBSIDIAN_CLI_PATH" list --vault "${OBSIDIAN_VAULT_NAME}" "Daily Notes"
   "$OBSIDIAN_CLI_PATH" print --vault "${OBSIDIAN_VAULT_NAME}" "Daily Notes/2024-01-15.md"
   "$OBSIDIAN_CLI_PATH" search-content --vault "${OBSIDIAN_VAULT_NAME}" "query text"
   ```
Run only commands exposed by the selected binary's help. Official app commands such as `obsidian read`, `eval`, or `property:*` belong to a separate surface; their absence from community help does not mean the app lacks them. Consult the official app documentation and its own help when that surface is selected.

3. Prefer exact vault-relative paths when the target is known. Use name-based lookup only when the note title is intentionally ambiguous and the command supports that mode.

4. For generated notes or nested paths, verify materialization with a filesystem readback under `${OBSIDIAN_VAULT_PATH}` after the CLI command returns success.
   ```bash
   test -f "${OBSIDIAN_VAULT_PATH}/Roundup/2024-01-15 - GDR.md"
   "$OBSIDIAN_CLI_PATH" print --vault "${OBSIDIAN_VAULT_NAME}" "Roundup/2024-01-15 - GDR.md"
   ```
If `create` returns success but the nested file is absent, use a bounded direct write to the already-verified exact path, then repeat the readback.

5. For frontmatter or wikilink-sensitive edits, verify both CLI output and exact filesystem content. If a wikilink scalar is serialized into a list or loses one bracket layer, patch only that exact frontmatter value back to the canonical scalar form.

6. For `Vault not found` or wrapper confusion, distinguish binaries before changing anything.
   ```bash
   command -v obsidian-cli
   command -v obsidian || true
   "$OBSIDIAN_CLI_PATH" --help
   ```
Use registry inspection supported by that binary. Do not silently substitute the app CLI in a headless workflow: NotesMD works without the app running, while app commands require their documented runtime prerequisites.

7. Avoid deletion, trash, prune, unlink, or cleanup primitives unless the operator explicitly approved the exact target in the current turn. Report the target path and approval source before executing any destructive command.

## Requirements

- Community `notesmd-cli` or its `obsidian-cli` alias, available through `${OBSIDIAN_CLI_PATH}` or `PATH`, with required operations verified in installed help.
- `${OBSIDIAN_VAULT_PATH}` points to the vault root; `${OBSIDIAN_VAULT_NAME}` is the registered vault name.
- The target vault name resolves to the expected root in that CLI's registry; use explicit `--vault` selection.
- Use the [community CLI documentation](https://github.com/Yakitrak/notesmd-cli) for NotesMD and the [official app CLI documentation](https://help.obsidian.md/cli) for `obsidian`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The CLI printed success, so the note exists." | Nested `create` calls can report success without materializing the file. Verify the exact filesystem path and print the note back. |
| "The `obsidian` binary is close enough." | The official app CLI and community NotesMD CLI expose different surfaces. Verify the selected binary's version, help, and vault mapping. |
| "A full path in the example is clearer." | Host-specific paths leak runtime state. Use `${OBSIDIAN_VAULT_PATH}` plus vault-relative paths. |
| "Search output is enough to identify the note." | Search can be broad or stale. Verify the final candidate with `print` or exact readback before editing. |
| "Cleanup is part of the smoke test." | Vault deletion requires explicit current-turn approval for the exact target. Leave smoke artifacts in place or ask for approval when interactive. |

## Red Flags

- A skill, script, or example contains a literal home directory or vault root instead of `${OBSIDIAN_VAULT_PATH}`.
- A cron/headless workflow invokes `obsidian` when the verified runtime command is `obsidian-cli`.
- Completion is reported after a write without exact readback evidence.
- A wikilink frontmatter edit is trusted from stdout alone.
- Any vault file is deleted, trashed, moved, or unlinked without explicit current-turn approval.

## Verification

- [ ] `"$OBSIDIAN_CLI_PATH" --version` reports the expected installed CLI version.
- [ ] Supported registry inspection resolves `${OBSIDIAN_VAULT_NAME}` to `${OBSIDIAN_VAULT_PATH}`; no default or registry was changed merely for preflight.
- [ ] The target note is verified with `print` or exact filesystem readback after any write.
- [ ] No host-specific path or secret appears in changed package files.
- [ ] Destructive operations have explicit current-turn approval for the exact target, or are skipped.
