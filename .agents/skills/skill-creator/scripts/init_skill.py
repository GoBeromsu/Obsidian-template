#!/usr/bin/env python3
"""Scaffolding tool for Antigravity Agent Skills.

Creates a new standardized skill directory adhering to the official
Antigravity Agent Skills specification (https://antigravity.google/docs/skills/).
"""

import argparse
import os
import re
import stat
import sys
from pathlib import Path


SKILL_MD_TEMPLATE_INSTRUCTION = """---
name: {name}
description: >-
  [Provide a concise 3rd-person description of what the skill does and when the agent should use it].
  Use when the user asks to [action/keywords in Korean/English],
  or mentions "[trigger keyword 1]", "[trigger keyword 2]".
---

# {title}

## Overview
Briefly describe the purpose and capability of this skill.

## Workflow

### 1. Initial Assessment
- Step 1 instructions...
- Refer to [Reference Guide](./references/guide.md) for domain details.

### 2. Execution Steps
- Step 2 instructions...

### 3. Verification & Follow-up
- Step 3 verification instructions...

## Common Mistakes & Guardrails
- Avoid X when doing Y.
"""

SKILL_MD_TEMPLATE_SCRIPT = """---
name: {name}
description: >-
  [Provide a concise 3rd-person description of what the skill does and when the agent should use it].
  Use when the user asks to [action/keywords in Korean/English],
  or mentions "[trigger keyword 1]", "[trigger keyword 2]".
---

# {title}

## Overview
Briefly describe the purpose and capability of this skill.

## Commands

### 1. Run Search / Query
Execute the helper script and store output in a JSON file:
```bash
python3 ./scripts/{script_name}.py search --query "<query>" --output result.json
```

### 2. Process / Fetch Details
```bash
python3 ./scripts/{script_name}.py fetch --item-id "<id>" --output details.json
```

## Workflow
1. Run the appropriate command above.
2. Read the resulting JSON file using `view_file`.
3. Synthesize the findings and present the response to the user.

## Error Handling
- If the script encounters rate limiting, it will automatically back off.
- Check stderr for detailed API response bodies on failures.
"""

REFERENCE_TEMPLATE = """# {title} Reference Guide

Detailed domain reference, configuration schemas, or error codes.
Keep this separate from `SKILL.md` to ensure progressive disclosure and token efficiency.
"""


def validate_name(name: str) -> bool:
    """Ensure skill name satisfies Antigravity conventions."""
    if not name or len(name) > 64:
        return False
    return bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name))


def to_title(name: str) -> str:
    """Convert hyphenated name to Title Case."""
    return " ".join(word.capitalize() for word in name.split("-"))


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Antigravity skill.")
    parser.add_argument("name", help="Name of the skill (lowercase, alphanumeric and hyphens, e.g. code-audit)")
    parser.add_argument(
        "--scope",
        choices=["workspace", "global", "custom"],
        default="workspace",
        help="Target scope: 'workspace' (.agents/skills), 'global' (~/.gemini/antigravity/skills), or 'custom'",
    )
    parser.add_argument("--dest", help="Custom destination directory (used when scope is 'custom')")
    parser.add_argument(
        "--type",
        choices=["instruction", "script", "hybrid"],
        default="instruction",
        help="Skill type: 'instruction' (procedural only), 'script' (CLI tool backed), or 'hybrid'",
    )

    args = parser.parse_args()

    skill_name = args.name.strip().lower()
    if not validate_name(skill_name):
        sys.stderr.write(
            f"Error: Invalid skill name '{skill_name}'. "
            "Skill names must be lowercase alphanumeric with hyphens, and at most 64 characters.\n"
        )
        sys.exit(1)

    # Determine destination root
    if args.scope == "workspace":
        target_root = Path.cwd() / ".agents" / "skills"
    elif args.scope == "global":
        target_root = Path.home() / ".gemini" / "antigravity" / "skills"
    else:
        if not args.dest:
            sys.stderr.write("Error: --dest must be specified when --scope is 'custom'.\n")
            sys.exit(1)
        target_root = Path(args.dest)

    skill_dir = target_root / skill_name
    if skill_dir.exists():
        sys.stderr.write(f"Error: Directory already exists at {skill_dir}\n")
        sys.exit(1)

    title = to_title(skill_name)
    script_name = skill_name.replace("-", "_")

    # Create directory structure
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(exist_ok=True)
    (skill_dir / "examples").mkdir(exist_ok=True)

    # Populate references
    guide_file = skill_dir / "references" / "guide.md"
    guide_file.write_text(REFERENCE_TEMPLATE.format(title=title), encoding="utf-8")

    # Select template & populate scripts if needed
    if args.type in ("script", "hybrid"):
        (skill_dir / "scripts").mkdir(exist_ok=True)
        cli_py = skill_dir / "scripts" / f"{script_name}.py"
        
        # Read the CLI template from this skill's references if available
        current_script_dir = Path(__file__).resolve().parent
        template_cli_path = current_script_dir.parent / "references" / "cli-script-template.py"
        if template_cli_path.exists():
            cli_content = template_cli_path.read_text(encoding="utf-8")
        else:
            cli_content = "#!/usr/bin/env python3\n# Script placeholder\n"
        
        cli_py.write_text(cli_content, encoding="utf-8")
        cli_py.chmod(cli_py.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        skill_md_content = SKILL_MD_TEMPLATE_SCRIPT.format(
            name=skill_name, title=title, script_name=script_name
        )
    else:
        skill_md_content = SKILL_MD_TEMPLATE_INSTRUCTION.format(name=skill_name, title=title)

    (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

    print(f"Successfully scaffolded Antigravity skill '{skill_name}' at:")
    print(f"  {skill_dir}")
    print("\nNext steps:")
    print(f"  1. Edit {skill_dir / 'SKILL.md'} to define description and instructions.")
    print("  2. Add detailed reference docs into 'references/'.")
    if args.type in ("script", "hybrid"):
        print(f"  3. Implement script commands in 'scripts/{script_name}.py'.")
    print(f"  4. Validate using: python3 validate_skill.py {skill_dir}")


if __name__ == "__main__":
    main()
