# bases

## Overview

Obsidian Bases (1.9+) turn the vault into a queryable dataset.
Every `.base` file is YAML conforming to a fixed schema; embedded bases use a ` ```base ` code block with the same YAML.
Getting `groupBy` and `sort` right is the difference between a base that *lists rows* and a base that *gives the reader a mental model* of the project.

Layout availability is version-gated: `table` and `cards` need 1.9, `list` and `map` need 1.10 (`map` also needs the Maps plugin), and further layouts arrive through community plugins.
Grouping by a single property is a current engine limit, not a 1.10 artifact — it still holds in 1.12.
Verify the constraint against [Views](https://obsidian.md/help/bases/views) rather than assuming a newer release lifted it.

## Vault Access

Use [`cli.md`](cli.md) for all note creation, edit, search, and property mutation inside the vault.
Do not shell out to raw `cat`/`sed` on vault paths.
See [`cli.md`](cli.md) for the command surface and required preconditions (Obsidian must be running).

## When to Use

- Creating or editing a `.base` file under a Bases folder in the vault
- Editing an embedded `` ```base `` block inside a project/MOC/dashboard note
- Optimizing an existing base so the reader can grasp the dataset at a glance — rethink `groupBy` before adding more columns
- Debugging a base that returns 0 rows or the wrong rows — inspect the filter tree, not the view

**NOT for:**
- Dataview / Dataview JS queries (different engine, different syntax)
- Writing Templater JS that *generates* a base string — use the Templater skill and call this skill for the inner YAML

## Core Schema

```yaml
filters:        # global, AND-concat with each view's own filters
formulas:       # named expressions, referenced as formula.<name>
properties:     # per-property config (displayName is the common one)
summaries:      # custom aggregations reusable across views
views:          # list of views; first view is the default
  - type: table | cards | list | map
    name: "..."
    limit: <int>
    filters: { and: [...] | or: [...] | not: [...] | "<expr>" }
    order:       # table column order (also controls what columns render)
      - <property>
    sort:        # multi-key cascade, first key is primary
      - property: <property>
        direction: ASC | DESC
    groupBy:     # single property — one groupBy per view (verified through 1.12)
      property: <property>
      direction: ASC | DESC
    summaries:   # per-column aggregation shown at top of each group / footer
      <property>: Average | Sum | Unique | Filled | Empty | ...
    columnSize:  # table-only, pixel width per column
      <property>: <int>
```

**Property namespaces** — `note.<prop>` (frontmatter, default if no prefix), `file.<field>` (ctime/mtime/name/basename/path/folder/ext/size/tags/links/backlinks), `formula.<name>` (defined in this base).

See `bases-syntax.md` for the full YAML reference and `bases-functions.md` for the complete function catalog.
Don't inline those — they're too long and the model can load them when a specific question needs them.

## The Workflow

1. **State the reader's question.** "Which logs in this project?" / "Which projects are overdue?" / "What did I touch this week?". The question chooses the view type and `groupBy`.
2. **Pick the smallest filter that answers it.** Prefer `file.inFolder("path")` over `file.hasLink(...)` when the corpus is folder-scoped — it's cheaper and less likely to over-match. Use `list(project).contains(link("<name>"))` for notes that reference a project via a frontmatter list property.
3. **Design the lens (`groupBy`).** Group by the property whose distinct values partition the set in a way that matches the reader's mental model. One `groupBy` per view — when you need a second lens, add a second view rather than stacking.
4. **Cascade the `sort`.** First key matches how a human would scan the group (e.g. newest first → `date_created DESC`). Add tiebreakers only when the first key has many ties.
5. **Choose `order`** (columns) to answer the reader's question, not to dump every field. 4–6 columns is the right ballpark.
6. **Verify.** Open the `.base`, confirm the first view renders, each group has members, and sort order looks right. If the view is empty, isolate the filter — comment out the narrowest clause and re-check.

## Designing `groupBy` for a High-Level Overview

The rule of thumb: **`groupBy` is the axis the reader uses to orient themselves before they read any row.**
Pick the property whose values chunk the dataset into ~3–10 visually distinct blocks.

| Reader's question | Good groupBy | Bad groupBy |
|---|---|---|
| "What kinds of notes exist for this project?" | `type` | `file.name` (no grouping signal) |
| "Where am I in the project timeline?" | formula: `date_created.format("YYYY-MM")` | `date_created` (too many groups) |
| "Which projects need attention?" | `status` | `priority` (often missing) |
| "Which area of work?" | formula: `file.folder` or `formula.section` | `tags` (multi-valued, messy) |

