# Sample Antigravity Skills

Here are two worked reference examples illustrating the two primary patterns for Antigravity skills.

---

## Pattern A: Instruction-Only Skill

Use this pattern when the workflow consists entirely of reasoning, guidelines, inspection, or coordinating existing built-in tools. No custom python scripts are needed.

### Directory Structure
```text
skills/code-review-guard/
├── SKILL.md
└── references/
    └── security-checklist.md
```

### `SKILL.md`
```markdown
---
name: code-review-guard
description: >-
  Review code diffs and PR branches against architecture and security guidelines.
  Use when the user asks for "code review", "PR 리뷰해줘", "보안 점검", or before merging major changes.
  Do not use for general code generation or bug fixing.
---

# Code Review Guard

Provides a rigorous, step-by-step code review procedure.

## Review Workflow

1. **Inspect Diffs**:
   - Run `git diff main...HEAD` to review all modified lines.
   - Categorize changes into logic, interface, and tests.

2. **Security & Vulnerability Audit**:
   - Check against [Security Checklist](./references/security-checklist.md).
   - Ensure no credentials, hardcoded secrets, or unescaped inputs exist.

3. **Produce Review Report**:
   - Structure feedback as:
     - 🔴 Critical / Blocker
     - 🟡 Suggestions / Improvements
     - 🟢 Praise & Positives
```

---

## Pattern B: Script-Assisted Skill

Use this pattern when the workflow requires querying external APIs, executing complex data transforms, or interacting with binaries that generate large JSON outputs.

### Directory Structure
```text
skills/github-release-helper/
├── SKILL.md
├── scripts/
│   └── release_cli.py
└── references/
    └── release-notes-template.md
```

### `SKILL.md`
```markdown
---
name: github-release-helper
description: >-
  Prepares and drafts GitHub releases with automated changelogs and asset uploads.
  Use when the user asks to "draft release", "create github release", "릴리즈 태그 생성",
  or "changelog 작성".
---

# GitHub Release Helper

Automates gathering closed PRs and drafting GitHub releases.

## Workflow

1. **Collect PRs since last release tag**:
   ```bash
   python3 ./scripts/release_cli.py list-prs --since v1.2.0 --output .release_prs.json
   ```
2. **Draft release notes**:
   - Read `.release_prs.json` using `view_file`.
   - Format entries according to [Release Notes Template](./references/release-notes-template.md).
3. **Publish release**:
   ```bash
   python3 ./scripts/release_cli.py publish --tag v1.3.0 --notes-file release_notes.md
   ```
```
