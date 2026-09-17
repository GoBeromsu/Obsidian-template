# Analysis Workflow: Validating Variables

To ensure your template works correctly, you must validate that the target page actually contains the data you want to extract.

## 1. Fetch the Page

Retrieve the content of a representative URL (provided by the user) with a web fetch or extraction step — `defuddle`, a browser DOM snapshot, or an HTTP client.

```text
defuddle parse "https://example.com/recipe/chocolate-cake" --markdown
```

## 2. Analyze the Output

### Check for Schema.org (Recommended)

Look for `<script type="application/ld+json">`.
This contains structured data which is the most reliable way to extract info.

**Example Found in HTML:**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Chocolate Cake",
  "author": {
    "@type": "Person",
    "name": "John Doe"
  }
}
```

**Conclusion:**

- `{{schema:Recipe:name}}` is valid.
- `{{schema:Recipe:author.name}}` is valid.
- **Tip:** You can use `schema:Recipe` in the `triggers` array to automatically select this template for any page with this schema.

### Check for Meta Tags

Look for `<meta>` tags in the `<head>` section.

**Example Found in HTML:**

```html
<meta property="og:title" content="The Best Chocolate Cake" />
<meta name="description" content="A rich, moist chocolate cake recipe." />
```

**Conclusion:**

- `{{meta:og:title}}` is valid.
- `{{meta:description}}` is valid.

### Check for CSS Selectors (Verified)

If Schema and Meta tags are missing, look for HTML structure (classes and IDs) to use with `{{selector:...}}`.
Selectors must be verified against the fetched HTML or DOM snapshot.
Do not guess selectors.

## 3. Verify Against Base

Compare available data with properties required by the user's Base (see [clipper-bases-workflow.md](clipper-bases-workflow.md)).

- If the Base requires a field but the page has no Schema or clear structure, warn the user that this field might need manual entry or a prompt variable.
