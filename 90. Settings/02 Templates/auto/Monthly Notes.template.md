<%*
// Parse year and month from filename (format: YYYY-MM)
const match = tp.file.title.match(/(\d{4})-(\d{2})/);
// If the title has no year-month (Untitled-then-rename race), fall back to the current month.
const year = match ? parseInt(match[1]) : moment().year();
const month = match ? parseInt(match[2]) : moment().month() + 1;

const currentMonth = moment().year(year).month(month - 1);
const prevMonthNote = currentMonth.clone().subtract(1, 'month').format('YYYY-MM');
const nextMonthNote = currentMonth.clone().add(1, 'month').format('YYYY-MM');
const quarterNum = Math.ceil(month / 3);
const quarterNote = year + '-Q' + quarterNum;
-%>
---
year: "[[<% year %>]]"
quarter: "[[<% quarterNote %>]]"
created_by: user
authorship: user
tags:
  - Plan/month
---
[[<% prevMonthNote %>|← Previous Month]] | [[<% nextMonthNote %>|Next Month →]]

## Key Metrics

## Deadline Timeline

<!--
- **[[YYYY-MM-DD]]**
	- event or deadline
-->

### [[<% nextMonthNote %>|Next month's leading deadlines]]

## What You Did

## Weeks in This Month

```base
filters:
  and:
    - file.hasTag("plan/week")
    - 'month.contains("<% tp.file.title %>")'

views:
  - type: table
    name: Weeks in Month
    order:
      - file.name
      - month
```
