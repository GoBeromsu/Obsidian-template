<%*
// Parse year and quarter from filename (format: YYYY-QN)
const match = tp.file.title.match(/(\d{4})-Q(\d)/);
// If the title has no year-quarter (Untitled-then-rename race), fall back to the current quarter.
const year = match ? parseInt(match[1]) : moment().year();
const quarter = match ? parseInt(match[2]) : moment().quarter();

const prevQ = quarter === 1 ? { year: year - 1, q: 4 } : { year, q: quarter - 1 };
const nextQ = quarter === 4 ? { year: year + 1, q: 1 } : { year, q: quarter + 1 };
const prevQuarterNote = `${prevQ.year}-Q${prevQ.q}`;
const nextQuarterNote = `${nextQ.year}-Q${nextQ.q}`;

const firstMonth = (quarter - 1) * 3 + 1;

const month1 = moment().year(year).month(firstMonth - 1).format('YYYY-MM');
const month2 = moment().year(year).month(firstMonth).format('YYYY-MM');
const month3 = moment().year(year).month(firstMonth + 1).format('YYYY-MM');
-%>
---
year: "[[<% year %>]]"
quarter: Q<% quarter %>
created_by: user
authorship: user
tags:
  - Plan/quarter
type: plan
---
[[<% prevQuarterNote %>|← Previous Quarter]] | [[<% nextQuarterNote %>|Next Quarter →]]

## Quarter Overview

### Core Focus Areas
- <% tp.file.cursor(0) %>

### Key Objectives
1.
2.
3.

## Monthly Breakdown

- [[<% month1 %>]]
- [[<% month2 %>]]
- [[<% month3 %>]]

```base
filters:
  and:
    - file.hasTag("Plan/month")
    - file.inFolder("10. Time/03 Monthly Notes")
    - or:
        - 'file.basename == "<% month1 %>"'
        - 'file.basename == "<% month2 %>"'
        - 'file.basename == "<% month3 %>"'

views:
  - type: table
    name: Months in Quarter
    order:
      - file.name
      - date_created
```
