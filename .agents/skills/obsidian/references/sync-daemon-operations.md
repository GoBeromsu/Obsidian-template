# Headless Sync Daemon Operations

Use a process supervisor only after the one-shot pull-only and bidirectional verification gates pass.
The supervisor owns process lifetime; `ob` owns sync configuration.

## Environment

Resolve these values on the replica:

```bash
: "${OBSIDIAN_CLI_PATH:=ob}"
: "${OBSIDIAN_VAULT_PATH:?set vault path}"
: "${OBSIDIAN_SYNC_PROCESS_NAME:=ob-sync}"
: "${PM2_LOG_DIR:=${HOME}/.pm2/logs}"
```

Do not copy an ecosystem file between replicas without re-resolving the vault path and binary path.

## pm2

Create an ecosystem file outside the vault:

```javascript
module.exports = {
  apps: [{
    name: process.env.OBSIDIAN_SYNC_PROCESS_NAME || "ob-sync",
    script: process.env.OBSIDIAN_CLI_PATH || "ob",
    args: ["sync", "--path", process.env.OBSIDIAN_VAULT_PATH, "--continuous"],
    autorestart: true,
    restart_delay: 5000,
    max_restarts: 10,
    kill_timeout: 10000,
    time: true,
    env: {
      OBSIDIAN_VAULT_PATH: process.env.OBSIDIAN_VAULT_PATH,
    },
  }],
};
```

Start once from the reviewed file, save the live definition, and inspect it:

```bash
pm2 start "${HOME}/.config/pm2/ob-sync.config.cjs"
pm2 save
pm2 describe "${OBSIDIAN_SYNC_PROCESS_NAME}"
pm2 logs "${OBSIDIAN_SYNC_PROCESS_NAME}" --lines 100 --nostream
```

After registration, restart by process name rather than by an old ecosystem-file path:

```bash
pm2 restart "${OBSIDIAN_SYNC_PROCESS_NAME}" --update-env
pm2 save
```

`pm2 save` updates the boot-time process dump.
Confirm the boot integration separately with the supervisor’s supported startup command for the operating system.

## Remote inspection

Keep inspection read-only until the failure mechanism is known:

```bash
: "${OBSIDIAN_SYNC_REMOTE_HOST:?set replica host}"
ssh "${OBSIDIAN_SYNC_REMOTE_HOST}" \
  'pm2 describe "$OBSIDIAN_SYNC_PROCESS_NAME"; pm2 logs "$OBSIDIAN_SYNC_PROCESS_NAME" --lines 100 --nostream'
```

Run `ob sync-setup` through an interactive terminal, not as a non-interactive remote command, because encryption setup prompts for a secret.

## Stop and recover

Contain a suspected deletion or crash loop before changing configuration:

```bash
pm2 stop "${OBSIDIAN_SYNC_PROCESS_NAME}"
```

Read the earliest relevant error, verify the local path and remote vault, and follow `sync-recovery.md`.
Do not restart repeatedly: each restart may replay the same destructive or failing state.

## Health evidence

A healthy daemon has:

- Supervisor state is `online` with a low stable restart count.
- A recent successful sync heartbeat is present.
- `ob sync-status` points at the exact intended vault path.
- No concurrent Obsidian desktop process uses the same replica vault.
- Git status and file count remain plausible after a controlled one-shot check.
