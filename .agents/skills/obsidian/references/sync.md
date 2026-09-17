# Obsidian Sync

Operate `obsidian-headless` (`ob`) under one rule: every sync change is staged, evidenced, and reversible.
A first sync or repaired config starts in `pull-only`, runs once, and earns promotion to bidirectional continuous mode only after the local diff is plausible.

## Requirements

- `ob` from the `obsidian-headless` package
- `${OBSIDIAN_VAULT_PATH}` set independently on every machine
- Git or another tested point-in-time backup for each live vault
- A process supervisor such as pm2, systemd, or launchd for continuous replicas
- Optional `${OBSIDIAN_SYNC_REMOTE_HOST}` and `${OBSIDIAN_SYNC_PROCESS_NAME}` for remote daemon operations

## Boundaries

Use this skill for the headless `ob` client, its local/remote vault pairing, sync modes, and daemon lifecycle.
Use `obsidian-cli` for note reads and writes, [`doctor.md`](doctor.md) for plugins and templates, and the desktop app for GUI Sync settings.
Do not use `mirror-remote` as a shortcut for conflict resolution.

## Topology

Assign roles before running a command:

- **Primary**: the machine whose vault state is authoritative for the operation. It may run the Obsidian desktop app.
- **Replica**: a machine running `ob`; a continuous replica must not run the desktop app against the same vault concurrently.
- **Remote service**: the Obsidian Sync vault. Confirm it still exists before changing a local pairing.

Resolve `${OBSIDIAN_VAULT_PATH}` separately on each machine.
Never copy an absolute path from one host to another; `ob` keys local configuration by the literal path, including its casing.

## Workflow

### Incident branch

If the signal is a large or unexplained deletion set, stop every Sync client and load [`sync-recovery.md`](sync-recovery.md) before running normal Preflight.
Do not create a normal pre-sync tag and treat the already-damaged tree as a restore point.
Preserve forensic evidence outside the vault, identify a known-good recovery source, and return to the staged workflow only after restoration.

### 1. Preflight

1. Identify the primary, replica, target remote vault, and expected direction of change.
2. Stop `ob sync --continuous` and close the Obsidian desktop app on the replica.
3. Create a rollback point on every affected vault. For a Git-backed vault:

   ```bash
   git -C "${OBSIDIAN_VAULT_PATH}" status --short
   git -C "${OBSIDIAN_VAULT_PATH}" tag "safety/ob-sync-$(date -u +%Y%m%d-%H%M%S)"
   ```

Do not stage or commit unrelated changes merely to make the snapshot look clean.
4. Record baseline evidence:

   ```bash
   find "${OBSIDIAN_VAULT_PATH}" -name '*.md' -not -path '*/.git/*' | wc -l
   git -C "${OBSIDIAN_VAULT_PATH}" status --short
   ob sync-list-remote
   ob sync-list-local
   ```

5. Confirm the intended remote vault exists. Stop when the target is absent or ambiguous.
6. Verify the exact local path and casing with `ob sync-status --path "${OBSIDIAN_VAULT_PATH}"`.

### 2. Stage in pull-only mode

Run setup in a real TTY because the end-to-end encryption password prompt is interactive:

```bash
ob sync-setup \
  --vault "<vault-id-or-name>" \
  --path "${OBSIDIAN_VAULT_PATH}" \
  --device-name "<replica-name>"
ob sync-config --path "${OBSIDIAN_VAULT_PATH}" --mode pull-only
```

If a stale config points to the wrong path, inspect it first, then unlink only that exact path:

```bash
ob sync-list-local
ob sync-unlink --path "<verified-stale-path>"
```

Never pipe credentials, place them in arguments, or run setup through a non-interactive SSH command.

### 3. Run once and verify

Run one bounded sync, preserving the command status while recording output:

```bash
set -o pipefail
ob sync --path "${OBSIDIAN_VAULT_PATH}" | tee "${TMPDIR:-/tmp}/ob-sync-first-run.log"
```

Verify all of the following before promotion:

