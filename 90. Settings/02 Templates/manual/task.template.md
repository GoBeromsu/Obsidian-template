<%*
const today = tp.date.now("YYYY-MM-DD");
-%>
---
aliases: []
type: task
done: false
gtd: inbox
project: []
plan: null
due: null
date_created: <% today %>
date_modified: <% today %>
date_finished: null
created_by: user
authorship: user
tags:
  - task
---
<!--
Dashboard Tasks (`auto/Dashboard.template.md`) match `type: task` and these fields:
- Today: `done != true` and (`plan` or `due` is an ISO date on or before today)
- Due soon: `done != true` and `due` is set
- Delegation: `gtd == "delegation"` and `done != true`
Fill `plan` / `due` as `YYYY-MM-DD`. Place the note anywhere Bases can index it
(for example `15. Work/04 Tasks`). Day-to-day checkboxes stay on the daily note.
-->

## Why
> Why this work exists. If it has a due date, why that date.

## What
> Concrete steps that finish inside the due date.

Add actionable steps here; `done` in frontmatter controls the Dashboard's task status.

## References

Link the source material or owning project here.
