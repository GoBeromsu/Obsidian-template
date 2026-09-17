# doctor

## Overview

Inspect installed plugin manifests, classify the symptom against a growing `doctor-plugins.yaml` registry, fetch fresh docs when the registry misses, patch via `obsidian-cli`, verify with `obsidian dev:errors`, and record the fix back into the registry so the next run is faster.

## Vault Access

Use [`cli.md`](cli.md) for all note creation, edit, search, and property mutation inside the vault.
Do not shell out to raw `cat`/`sed` on vault paths.
See [`cli.md`](cli.md) for the command surface and required preconditions (Obsidian must be running).

## When to Use

- A Templater template renders a `ReferenceError` or produces a literal `<% ... %>` string instead of evaluated output.
- An Obsidian plugin command fails silently or throws a console error.
- A Base block, dataview query, or plugin-driven script references a plugin API that changed between versions.
- The user wants to verify which plugin version is installed and whether known regressions apply.
- The user asks to "add a plugin to the registry" or "document this plugin's API patterns".

**NOT for:**
- Vault-wide link rot, orphan notes, or frontmatter schema drift — those are not plugin-scoped.
- Core Obsidian bugs unrelated to any plugin.
- Template format problems that have nothing to do with plugin API (e.g., pure Markdown structure issues) — use [`markdown.md`](markdown.md).

## Dependencies

1. [`cli.md`](cli.md) applies and Obsidian must be running (`obsidian status`).
2. `doctor-plugins.yaml` ships with this package as a seed registry — the accumulating store of plugin knowledge. Append to it; never delete or blank it.
3. Plugin manifest path: `${OBSIDIAN_VAULT_PATH}/.obsidian/plugins/{plugin-id}/manifest.json` — readable without Obsidian running.

## Pipeline

Full step-by-step recipes are in [doctor-pipeline.md](doctor-pipeline.md).
Summary:

### Step 1 — Inspect

Identify the plugin involved and its installed version.

```bash
# Read the manifest directly (no obsidian-cli needed)
cat "${OBSIDIAN_VAULT_PATH}/.obsidian/plugins/<plugin-id>/manifest.json"

# Or list all installed plugins
obsidian plugin:list
```

Expected output: `{ "id": "...", "version": "2.19.3", ... }`.
Record `id` and `version`.

**Handoff:** plugin-id + installed version → Step 2.

### Step 2 — Diagnose

Classify the symptom using the error message and plugin version.

```bash
# Pull recent console errors from Obsidian's DevTools bridge
obsidian dev:errors
```

Classification categories:
- **undefined-variable** — `ReferenceError: X is not defined` inside a template expression.
- **api-mismatch** — plugin method signature changed between versions.
- **known-regression** — matches a `known_regressions` entry for that plugin inside `doctor-plugins.yaml`.
- **config-drift** — plugin `data.json` references a path or key that no longer exists.
- **missing-dependency** — plugin requires another plugin that is disabled or absent.

**Handoff:** symptom class + error text → Step 3.

### Step 3 — Consult Registry

Look up the plugin in `doctor-plugins.yaml`.

```bash
# Check registry for the plugin entry
yq '.["<plugin-id>"]' doctor-plugins.yaml

# Check for a known regression matching the installed version
yq '.["<plugin-id>"].known_regressions[] | select(.version == "<version>")' doctor-plugins.yaml
```

If the plugin is **not in the registry**, or the registry entry has no `key_patterns` that cover the symptom:
1. Fetch the plugin docs (via a web fetch, browser, or `defuddle`) using the `docs` URL from the registry (or the repo README if `docs` is null).
2. Extract relevant patterns with Defuddle.
3. Append the learned entry to `doctor-plugins.yaml` (see `## Registry Schema`).

**Handoff:** matching pattern or fetched docs → Step 4.

### Step 4 — Patch

Apply the fix using `obsidian-cli`.
Never hand-edit `.obsidian/plugins/*/data.json` directly.

```bash
# Edit a template note
obsidian note:edit file="<vault-relative-path>"

# Run a Templater template against a test file
obsidian templater:create-from-template template="<template-path>" file="<output-path>"

# Reload the plugin after a config change
obsidian plugin:reload id="<plugin-id>"

# Evaluate a JS snippet inside Obsidian (for runtime mutation)
obsidian eval code="<js-expression>"
```

For `undefined-variable` in a Templater template: rewrite the expression block from `<% bareVar %>` to the `<%* ... %>` entry-block form with `await tp.system.prompt(...)` and `tR +=`.
See `## Worked Example` for the concrete rewrite.

**Handoff:** patched file saved → Step 5.

### Step 5 — Verify

Confirm the fix produces no errors.

```bash
# Check for Obsidian console errors post-patch
obsidian dev:errors

# Run the template end-to-end (answer any prompts)
obsidian templater:create-from-template template="<template-path>" file="_smoketest/plugin-doctor-smoke"

# Capture a screenshot for UI-surfaced fixes
obsidian dev:screenshot
```

Pass criteria: `obsidian dev:errors` returns empty or only pre-existing unrelated errors.
The rendered note contains no literal `<% ... %>` strings.

Cleanup after smoke test:

```bash
obsidian note:delete file="_smoketest/plugin-doctor-smoke"
```

**Handoff:** clean error log + rendered note evidence → Step 6.

### Step 6 — Learn

Append the regression or fix recipe to the registry so the next run is faster.

