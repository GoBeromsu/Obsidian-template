<%*
const match = tp.file.title.match(/(\d{4}-\d{2}-\d{2})/);
// If the title has no date (Untitled-then-rename race), fall back to today.
const today = match ? moment(match[1], 'YYYY-MM-DD') : moment();
const yesterday = today.clone().subtract(1, 'day').format('YYYY-MM-DD');
const tomorrow = today.clone().add(1, 'day').format('YYYY-MM-DD');
const dateStr = today.format('YYYY-MM-DD');
const monday = today.isoWeekday() === 7 ? today.clone().add(1, 'day') : today.clone().startOf('isoWeek');
const weekNote = monday.format('GGGG-WW') + 'W';
-%>
---
aliases: []
created_by: user
authorship: user
tags:
  - plan
type: plan
week: "[[<% weekNote %>]]"
---

[[<% yesterday %> Dashboard|Yesterday's Log (<% yesterday %>)]] | [[<% tomorrow %> Dashboard|Tomorrow's Log (<% tomorrow %>)]]

## Thinking

## Routine

## Overdue
> Incomplete checkboxes from earlier daily notes. Checking them here updates the original daily note.

```dataview
TASK
FROM "10. Time/01 Daily Notes"
WHERE !completed AND file.day < date(today)
SORT file.day DESC
```

## Tasks
> Multi-day, delegated, or deadline work belongs here. Day-to-day checkboxes stay on the daily note; Overdue will surface them.

```base
filters:
  type == "task"
formulas:
  days_left: if(due, (date(due) - today()).days, "")
properties:
  formula.days_left:
    displayName: D-day
  due:
    displayName: Due
  plan:
    displayName: Planned
  done:
    displayName: Done
  project:
    displayName: Project
views:
  - type: table
    name: Today
    filters:
      and:
        - done != true
        - or:
            - and:
                - plan != ""
                - date(plan) <= today()
            - and:
                - due != ""
                - date(due) <= today()
    order:
      - done
      - file.name
      - project
      - due
      - formula.days_left
    sort:
      - property: due
        direction: ASC
      - property: file.name
        direction: ASC
    columnSize:
      file.name: 320
      formula.days_left: 80
  - type: table
    name: Due soon
    filters:
      and:
        - done != true
        - due != ""
    order:
      - done
      - file.name
      - project
      - plan
      - due
      - formula.days_left
    sort:
      - property: due
        direction: ASC
    columnSize:
      file.name: 320
      formula.days_left: 80
  - type: table
    name: Delegation
    filters:
      and:
        - gtd == "delegation"
        - done != true
    order:
      - done
      - file.name
      - project
      - due
    sort:
      - property: due
        direction: ASC
    columnSize:
      file.name: 360
```

## Time Blocks
> In the morning, schedule slots from the Today view (plan). During the day, record what actually happened (track).

## Timeline

```base
filters:
  file.ext == "md"
formulas:
  created_at: 'file.ctime.format("HH:mm")'
  modified_at: 'file.mtime.format("HH:mm")'

properties:
  formula.created_at:
    displayName: "Created"
  formula.modified_at:
    displayName: "Modified"

views:
  - type: table
    name: Created Today
    filters:
      or:
        - date_created == "<% dateStr %>"
        - and:
            - file.ctime >= "<% dateStr %>"
            - file.ctime < "<% tomorrow %>"
    groupBy:
      property: type
      direction: ASC
    order:
      - file.name
      - formula.created_at
      - file.mtime
    sort:
      - property: file.ctime
        direction: ASC
    columnSize:
      file.name: 393

  - type: table
    name: Modified Today
    filters:
      or:
        - date_modified == "<% dateStr %>"
        - and:
            - file.mtime >= "<% dateStr %>"
            - file.mtime < "<% tomorrow %>"
    groupBy:
      property: type
      direction: ASC
    order:
      - file.name
      - file.ctime
      - formula.modified_at
    sort:
      - property: file.mtime
        direction: ASC
```
