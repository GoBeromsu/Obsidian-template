<%*
// Parse ISO week-year and week from filename (format: GGGG-WW + W, e.g. 2026-37W).
const match = tp.file.title.match(/(\d{4})-(\d{2})W/);
// If the title has no week (Untitled-then-rename race), fall back to the current ISO week.
const year = match ? parseInt(match[1]) : moment().isoWeekYear();
const week = match ? parseInt(match[2]) : moment().isoWeek();

// ISO week Monday–Sunday, matching the Daily template's GGGG-WW+W id.
const isoMonday = moment().isoWeekYear(year).isoWeek(week).startOf('isoWeek');
const weekStart = isoMonday.clone();
const weekEnd = isoMonday.clone().add(6, 'days');
const monthNote = weekStart.format('YYYY-MM');
const quarterNum = Math.ceil((weekStart.month() + 1) / 3);
const quarterNote = weekStart.format('YYYY') + '-Q' + quarterNum;

const prevWeekNote = isoMonday.clone().subtract(1, 'week').format('GGGG-WW') + 'W';
const nextWeekNote = isoMonday.clone().add(1, 'week').format('GGGG-WW') + 'W';

const weekStartDate = weekStart.format('YYYY-MM-DD');
const weekEndDate = weekEnd.format('YYYY-MM-DD');
-%>
---
created_by: user
authorship: user
tags:
  - plan/week
month: "[[<% monthNote %>]]"
quarter: "[[<% quarterNote %>]]"
roundup: ""
type: plan
---
[[<% prevWeekNote %>|← Previous Week]] | [[<% nextWeekNote %>|Next Week →]]

## Goals

## Review

## Daily Notes

```base
filters:
  and:
    - file.inFolder("10. Time/01 Daily Notes")
    - 'file.basename >= "<% weekStartDate %>"'
    - 'file.basename <= "<% weekEndDate %>"'

views:
  - type: table
    name: Days in Week
    order:
      - file.name
      - file.size
      - file.mtime
    sort:
      - property: file.size
        direction: DESC
```
