# Verified Diagram Catalog

These copy-ready blocks were renderer-tested on Obsidian 1.13.1's bundled Mermaid 11.13.0.
Use the compatibility gate in the parent skill before applying them to another Obsidian baseline.
The examples derive from the linked Threads catalog but use Obsidian-safe fences and an explicit fallback policy.

## Table of Contents

1. [Flowchart](#flowchart)
2. [Class diagram](#class-diagram)
3. [Sequence diagram](#sequence-diagram)
4. [Architecture](#architecture)
5. [User journey](#user-journey)
6. [Pie chart](#pie-chart)
7. [Kanban](#kanban)
8. [Treemap](#treemap)
9. [Mindmap](#mindmap)
10. [Timeline](#timeline)
11. [Sankey diagram](#sankey-diagram)
12. [XY chart](#xy-chart)

## Flowchart

```mermaid
flowchart LR
A[Order received] --> B{Payment successful?}
B -->|Yes| C[Start delivery]
B -->|No| D[Retry payment]
```

## Class diagram

```mermaid
classDiagram
direction LR
class User {
  +String name
  +login()
}
class Order {
  +int amount
  +pay()
}
User "1" --> "*" Order : places
```

## Sequence diagram

```mermaid
sequenceDiagram
User->>Server: Login request
Server->>DB: Find user
DB-->>Server: User record
Server-->>User: Login success
```

## Architecture

```mermaid
architecture-beta
group shop(cloud)[Shop Service]
service web(server)[Web Server] in shop
service api(server)[API Server] in shop
service db(database)[Database] in shop
web:R --> L:api
api:R --> L:db
```

Fallback: use a `flowchart LR` with a subgraph for the service boundary.

## User journey

```mermaid
journey
title Shopping journey
section Join
Sign up: 3: User
Log in: 4: User
section Purchase
Search products: 4: User
Pay: 2: User
```

## Pie chart

```mermaid
pie title Device share
"Mobile" : 60
"Desktop" : 30
"Tablet" : 10
```

## Kanban

```mermaid
kanban
todo[To do]
design[Screen design]
api[API design]
doing[In progress]
login[Login implementation]
done[Done]
release[Create release]
```

Fallback: use headings with task lists when the target bundle lacks `kanban`.

## Treemap

```mermaid
treemap-beta
"Development cost"
  "Frontend": 30
  "Backend": 40
  "Infrastructure": 20
  "Testing": 10
```

Fallback: use `pie` for a single level or `flowchart` for hierarchy.

## Mindmap

```mermaid
mindmap
root((App launch))
  Plan
    User research
    Requirements
  Build
    Frontend
    Backend
  Operate
    Monitoring
```

## Timeline

```mermaid
timeline
title Product development
January : Confirm idea
March : Start development
June : Beta test
July : Release
```

## Sankey diagram

```mermaid
sankey
Visitors,ProductPage,100
ProductPage,Cart,60
ProductPage,Exit,40
Cart,Purchase,30
Cart,Exit,30
```

## XY chart

```mermaid
xychart-beta
title "Monthly signups"
x-axis ["Jan", "Feb", "Mar", "Apr"]
y-axis "Signups" 0 --> 200
bar [80, 120, 150, 180]
line [70, 110, 140, 175]
```
