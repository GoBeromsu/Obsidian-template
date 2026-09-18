#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests"]
# ///
"""Fetch ToC image URLs from Aladin product page.

Usage: uv run fetch_aladin_toc.py <ISBN13>
Output: JSON array of image URLs to stdout (skips _toc1 which is the book cover).
        Empty array if no ToC images found.
"""

import json
import re
import sys

import requests

HEADERS = {"User-Agent": "Mozilla/5.0"}


def fetch_toc_urls(isbn13: str) -> list[str]:
    resp = requests.get(
        f"https://www.aladin.co.kr/shop/wproduct.aspx?ISBN={isbn13}",
        headers=HEADERS,
        timeout=15,
    )
    resp.raise_for_status()
    urls = sorted(set(re.findall(
        r'//image\.aladin\.co\.kr/product/\d+/\d+/letslook/\w+_toc\d+\.jpg',
        resp.text,
    )))
    # Skip _toc1 (book cover), return the rest as full URLs
    return [f"https:{u}" for u in urls if not u.endswith("_toc1.jpg")]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_aladin_toc.py <ISBN13>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(fetch_toc_urls(sys.argv[1]), ensure_ascii=False, indent=2))
