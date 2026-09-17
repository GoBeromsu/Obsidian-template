# Sync Incident Recovery

Contain first, preserve evidence second, restore third, and re-admit continuous sync only after a clean staged run.

## 1. Contain

Stop every headless sync process targeting the affected vault and close the desktop app on replicas.
Do not unlink, reset, or restart while the scope is unknown.

Record:

```bash
ob sync-list-local
ob sync-list-remote
ob sync-status --path "${OBSIDIAN_VAULT_PATH}"
git -C "${OBSIDIAN_VAULT_PATH}" status --short
find "${OBSIDIAN_VAULT_PATH}" -name '*.md' -not -path '*/.git/*' | wc -l
```

Copy the relevant `ob` log and supervisor stderr to a location outside the vault.
Preserve the damaged tree as evidence without making it the rollback source:

```bash
git -C "${OBSIDIAN_VAULT_PATH}" status --short > "${TMPDIR:-/tmp}/ob-sync-incident-status.txt"
git -C "${OBSIDIAN_VAULT_PATH}" diff --binary -- > "${TMPDIR:-/tmp}/ob-sync-incident.patch"
```

## 2. Classify

Distinguish these failure classes before restoring:

| Class | Evidence | Response |
|---|---|---|
| Remote vault missing | `sync-list-remote` lacks the expected vault; stored config reports missing vault. | Preserve local state and create or select a verified remote; never reuse the stale identifier. |
| Wrong local path | `sync-status` path differs by folder or casing. | Unlink only the verified bad path, then pair the exact path in pull-only mode. |
| Concurrent clients | Desktop app and headless daemon touched the same replica vault. | Stop both, restore to a known point, then select one client for that vault. |
| Remote deletion propagated | Git shows broad deletions after a successful pull. | Restore from the named rollback point, verify the remote state, and keep the replica offline until the remote is safe. |
| Authentication or subscription | Error names login, token, password, or subscription. | Stop the crash loop; repair account state through an interactive login, then run one bounded sync. |
| Supervisor/runtime | Native-module, binary path, environment, or restart errors without vault mutations. | Repair the runtime definition, then inspect status before starting sync. |

## 3. Restore

Choose the recovery source explicitly: the primary vault, a named Git rollback point, or a tested external backup.
Do not assume the remote service is authoritative merely because it is remote.

For a Git-backed vault, inspect before restoring:

```bash
git -C "${OBSIDIAN_VAULT_PATH}" tag --list 'safety/ob-sync-*' --sort=-creatordate
git -C "${OBSIDIAN_VAULT_PATH}" diff --stat "<rollback-tag>" --
```

A destructive reset requires explicit approval for the exact vault and target revision.
After restoration, verify file count, representative files, links/assets relevant to the incident, and repository status.

## 4. Re-admit sync safely

1. Confirm the intended remote exists.
2. Keep a valid pairing. Only when classification proved the local pairing stale, unlink that exact pairing and run `sync-setup` in a real TTY.
3. Repair or replace an unsafe remote before reconnecting a restored replica.
4. Set `pull-only` before the first post-recovery sync.
5. Run one sync, inspect the complete diff and logs, and stop on unexplained changes.
6. Promote to bidirectional only after acceptance.
7. Re-enable the daemon only after a second clean one-shot run.

## Evidence receipt

Record:

- Affected machines and vault paths.
- First observed symptom and earliest relevant error.
- Process and client state at containment.
- Rollback source and exact revision or backup timestamp.
- File-count and diff evidence before and after restoration.
- One-shot pull-only and bidirectional verification results.
- Final supervisor state.

Do not record tokens, passphrases, encryption keys, or raw auth files.