```bash
# Append a new antipattern entry (yq in-place edit)
yq -i '.["<plugin-id>"].antipatterns += ["<description of the broken pattern>"]' doctor-plugins.yaml

# Append a known regression
yq -i '.["<plugin-id>"].known_regressions += [{"version": "<ver>", "id": "<id>", "note": "<desc>", "fix": "<workaround>"}]' doctor-plugins.yaml

# Update version_seen if the installed version is newer than recorded
yq -i '.["<plugin-id>"].version_seen = "<installed-version>"' doctor-plugins.yaml
```

The registry update is the durable record of the fix — no separate vault log is required.

## Registry Schema

The registry lives at [doctor-plugins.yaml](doctor-plugins.yaml).
It is keyed by `plugin-id` (the string in `manifest.json`).

```yaml
<plugin-id>:
  repo: <GitHub URL>
  docs: <docs URL or null>
  version_seen: <semver string or null>
  key_patterns:
    <pattern-name>: "<pattern string>"
  antipatterns:
    - "<description>  # reason → consequence"
  known_regressions:
    - version: "<semver>"
      id: "<short-id>"
      note: "<description>"
      fix: "<workaround>"
```

Rules:
- `version_seen` is updated on every run where the installed version is newer than recorded.
- `key_patterns` grows; entries are never removed unless the API is gone.
- `antipatterns` and `known_regressions` are append-only — never blank the list.
- New plugins are appended as new top-level keys; existing keys are never replaced wholesale.
- Keep host- or vault-specific note/template paths out of the registry — cite the plugin behavior, not a private file.

## Worked Example — undefined variable in a Templater template

The concrete form of the pipeline against a Templater template whose heading renders as the literal string `# <% newName %>` and whose Base block references `<% newName %>` unresolved.
Obsidian's console shows `ReferenceError: newName is not defined`.

**Step 1 — Inspect:** Plugin is `templater-obsidian`, manifest version `2.19.3`.

**Step 2 — Diagnose:** Class = `undefined-variable`.
Templater evaluates `<% expr %>` as a bare JS expression in its scope.
`newName` has no binding in that scope — it is not a Templater system variable.
Result: `ReferenceError`, template aborts.

**Step 3 — Consult Registry:** the `doctor-plugins.yaml` entry for `templater-obsidian` confirms:
- `antipatterns` includes `"<% bareVar %> # undefined in Templater's JS scope → ReferenceError"`.
- `key_patterns.entry_block` = `"<%* ... %>"` — the correct form for imperative logic.
- `key_patterns.prompt` = `"await tp.system.prompt('label', 'default')"` — to capture user input.

**Step 4 — Patch:** Rewrite the template.
Replace every `<% newName %>` occurrence with a `<%* ... %>` entry block that:
1. Prompts the user for the value.
2. Sanitizes input.
3. Renames the file.
4. Appends the rendered body (with `${newName}` interpolation inside `tR +=`) so the Base block filters use the resolved string.

Correct entry block pattern:

```
<%*
const rawInput = await tp.system.prompt("Project name");
if (!rawInput) return;
const newName = rawInput.replace(/[\\/:*?"<>|]/g, "").trim();
await tp.file.rename(newName);
tR += `# ${newName}

## Thinking

## Reflections

## Details

...Base block with ${newName} substituted...
`;
%>
```

**Step 5 — Verify:** Run the template against `_smoketest/plugin-doctor-smoke`, enter a test value at the prompt.
Confirm: file renamed to the value, heading resolved, Base block filters contain the resolved string, `obsidian dev:errors` clean.

**Step 6 — Learn:** Append the antipattern entry to the registry under `templater-obsidian`.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can skip registry lookup — I know what the fix is." | Registry lookup takes one `yq` call. Skipping it means the fix is never recorded and the next occurrence requires full re-diagnosis. |
| "I'll edit `data.json` directly — it's faster than obsidian-cli." | Direct edits to `.obsidian/plugins/*/data.json` bypass Obsidian's in-memory state and can corrupt plugin config on next load. Always use `obsidian eval` or `obsidian plugin:reload`. |
| "The template error is obvious — no need to run `dev:errors`." | `dev:errors` may surface a second unrelated error in the same plugin that is masked by the first. Always run it before declaring done. |
| "I'll update the registry later." | Later never comes. The learn step is part of the pipeline; committing without it means the registry drifts from reality. |
| "I can guess the docs URL without fetching it." | The registry stores the fetched URL. A wrong URL causes the next fetch to fail silently. Always verify before writing. |

## Red Flags

- Running the patch step before reading `obsidian dev:errors` output.
- Writing to `doctor-plugins.yaml` by overwriting the whole file (blanks all prior knowledge).
- Using `<% expr %>` syntax in any new Templater template block (always use `<%* ... %>` for imperative logic).
- Skipping the smoke test after a template patch.
- Reporting completion before `obsidian dev:errors` returns clean.
- Creating a new plugin entry in the registry without a `repo` URL.

## Verification

- [ ] `obsidian plugin:list` or manifest read returned the plugin-id and version before any edit.
- [ ] `obsidian dev:errors` ran before the patch and its output was inspected.
- [ ] Symptom classified into one of the five categories (undefined-variable, api-mismatch, known-regression, config-drift, missing-dependency).
- [ ] Registry consulted via `yq` before patching; if plugin absent, docs fetched and entry appended.
- [ ] Patch applied via `obsidian-cli` commands only — no raw file edits inside `.obsidian/plugins/`.
- [ ] Smoke test ran (`obsidian templater:create-from-template` or equivalent) and produced the expected note.
- [ ] `obsidian dev:errors` ran after the patch and returned clean (or only pre-existing unrelated errors).
- [ ] Smoke test note deleted after verification.
- [ ] `doctor-plugins.yaml` updated with `version_seen`, any new antipattern, and any new regression.