- The Markdown file-count delta is explained by known drift.
- `git status --short` shows a plausible set of changes rather than a broad wipe.
- The log has no authentication, missing-vault, or repeated transport errors.
- `ob sync-status --path "${OBSIDIAN_VAULT_PATH}"` reports the intended device and `pull-only` mode.
- A representative sample of changed files opens and contains expected content.

Stop the workflow when any check is unexplained.
Follow [sync-recovery.md](sync-recovery.md); do not “try bidirectional” to see whether it heals itself.

### 4. Promote deliberately

After the one-shot result is accepted:

```bash
ob sync-config --path "${OBSIDIAN_VAULT_PATH}" --mode bidirectional
ob sync --path "${OBSIDIAN_VAULT_PATH}"
```

Verify the second one-shot run, then start continuous mode under the selected supervisor:

```bash
ob sync --path "${OBSIDIAN_VAULT_PATH}" --continuous
```

Use [daemon-operations.md](sync-daemon-operations.md) for supervisor configuration and remote inspection.

## Daily operations

Prefer read-only inspection before restart or reconfiguration:

```bash
ob sync-status --path "${OBSIDIAN_VAULT_PATH}"
ob sync-list-local
```

For a remote replica, resolve the host and process explicitly:

```bash
: "${OBSIDIAN_SYNC_REMOTE_HOST:?set replica host}"
: "${OBSIDIAN_SYNC_PROCESS_NAME:?set supervisor process name}"
ssh "${OBSIDIAN_SYNC_REMOTE_HOST}" \
  'ob sync-status --path "$OBSIDIAN_VAULT_PATH" && pm2 describe "$OBSIDIAN_SYNC_PROCESS_NAME"'
```

A mode change, unlink, setup, or daemon-definition change repeats Preflight and the one-shot Verify gate.
A restart alone does not justify changing configuration.

## Mode selection

| Mode | Behavior | Admission |
|---|---|---|
| `pull-only` | Downloads remote changes; remote deletions still apply locally. | Required for first sync and repaired pairings. |
| `bidirectional` | Uploads local changes and downloads remote changes. | Only after a clean one-shot pull and reviewed diff. |
| `mirror-remote` | Reverts local-only state to match the remote. | Explicit destructive intent plus a tested rollback point. |

## Failure triage

| Signal | Interpretation | Action |
|---|---|---|
| `The connected remote vault no longer exists` or `Vault not found` | The stored remote identifier is stale or deleted. | Re-run `sync-list-remote`; do not reuse the stale pairing. |
| `Failed to validate password` | Wrong passphrase or no interactive TTY. | Re-run setup in a real terminal; do not pass the secret on the command line. |
| Restart count rises continuously | Authentication, binary, native-module, path, or supervisor failure. | Stop the process and inspect stderr before restarting again. |
| Files appear absent only over SSH on macOS | The shell may lack Full Disk Access. | Verify locally on the replica or through an authorized process before diagnosing data loss. |
| Large unexplained deletion set | Remote deletion, wrong path, race, or corrupt state. | Stop all sync clients and execute the recovery procedure. |

## Anti-patterns

- Treating `pull-only` as deletion-proof → remote deletions still propagate; keep a rollback point and inspect the diff.
- Running the desktop app and `ob --continuous` on the same replica vault → choose one sync client per vault at a time.
- Restarting a supervisor from a stale ecosystem file → inspect the live process definition and restart by the registered process name.
- Guessing that a remote vault still exists → `ob sync-list-remote` is a mandatory preflight check.
- Copying one host’s vault path into another host’s config → resolve and verify the exact path independently.
- Repeatedly restarting a crash loop → stop it, read the first error, fix the cause, then perform one controlled restart.

## Verification

- [ ] Every affected vault has a named rollback point created before mutation.
- [ ] The target remote vault exists and the exact local path is verified.
- [ ] A one-shot `pull-only` run completed before bidirectional or continuous mode.
- [ ] File-count, Git diff, logs, and representative files agree with the expected change.
- [ ] The desktop app is not racing the headless client on the replica.
- [ ] Supervisor status and recent logs show a stable heartbeat with a low restart count.

See [cli-commands.md](sync-cli-commands.md) for the command surface and [recovery.md](sync-recovery.md) for incident containment and restoration.
