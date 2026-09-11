<%*
// Parse year from filename (format: YYYY)
const match = tp.file.title.match(/^(\d{4})$/);
// If the title has no year (Untitled-then-rename race), fall back to the current year.
const year = match ? parseInt(match[1]) : moment().year();
const prevYear = year - 1;
const nextYear = year + 1;
const q1 = year + '-Q1';
const q2 = year + '-Q2';
const q3 = year + '-Q3';
const q4 = year + '-Q4';
-%>
---
created_by: user
authorship: user
tags:
  - plan/year
type: plan
---
[[<% prevYear %>|← Previous Year]] | [[<% nextYear %>|Next Year →]]

## Vision

## Goals

## Quarters

- [[<% q1 %>]]
- [[<% q2 %>]]
- [[<% q3 %>]]
- [[<% q4 %>]]

## Review
