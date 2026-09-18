# Changelog

- 2026-09-10 — v1.0.1: Route CLI mechanics to the existing craft Obsidian package, distinguish community and app prerequisites, and replace the machine-specific write default and mixed move syntax with verified vault-aware operations. Preserve exact-path fallback limitations, Ataraxia template/provenance requirements, and existing book-content workflows in the output contract; no live vault operation was performed for this correction.

- 2026-07-02 — vault-path SSOT migration: retire `ATARAXIA_*` env vars in favor of `${OBSIDIAN_VAULT_PATH}` + canonical zone folders (`skills/rss/scripts/vault_paths.py`); bring frontmatter up to the 5-key contract (version/allowed-tools/compatibility) and add this changelog. (v1.0.0 — first versioned release)
