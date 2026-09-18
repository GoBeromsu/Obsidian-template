# /// script
# requires-python = ">=3.10"
# ///
"""
Merge per-language localization fragments into one validated localizations JSON
that upload.py can apply via `--update --localizations-file`.

Why this exists:
    Assembling multilingual title/description JSON by hand (or via inline shell)
    is a reliable source of bugs: unescaped quotes inside a foreign-language
    string break the whole payload, and translators routinely "fix" the chapter
    timestamps (0:00, 1:20, ...) into prose — which silently destroys YouTube
    chapter markers. This script merges fragments, then HARD-CHECKS two invariants
    before anything is uploaded:
      1. every localized title is <= 100 chars (YouTube's limit), and
      2. every localized description still contains all chapter timestamps.

Fragment format — one JSON object per file, keyed by BCP-47 locale:
    {"es": {"title": "...", "description": "..."}}
    {"zh-Hans": {"title": "...", "description": "..."}}

Usage:
    uv run build_localizations.py --dir /tmp/loc_frags --output /tmp/localizations.json
    uv run build_localizations.py --merge a.json b.json --output out.json
    # explicit chapter list (otherwise auto-derived from the 'en' description):
    uv run build_localizations.py --dir D --output O --chapters "0:00,1:20,3:10"

Exits non-zero with a readable report if any invariant fails — so a broken
translation is caught here, not after a half-applied upload.
"""
import argparse
import glob
import json
import re
import sys

TS_RE = re.compile(r"\b\d{1,2}:\d{2}\b")


def load_fragment(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def derive_chapters(merged):
    """Pull the ordered chapter timestamps from the en description if present,
    else from whichever locale has the most timestamp-looking tokens."""
    candidates = []
    if "en" in merged:
        candidates.append(merged["en"].get("description", ""))
    candidates += [b.get("description", "") for k, b in merged.items() if k != "en"]
    best = []
    for desc in candidates:
        found = TS_RE.findall(desc)
        if len(found) > len(best):
            best = found
        if "en" in merged and desc is candidates[0] and found:
            return found  # prefer en's exact set
    return best


def main():
    p = argparse.ArgumentParser(description="Merge + validate localization fragments")
    p.add_argument("--dir", help="Directory of *.json fragments")
    p.add_argument("--merge", nargs="*", default=[], help="Explicit fragment files")
    p.add_argument("--output", required=True, help="Output combined localizations JSON")
    p.add_argument("--chapters", default=None,
                   help="Comma-separated chapter timestamps every description must keep. "
                        "If omitted, derived from the 'en' description.")
    p.add_argument("--max-title-len", type=int, default=100)
    args = p.parse_args()

    paths = list(args.merge)
    if args.dir:
        paths += sorted(glob.glob(f"{args.dir}/*.json"))
    if not paths:
        print("ERROR: no fragments (use --dir and/or --merge)", file=sys.stderr)
        sys.exit(1)

    merged = {}
    bad_json = []
    for path in paths:
        try:
            frag = load_fragment(path)
        except json.JSONDecodeError as e:
            bad_json.append(f"{path}: {e}")
            continue
        for loc, body in frag.items():
            merged[loc] = body

    if bad_json:
        print("ERROR: malformed fragment JSON (often an unescaped quote in a translated string):",
              file=sys.stderr)
        for b in bad_json:
            print("  -", b, file=sys.stderr)
        sys.exit(1)

    required_ts = (
        [c.strip() for c in args.chapters.split(",") if c.strip()]
        if args.chapters else derive_chapters(merged)
    )

    problems = []
    for loc, body in merged.items():
        title = body.get("title", "")
        desc = body.get("description", "")
        if not title:
            problems.append(f"{loc}: missing title")
        if len(title) > args.max_title_len:
            problems.append(f"{loc}: title too long ({len(title)} > {args.max_title_len})")
        missing = [ts for ts in required_ts if ts not in desc]
        if missing:
            problems.append(f"{loc}: description dropped chapter timestamps {missing}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False)

    if problems:
        print("VALIDATION FAILED:", file=sys.stderr)
        for pr in problems:
            print("  -", pr, file=sys.stderr)
        print(json.dumps({"status": "invalid", "locales": list(merged), "problems": problems},
                         ensure_ascii=False))
        sys.exit(1)

    print(f"OK: {len(merged)} locales, all titles <= {args.max_title_len} chars, "
          f"all {len(required_ts)} chapter timestamps preserved", file=sys.stderr)
    print(json.dumps({
        "status": "ok",
        "output": args.output,
        "locales": list(merged),
        "chapters_checked": required_ts,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
