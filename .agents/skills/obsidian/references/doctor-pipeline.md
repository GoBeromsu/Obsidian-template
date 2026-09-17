# doctor — Pipeline Reference

Detailed recipes for each of the six pipeline steps.
The SKILL.md body carries summaries; this file carries the full command forms, decision trees, and expected output shapes.

Vault root assumed: `${OBSIDIAN_VAULT_PATH}` Registry path: `references/doctor-plugins.yaml` (ships with this skill package)

---

## Step 1 — Inspect

**Trigger question:** Which plugin is involved, and what version is installed?

### Commands

```bash
# Option A: read manifest directly (Obsidian need not be running)
cat "${OBSIDIAN_VAULT_PATH}/.obsidian/plugins/<plugin-id>/manifest.json"

# Option B: list all installed plugins via obsidian-cli (Obsidian must be running)
obsidian plugin:list

# List all plugin directories to discover available plugin-ids
ls "${OBSIDIAN_VAULT_PATH}/.obsidian/plugins/"
```

### Expected output shape

```json
{
  "id": "templater-obsidian",
  "name": "Templater",
  "version": "2.19.3",
  "minAppVersion": "1.5.0",
  "author": "SilentVoid"
}
```

Record: `plugin-id` (the `id` field) and `version`.

### Handoff to Step 2

Plugin-id string + installed version string.

---

## Step 2 — Diagnose

**Trigger question:** What class of failure is this?

### Commands

```bash
# Pull Obsidian DevTools console errors
obsidian dev:errors

# If the symptom is a broken template, render it to see the error live
obsidian templater:create-from-template \
  template="<vault-relative-template-path>" \
  file="_smoketest/diag-probe"

# Clean up probe note regardless of outcome
obsidian note:delete file="_smoketest/diag-probe"
```

### Classification decision tree

```
Is there a ReferenceError for a variable name?
  YES → undefined-variable
  NO  → Does the error mention a method or property that no longer exists?
    YES → api-mismatch
    NO  → Does the version_seen in the registry have a known_regressions entry matching installed version?
      YES → known-regression
      NO  → Does the plugin fail to find a configured path or key?
        YES → config-drift
        NO  → Does the plugin require another plugin that is disabled?
          YES → missing-dependency
          NO  → unknown (fetch docs in Step 3 and classify after reading)
```

### Expected evidence

- `dev:errors` output (may be empty — that is also evidence).
- Error class label from the decision tree.
- Exact error string for registry recording.

### Handoff to Step 3

Symptom class + raw error text.

---

## Step 3 — Consult Registry

**Trigger question:** Does the registry have a pattern or known regression that explains this symptom?

### Commands

```bash
REGISTRY="references/doctor-plugins.yaml"  # ships with this skill package

# Check whether the plugin has an entry
yq '.["<plugin-id>"] | has("repo")' "$REGISTRY"

# Read all key_patterns for the plugin
yq '.["<plugin-id>"].key_patterns' "$REGISTRY"

# Check antipatterns list
yq '.["<plugin-id>"].antipatterns[]' "$REGISTRY"

# Look for a known regression at the installed version
yq '.["<plugin-id>"].known_regressions[] | select(.version == "<installed-version>")' "$REGISTRY"
```

### Registry miss — fetch docs

If the plugin entry is absent, or `key_patterns` is empty (`{}`), or no antipattern matches:

1. Read `docs` URL from the registry entry (or use `repo` README URL if `docs` is null).
2. Fetch the docs page with a web fetch (browser or `defuddle`).
3. Extract relevant API patterns with Defuddle.
4. Append the new entry or update the existing entry in the registry (see `## Registry Append Protocol`).

### Expected evidence

- `yq` output showing the matching pattern or regression entry.
- If registry miss: fetched docs content and the new registry entry written.

### Handoff to Step 4

Matching pattern string or fetched fix recipe.

---

## Step 4 — Patch

**Trigger question:** How is the fix applied without corrupting plugin state?

### Commands

```bash
# Edit a vault note (template, script, config note) via obsidian-cli
obsidian note:edit file="<vault-relative-path>"

# Run a Templater template to test a patch interactively
obsidian templater:create-from-template \
  template="<vault-relative-template-path>" \
  file="<vault-relative-output-path>"

# Reload the plugin after a data.json change (use eval to mutate config in-memory first)
obsidian plugin:reload id="<plugin-id>"

# Runtime JS evaluation (for in-memory config mutation — avoid if note:edit suffices)
obsidian eval code="app.plugins.plugins['<plugin-id>'].settings.<key> = <value>; await app.plugins.plugins['<plugin-id>'].saveSettings();"
```

### Patch patterns by symptom class

**undefined-variable (Templater):** Replace `<% bareVar %>` with an `<%* ... %>` entry block:

```
# Before (broken)
<% newName %>

# After (correct)
<%*
const rawInput = await tp.system.prompt("Label for prompt");
if (!rawInput) return;
const newName = rawInput.replace(/[\\/:*?"<>|]/g, "").trim();
await tp.file.rename(newName);
tR += `# ${newName}
... rest of body with ${newName} interpolated via template literal ...
`;
%>
```

