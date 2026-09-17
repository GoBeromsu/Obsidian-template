# `ob` CLI Command Reference

The headless client is installed as the global command `ob` (npm package `obsidian-headless`).
Resolve it through `${OBSIDIAN_CLI_PATH}` when the binary is not on `PATH`.
Verify the installed release against the package registry and its release notes before changing a working replica.

## Install and inspect

```bash
npm install -g obsidian-headless       # install or upgrade
npm view obsidian-headless version     # check latest on npm
ob --version                            # check locally installed version
```

Configuration lives under `~/.obsidian-headless/` (note: **not** `~/.config/obsidian-headless/`):

- `~/.obsidian-headless/auth_token` — login token (set by `ob login`)
- `~/.obsidian-headless/sync/<vaultId>/config.json` — per-vault config
- `~/.obsidian-headless/sync/<vaultId>/state.db` — sync state database
- `~/.obsidian-headless/sync/<vaultId>/sync.log` — rolling sync log

## Command surface

```
ob login                 login to Obsidian account or show login status
ob logout                log out
ob sync-list-remote      list vaults available on the server
ob sync-list-local       list locally configured vaults
ob sync-create-remote    create a new remote vault
ob sync-setup            connect a local path to a remote vault
ob sync-config           change sync configuration for a local vault
ob sync-status           show current sync configuration for a local vault
ob sync-unlink           disconnect a local vault and remove stored credentials
ob sync                  run sync (once, or --continuous)
ob publish-*             publish-site family (different code path, out of scope)
```

## `sync-setup`

```
--vault <id-or-name>             remote vault identifier
--path <local-path>              local vault path (default: cwd)
--password <passphrase>          E2E encryption password (prompted if omitted)
--device-name <name>             label for this machine in sync history
--config-dir <name>              config directory name (default: .obsidian)
```

**Interactive password caveat:** `sync-setup` must run in a real TTY for the password prompt.
Piping `< /dev/null` fails with `Failed to validate password`.
In a Claude Code chat, use the `!` prefix so the command attaches to the user's terminal.

## `sync-config`

```
--path <local-path>              which local vault
--mode <mode>                    bidirectional | pull-only | mirror-remote
--conflict-strategy <strategy>   merge | conflict
--excluded-folders <folders>     comma-separated paths; empty string clears
--file-types <types>             image, audio, video, pdf, unsupported; empty clears
--configs <settings>             app, appearance, hotkey, core-plugin, core-plugin-data, community-plugin, community-plugin-data
--device-name <name>             change the device label
--config-dir <name>              default: .obsidian
```

**Mode semantics:**

- `bidirectional` — default. Uploads local changes and downloads remote changes.
- `pull-only` — download only. Ignores local-only additions (keeps them). Remote deletions still propagate.
- `mirror-remote` — download only. Reverts local-only additions. Destructive to local work.

**File-type note:** `--file-types` controls *attachments*.
Markdown is always synced regardless.

## `sync`

```
--path <local-path>              target vault
--continuous                     run as a long-lived daemon
```

Never enable `--continuous` in a first-sync run.
Always start with a one-shot sync and confirm the diff is expected.

## Config.json shape

A healthy `config.json` looks like this (real keys redacted):

```json
{
  "vaultId": "<32-hex>",
  "vaultName": "Vault Name",
  "vaultPath": "/absolute/path/to/vault",
  "host": "sync-XX.obsidian.md",
  "encryptionVersion": 3,
  "encryptionKey": "<base64>",
  "encryptionSalt": "<hex>",
  "conflictStrategy": "merge",
  "deviceName": "this-machine",
  "syncMode": "bidirectional",
  "fileTypes": [],
  "ignoreFolders": ["path/to/ignore"]
}
```

**`encryptionVersion: 0`** in a fresh setup is a red flag: current Obsidian Sync uses v3+.
A v0 config is almost certainly stale and should be `sync-unlink`-ed and re-created via `sync-setup`.

## Common errors and meaning

| Error text | Meaning | Action |
|---|---|---|
| `The connected remote vault no longer exists` | Server-side vault gone | Re-run `sync-list-remote`, pick a live vault, `sync-setup` against it |
| `Failed to authenticate: Vault not found` | Same as above, usually paired | See above |
| `Failed to validate password` | Wrong E2E passphrase or non-TTY invocation | Re-run in a real terminal with the correct password |
| `Sync error: ECONNRESET` | Transient network | Retry; if persistent, check `sync.log` and rotate auth (`ob logout && ob login`) |
