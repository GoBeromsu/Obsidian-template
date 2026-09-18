#!/usr/bin/env python3
"""Validation and linting tool for Antigravity Agent Skills.

Ensures that a skill complies with the official Antigravity specification:
- Valid YAML frontmatter with 'name' and 'description'
- Correct naming conventions and description length constraints
- Valid relative file links
- Token-efficient progressive disclosure structure
"""

import argparse
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(content: str):
    """Extract frontmatter lines from SKILL.md."""
    if not content.startswith("---"):
        return None, "File does not start with YAML frontmatter delimiter ('---')."

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Malformed frontmatter. Missing closing '---' delimiter."

    frontmatter_raw = parts[1].strip()
    body = parts[2]

    # Simple YAML key-value parser for name and description
    metadata = {}
    current_key = None
    current_val_lines = []

    for line in frontmatter_raw.splitlines():
        match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if match:
            if current_key:
                metadata[current_key] = "\n".join(current_val_lines).strip()
            current_key = match.group(1).strip()
            val = match.group(2).strip()
            if val in (">-", ">", "|", "|-"):
                current_val_lines = []
            else:
                current_val_lines = [val]
        elif current_key:
            current_val_lines.append(line.strip())

    if current_key:
        metadata[current_key] = " ".join(current_val_lines).strip()

    return metadata, body


def validate_skill(skill_path: Path) -> bool:
    errors = []
    warnings = []

    if not skill_path.exists() or not skill_path.is_dir():
        print(f"Error: Directory '{skill_path}' does not exist.")
        return False

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: Mandatory file '{skill_md}' not found.")
        return False

    content = skill_md.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    if metadata is None:
        errors.append(f"Frontmatter parsing error: {body}")
        metadata = {}

    # 1. Check 'name'
    name = metadata.get("name", "").strip()
    if not name:
        errors.append("Missing required frontmatter field: 'name'.")
    else:
        if len(name) > 64:
            errors.append(f"'name' exceeds 64 characters (currently {len(name)}).")
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            errors.append(f"'name' '{name}' must be lowercase alphanumeric with hyphens (e.g. 'my-skill').")
        if name != skill_path.name:
            warnings.append(f"'name' ('{name}') differs from directory name ('{skill_path.name}').")

    # 2. Check 'description'
    desc = metadata.get("description", "").strip()
    if not desc:
        errors.append("Missing required frontmatter field: 'description'.")
    else:
        if len(desc) > 1024:
            warnings.append(f"'description' is very long ({len(desc)} chars). Recommended maximum is 1024.")
        if len(desc) < 20:
            warnings.append(f"'description' is very short ({len(desc)} chars). Add clear trigger criteria.")
        if not any(k in desc.lower() for k in ("use when", "trigger", "사용", "요청")):
            warnings.append("Consider adding explicit trigger phrasing to description (e.g. 'Use when the user...').")

    # 3. Check line count (Progressive disclosure)
    lines = content.splitlines()
    if len(lines) > 500:
        warnings.append(
            f"SKILL.md is {len(lines)} lines long. For better token efficiency and progressive disclosure, "
            "move lengthy guidelines or schemas into 'references/'."
        )

    # 4. Check relative links in markdown body (excluding code blocks and inline code)
    # Strip fenced code blocks
    cleaned_body = re.sub(r"```[\s\S]*?```", "", body)
    # Strip inline code
    cleaned_body = re.sub(r"`[^`\n]+`", "", cleaned_body)

    link_pattern = re.compile(r"\[([^\]]+)\]\((?!https?:\/\/|mailto:)([^\)]+)\)")
    for match in link_pattern.finditer(cleaned_body):
        link_target = match.group(2).split("#")[0].strip()
        if not link_target:
            continue
        target_path = (skill_path / link_target).resolve()
        try:
            # Ensure it is within the skill directory or workspace
            if not target_path.exists():
                errors.append(f"Broken relative link in SKILL.md: '{link_target}' (file not found).")
        except Exception as e:
            errors.append(f"Invalid link path '{link_target}': {e}")

    # 5. Check scripts directory if present
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for script_file in scripts_dir.glob("*.py"):
            try:
                code = script_file.read_text(encoding="utf-8")
                compile(code, str(script_file), "exec")
            except SyntaxError as e:
                errors.append(f"Python syntax error in '{script_file.name}': {e}")

    # Output results
    print(f"\nLinting Antigravity Skill: {skill_path.resolve()}")
    print("=" * 60)

    if errors:
        print("\n❌ ERRORS:")
        for err in errors:
            print(f"  - {err}")

    if warnings:
        print("\n⚠️ WARNINGS:")
        for warn in warnings:
            print(f"  - {warn}")

    if not errors and not warnings:
        print("\n✅ All checks passed! The skill conforms to Antigravity standards.")
    elif not errors:
        print("\n✅ Skill is valid (with warnings).")

    return len(errors) == 0


def main():
    parser = argparse.ArgumentParser(description="Validate an Antigravity Agent Skill.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Path to the skill directory (default: current directory)")
    args = parser.parse_args()

    target = Path(args.skill_dir).resolve()
    valid = validate_skill(target)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