**api-mismatch:** Update the call site in the template or script to match the current API signature found in the registry `key_patterns`.

**known-regression:** Apply the `fix` recipe from the `known_regressions` entry verbatim.

**config-drift:** Use `obsidian eval` to update the in-memory setting and `saveSettings()`, then `obsidian plugin:reload`.

**missing-dependency:** Enable the required plugin via `obsidian plugin:enable id="<dep-plugin-id>"`.

### Never do

- Do not edit `.obsidian/plugins/*/data.json` directly with a shell editor. Always go through `obsidian eval` + `saveSettings()` or the plugin's own settings UI.
- Do not edit `.obsidian/plugins/*/main.js` — that is patching the plugin binary, not the user config.

### Expected evidence

- The edited file path and a brief description of the change.
- `obsidian plugin:reload` exit code 0.

### Handoff to Step 5

Patched file path(s) and reload confirmation.

---

## Step 5 — Verify

**Trigger question:** Does the fix produce clean output with no console errors?

### Commands

```bash
# Check Obsidian console errors after the patch
obsidian dev:errors

# Run a smoke test (for template patches)
obsidian templater:create-from-template \
  template="<vault-relative-template-path>" \
  file="_smoketest/plugin-doctor-smoke"

# Capture a screenshot for UI-surfaced verifications
obsidian dev:screenshot

# Delete the smoke test note after verification
obsidian note:delete file="_smoketest/plugin-doctor-smoke"
```

### Pass criteria

- `obsidian dev:errors` output contains no new error lines compared to the pre-patch baseline.
- The smoke-test note:
  - Contains no literal `<% ... %>` strings.
  - Has the correct title (the value entered at the prompt).
  - Has the correct property values if frontmatter was generated.
- `dev:screenshot` (if taken) shows the rendered note without error banners.

### Fail criteria — escalate

If the smoke test still fails after one patch attempt, return to Step 2 with the new error text.
If the same symptom class recurs after three attempts, record an `unresolved` entry in `known_regressions` and escalate to the user with full evidence.

### Handoff to Step 6

Clean `dev:errors` output + smoke-test note path (before deletion) + screenshot path if taken.

---

## Step 6 — Learn

**Trigger question:** Is the fix recorded so the next occurrence is faster?

### Commands

```bash
REGISTRY="references/doctor-plugins.yaml"  # ships with this skill package

# Append a new antipattern entry
yq -i '.["<plugin-id>"].antipatterns += ["<description of broken pattern>  # reason → consequence"]' "$REGISTRY"

# Append a known regression
yq -i '.["<plugin-id>"].known_regressions += [{"version": "<ver>", "id": "<short-id>", "note": "<description>", "fix": "<workaround>"}]' "$REGISTRY"

# Update version_seen if the installed version is newer than recorded
yq -i '.["<plugin-id>"].version_seen = "<installed-version>"' "$REGISTRY"

# Add a new key_pattern
yq -i '.["<plugin-id>"].key_patterns.<pattern-name> = "<pattern string>"' "$REGISTRY"
```

### Durable record

The registry update above is the durable record of the fix.
Do not write a separate host- or vault-specific change log.

### Expected evidence

- `yq` exit code 0 for each registry mutation.
- Registry diff showing the new/updated entry.

### Handoff

Done.
Return the patched file path and registry diff to the user as the completion report.

---

## Registry Append Protocol

This section governs how `references/doctor-plugins.yaml` is updated.
The registry is NEVER blanked.
New entries are always appended; existing entries are updated field-by-field.

### Adding a new plugin entry

```bash
REGISTRY="references/doctor-plugins.yaml"  # ships with this skill package

yq -i '.["<new-plugin-id>"] = {
  "repo": "<GitHub URL>",
  "docs": "<docs URL or null>",
  "version_seen": "<semver or null>",
  "key_patterns": {},
  "antipatterns": [],
  "known_regressions": []
}' "$REGISTRY"
```

### Updating an existing entry

Always use field-level mutations, never overwrite the top-level key:

```bash
# Add a key_pattern
yq -i '.["<plugin-id>"].key_patterns.<name> = "<value>"' "$REGISTRY"

# Append antipattern
yq -i '.["<plugin-id>"].antipatterns += ["<entry>"]' "$REGISTRY"

# Append known regression
yq -i '.["<plugin-id>"].known_regressions += [{"version":"<v>","id":"<id>","note":"<n>","fix":"<f>"}]' "$REGISTRY"

# Update version_seen
yq -i '.["<plugin-id>"].version_seen = "<ver>"' "$REGISTRY"
```

### Manual edit fallback

If `yq` is unavailable, open the YAML file directly, locate the plugin-id key, and append to the appropriate list.
Preserve indentation (2-space).
Never delete existing entries.
Quote strings containing `<`, `>`, or `%` characters.

### Invariants

- The registry file is never truncated or replaced wholesale.
- Every new plugin entry must include at minimum `repo` and `docs` (null is allowed for `docs`).
- `key_patterns`, `antipatterns`, and `known_regressions` must always be present as keys, even if empty (`{}` or `[]`).
- After any `yq -i` mutation, verify with `yq '.' "$REGISTRY"` to confirm the YAML parses cleanly.
