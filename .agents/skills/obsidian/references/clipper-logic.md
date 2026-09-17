# Obsidian Web Clipper Template Logic

**Official docs:** [Logic - Obsidian Help](https://help.obsidian.md/web-clipper/logic)

As of **Obsidian Web Clipper 1.0.0**, templates support logic in `noteContentFormat` and in property `value` fields: conditionals, loops, variable assignment, and fallbacks.

## When to use logic

- **Conditionals:** Show optional sections only when data exists (e.g. nutrition block only if `{{schema:Recipe:nutrition}}` is present).
- **Variable assignment:** Assign a value once and reuse it in the template to avoid repeating long expressions.
- **Fallbacks:** Provide a default when a variable is empty so the note still looks correct.
- **Loops:** Iterate over arrays (ingredients, steps, tags) to format each item; combine with filters for list/table output.

Keep simple templates simple; add logic only when it improves the result or avoids broken output for missing data.

## Conditionals

Conditionals include or exclude blocks based on whether a value exists or meets a condition.

- **Comparison operators:** Compare two values (equals, not equals, greater than, less than). Exact operators are defined in the official Logic page.
- **Logical operators:** Combine or negate conditions (`&&`, `||`, `!`).
- **Truthiness:** Empty strings, empty arrays, and missing variables are falsy; non-empty values are truthy.

## Assign a variable

Assign a variable once and reuse it in the same template.
Use this to avoid repeating long variable or filter chains.
Exact syntax is in the official Logic documentation.

## Fallbacks

- **Default when missing:** Provide a fallback value for empty variables.
- **Chaining fallbacks:** Chain multiple fallbacks (try variable A, then B, then a literal default). First non-empty value is used.
- **With filters:** Fallbacks can be used together with filters.

## Loops

- **Loop sources:** Typically a variable that returns a list (e.g. `{{schema:Recipe:recipeIngredient}}`).
- **Loop variables:** Current item variable, index, and loop metadata.
- **Nested loops:** Supported for arrays of structured data.
- **Combine logic:** Loops and conditionals can be combined.

## Template validation

The Obsidian Web Clipper template editor **validates template syntax**.
Invalid logic will be reported in the editor.
Use only constructs described on the official Logic page.