When the natural axis isn't a single property, **define a formula** (`formula.month`, `formula.section`, `formula.bucket`) and group by that.
Formulas are first-class properties for grouping and sorting.

Because Obsidian 1.10 supports only one `groupBy` per view, **add a second view** (same filter, different `groupBy`) rather than trying to simulate two-level grouping.

## Common Filter Recipes

```yaml
# Notes inside a project subtree, excluding the project note itself
filters:
  and:
    - file.inFolder("Projects/My Project")
    - file.name != "My Project"

# Notes that mention the project via a frontmatter list OR via [[wikilink]] body
filters:
  or:
    - list(project).contains(link("My Project"))
    - file.hasLink("My Project")

# "Active" projects only
filters:
  and:
    - type == "project"
    - status != "done"
    - status != "stop"

# This week
filters:
  and:
    - file.mtime > now() - "7d"
```

## Embedding a Base in a Note

```markdown
![[Hermes Cron.base]]              <!-- renders the FIRST view in the views list -->
![[Hermes Cron.base#Retired]]      <!-- renders the named view -->
```

The view selector after `#` is the view's `name`, so renaming a view silently breaks every embed that targeted it — grep for the old name when renaming.
When a dashboard note should open on a specific lens, prefer the explicit `#View` selector over reordering `views:`, because reordering changes what every bare `![[...]]` embed renders.

## Reading a Base Without Obsidian

The toolbar covers inspection and extraction: **Search** filters rows by displayed properties, **Results** limits the row count, and **Copy to clipboard** / **Export CSV** move a view into Markdown, a spreadsheet, or another document app.
Reach for CSV export when a base's contents must be verified or diffed outside the app; it is the supported extraction path rather than parsing rendered output.

## Formula Patterns

```yaml
formulas:
  month:     file.ctime.format("YYYY-MM")
  days_left: if(date_finished, (date(date_finished) - today()).days, "")
  section:   if(file.inFolder("Projects"), "Project", "Area")
  updated:   file.mtime.format("YYYY-MM-DD HH:mm")
```

Formulas are always quoted YAML strings.
Reference other formulas as `formula.<name>` — no self-reference, no cycles.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "More columns = more useful base." | Columns past the 6th force horizontal scroll and dilute the reader's attention. Move secondary fields to a second view. |
| "I'll groupBy by tags." | `tags` is a list, so each row can appear in multiple groups and the UI duplicates rows. Group by a single-valued property or a formula. |
| "I'll skip `sort` — Obsidian sorts by default." | Without `sort`, row order is file-system dependent and visually random. Always declare sort when rows mean anything chronological or by-priority. |
| "The view is empty, the data must be wrong." | The filter is wrong 9/10 times. Start by deleting the filter entirely and narrow back down one clause at a time. |
| "I'll use `file.backlinks` because it's expressive." | `file.backlinks` is performance-heavy and is noted as such in the docs; reverse the lookup with `file.links` or `file.hasLink(target)` where possible. |
| "I'll stack two `groupBy`s." | Obsidian groups by one property per view. Duplicate the view with a different `groupBy` instead. |

## Red Flags

- A base with no `sort` block and rows whose order is meant to carry information
- `groupBy` on a list-typed property (tags, aliases, links) — produces duplicate rows
- Identical `filters` block repeated on every view instead of being promoted to the global `filters`
- `order` listing properties that don't exist (silently renders blank columns)
- `file.backlinks` in a filter when `file.links` or `file.hasLink(target)` would work
- Embedded ` ```base ` block with Templater placeholders left unresolved (`undefined` visible in the rendered view)

## Verification

- [ ] Base file parses (Obsidian shows the view, no red error banner)
- [ ] First view renders at least one row for a dataset you know matches
- [ ] `groupBy` produces ≤ ~10 distinct groups for the expected dataset
- [ ] `sort` keys exist as properties / formulas and each has a `direction`
- [ ] `order` only references properties that exist on at least one matched file
- [ ] For multi-view bases, every view that should be scoped has its own `filters`
- [ ] Any `![[Base#View]]` embed names a view that still exists
- [ ] Layouts used are available in the target Obsidian version (`list`/`map` need 1.10+)

## Reference Files

| File | When to read |
|---|---|
| `bases-syntax.md` | Full YAML schema, operators, type system |
| `bases-functions.md` | Every built-in function (file/string/number/date/list/link/object/regex) with signatures |
| `bases-views.md` | View-type-specific options (table/cards/list/map) |
