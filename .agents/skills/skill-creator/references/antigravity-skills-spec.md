# Antigravity Agent Skills Specification

Based on official Google Antigravity documentation ([antigravity.google/docs/skills](https://antigravity.google/docs/skills/)).

## 1. What are Agent Skills?

Agent Skills are modular, reusable packages of procedural knowledge, runbooks, and optional helper tools designed to extend the capabilities of AI agents in Google Antigravity.

### The Problem: Tool & Context Bloat
In complex software and engineering workflows, equipping an LLM agent with every possible tool, system prompt rule, and documentation snippet at startup leads to:
- Context window exhaustion
- High latency and excessive token costs
- Hallucination and tool misdirection (confusion between overlapping tools)

### The Solution: Progressive Disclosure
Skills solve this by decoupling **discovery** from **execution**:
1. **Discovery (Low Context Cost)**: At session initialization, only the skill's metadata (`name` and `description` from YAML frontmatter) is loaded into the agent's context.
2. **Activation (On-Demand)**: When the agent or user identifies that a task requires the skill, the agent reads `SKILL.md` and loads the full instructions into memory.
3. **Execution (Deep Dive)**: Bulky reference manuals or helper scripts in subdirectories (`references/`, `scripts/`) are only accessed if the active skill explicitly needs them.

---

## 2. Directory Structure

A compliant Antigravity skill is a directory bundle formatted as follows:

```text
skills/<skill_name>/
├── SKILL.md          # Mandatory: Main instruction file with YAML frontmatter
├── scripts/          # Optional: Executable helper scripts (CLI tools, automation)
├── references/       # Optional: In-depth documentation, manuals, API schemas
├── examples/         # Optional: Worked examples, sample inputs and outputs
└── resources/        # Optional: Templates, static assets, configuration files
```

### Folder Roles
- **`SKILL.md`**: The entry point. Must be concise (ideally under 500 lines) and focus on workflow logic. It links to files in `references/` or `scripts/` using relative markdown links (e.g., `[API Manual](./references/api-docs.md)`).
- **`scripts/`**: Executable code (`.py`, `.sh`, `.js`). Used when programmatic work (API calls, data processing, formatting) is needed. Python scripts should follow the `uv run` convention and standard library preferences.
- **`references/`**: Bulky domain knowledge that the agent doesn't need on every invocation (e.g., full API schemas, error code tables, lengthy protocols).
- **`examples/`**: Concrete demonstrations showing how the skill should be performed, providing few-shot guidance.

---

## 3. Frontmatter Specification

Every `SKILL.md` must start with YAML frontmatter containing `name` and `description`:

```yaml
---
name: my-skill-name
description: >-
  Concise summary in third person describing what the skill does and when the agent should use it.
  Include positive trigger phrases and negative boundaries.
---
```

### Constraints:
- **`name`**:
  - Lowercase alphanumeric characters and hyphens (`[a-z0-9-]+`)
  - Maximum 64 characters
  - Must match the directory name (convention)
- **`description`**:
  - Plain string (YAML `>-` folded scalar recommended)
  - Maximum 1024 characters
  - Must specify **what** the skill accomplishes and **exact trigger criteria** ("Use when...", "Trigger on...").
  - Should include negative boundaries ("Do not use for...") if similar skills exist.

---

## 4. Discovery Locations & Loading Priority

Antigravity traverses specific directories to discover and load skills. The loading precedence (from highest to lowest) is:

1. **Workspace Project Root**:
   - Path: `.agents/skills/<skill-name>/` (also recognizes `.claude/skills/` via symlinks or compatibility)
   - Scope: Shared with team members via version control (Git).
2. **Explicit Workspace Manifest**:
   - Customizations declared in `skills.json` or `plugins.json` in the workspace.
3. **Global User Configuration**:
   - Path: `~/.gemini/antigravity/skills/<skill-name>/` (or `~/.gemini/config/skills/<skill-name>/`)
   - Scope: Available across all projects and conversations on the local machine.
4. **Built-in / Bundled Skills**:
   - Shipped with the Antigravity application or installed plugins.

---

## 5. Skills vs. Rules vs. Plugins vs. MCP

| Type | Path / Format | Scope | Primary Purpose |
| :--- | :--- | :--- | :--- |
| **Skill** | `skills/<name>/SKILL.md` | On-Demand (Triggered) | Multi-step workflows, runbooks, procedural knowledge, tool scripts. |
| **Rule** | `AGENTS.md`, `GEMINI.md` | Contextual / Always-On | Universal constraints, coding standards, directory conventions. |
| **Plugin** | `plugin.json` bundle | Package | Bundles related skills, rules, and MCP servers together. |
| **MCP** | `mcp_config.json` | Tool integration | Exposes external server APIs and tools via Model Context Protocol. |

---

## 6. Execution Guidelines for Agents

When an agent executes an Antigravity skill:
1. **Never dump large script outputs to stdout**: Always write results to JSON or Markdown files and print only a compact summary to stdout.
2. **Follow progressive reading**: Do not view every file in `references/` upfront; view only the specific reference relevant to the sub-step.
3. **Handle errors gracefully**: Scripts must return actionable error messages containing HTTP status, endpoint URL, and error response bodies to enable self-correction.
