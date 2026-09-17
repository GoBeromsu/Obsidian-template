# Working with Obsidian Bases

Bases are `.base` files (commonly kept in a Bases folder in the vault) that define the schema and properties for different note types.
Reuse those property definitions so a clipped note lands with the same frontmatter as everything else of its type.

## Workflow

1. **Identify the Category:** Determine the type of content to clip (e.g., Recipe, Article, YouTube video).
2. **Find the Base:** Search the vault's Bases folder for a matching `.base` file.
3. **Read the Base:** Read the content of the `.base` file to understand the required properties.

## Interpreting .base Files

Base files use a YAML-like structure.
Look for the `properties` section.

```yaml
properties:
  file.name:
    displayName: name
  note.author:
    displayName: author
  note.type:
    displayName: type
```

- `note.X` corresponds to a property name `X` in the frontmatter.
- `displayName` helps understand the intent, but the property key (e.g., `author`, `type`) is what matters for the template.

## Mapping to Clipper Properties

| Base Property | Clipper JSON Property Name | Value Strategy |
|---|---|---|
| `note.author` | `author` | `{{author}}` or `{{schema:author.name}}` |
| `note.source` | `source` | `{{url}}` |
| `note.published` | `published` | `{{published}}` |
| `note.type` | `type` | Constant (e.g., `Recipe`) or empty |

**Crucial Step:** Ask the user which properties should be automatically filled, which should be hardcoded, and which should be left empty for manual entry.
