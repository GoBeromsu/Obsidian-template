# Skill Description Optimization Guide

In Antigravity, the `description` in the YAML frontmatter of `SKILL.md` is the **single most critical factor** determining whether an agent loads your skill at the right time.

Because Antigravity relies on **Progressive Disclosure**, the body of `SKILL.md` is invisible to the agent during discovery. Only `name` and `description` are placed in the agent's prompt during tool/skill routing.

---

## 1. Structure of a High-Quality Description

A well-crafted description consists of three key components:

1. **Role & Capability**: What the skill does (action-oriented).
2. **Positive Triggers (When to Use)**: Keywords, user phrasing, and scenarios that should activate the skill.
3. **Negative Boundaries (When NOT to Use)**: Guardrails to prevent hijacking tasks meant for other skills, general reasoning, or built-in tools.

### Example Template
```yaml
description: >-
  [Brief action summary of what the skill accomplishes].
  Use when the user asks to [action 1], [action 2], [specific keywords in Korean/English],
  or mentions "[keyword A]", "[keyword B]".
  Do not use for [unrelated task A] (use [other-skill] instead) or [unrelated task B].
```

---

## 2. Common Anti-Patterns & How to Fix Them

### Anti-Pattern 1: Too Vague (Under-Triggering)
- ❌ `description: A skill for handling GitHub repositories.`
- **Problem**: The agent will rarely trigger this because the intent is too abstract.
- ✅ **Fixed**:
  ```yaml
  description: >-
    Automate GitHub repository management including issue triage, branch protection rules,
    and PR automation via gh CLI. Use when the user asks to "manage repo", "GitHub PR",
    "이슈 정리", "PR 올려줘", or wants to configure repository settings.
  ```

### Anti-Pattern 2: Overly Broad (Over-Triggering / Hijacking)
- ❌ `description: Helps with writing code, documentation, and answering technical questions.`
- **Problem**: This triggers on virtually every prompt, polluting context and wasting tokens.
- ✅ **Fixed**: Scope down to the specific domain or framework.

### Anti-Pattern 3: Missing Negative Boundaries
- If you have two related skills (e.g., `youtube-upload` and `youtube-channel-ops`):
  - In `youtube-channel-ops`:
    ```yaml
    description: >-
      Analyze and operate YouTube channel performance and metadata.
      Use when the user asks about channel metrics, 조회수 추이, 검색 유입, or retention.
      Do not use for uploading videos or generating subtitles (use youtube-upload instead).
    ```

---

## 3. Bilingual Trigger Support

If the user interacts in multiple languages (e.g., Korean and English), include key trigger phrases in both languages:

```yaml
description: >-
  Create and manage book notes in the vault with structured frontmatter and ToC.
  Use when the user provides a book URL (yes24, aladin), says "책 노트", "book note",
  "이 책 정리해줘", or requests reading list processing.
```

---

## 4. Length Constraints

- Keep the description under **1024 characters**.
- Avoid multi-paragraph narratives; use concise, dense phrasing.
- Avoid markdown formatting inside the YAML scalar (keep it plain text with `>-`).
