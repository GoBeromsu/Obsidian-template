#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "beautifulsoup4", "markdownify"]
# ///
"""Fetch book metadata from yes24.com product page.

Usage: uv run fetch_yes24.py <URL>
Output: JSON to stdout with title, subtitle, authors, cover_url, description,
        date_published, isbn13, categories, toc, introduce, in_book, pub_review.
"""

import json
import re
import sys

import markdownify
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch(url: str) -> dict:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    sub_el = soup.select_one("#yDetailTopWrap h3")
    cover_el = soup.select_one("#yDetailTopWrap img.gImg")
    cover_url = (cover_el.get("src", "") if cover_el else "")
    if cover_url and not cover_url.startswith("http"):
        cover_url = "https:" + cover_url

    return {
        "title": _meta(soup, "title"),
        "subtitle": sub_el.get_text(strip=True) if sub_el else "",
        "authors": _authors(soup),
        "cover_url": cover_url,
        "description": _meta(soup, "description"),
        "date_published": _pub_date(soup),
        "isbn13": _isbn(soup),
        "categories": _categories(soup),
        "toc": _html_to_md(_textarea(soup, "infoset_toc")),
        "introduce": _html_to_md(_textarea(soup, "infoset_introduce")),
        "in_book": _html_to_md(_textarea(soup, "infoset_inBook")),
        "pub_review": _html_to_md(_textarea(soup, "infoset_pubReivew")),  # sic: yes24's typo
        "source_url": url,
    }


def _html_to_md(html: str) -> str:
    if not html:
        return ""
    text = markdownify.markdownify(html, strip=["img", "a"])
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _meta(soup: BeautifulSoup, name: str) -> str:
    el = soup.find("meta", attrs={"name": name})
    return el["content"].strip() if el and el.get("content") else ""


def _textarea(soup: BeautifulSoup, section_id: str) -> str:
    """yes24 stores HTML as entity-encoded text inside textareas.
    get_text() decodes entities → valid HTML for markdownify."""
    el = soup.select_one(f"#{section_id} textarea.txtContentText")
    return el.get_text().strip() if el else ""


def _authors(soup: BeautifulSoup) -> list[str]:
    """Return author names as plain strings (roles stripped)."""
    area = soup.select_one("span.gd_auth")
    if not area:
        return []
    links = area.select("a")
    if links:
        return [a.get_text(strip=True) for a in links if a.get_text(strip=True)]
    # Fallback: parse raw text
    raw = area.get_text(strip=True)
    raw = re.sub(r"\s*(저|역|편|감수|그림)\s*", " ", raw)
    return [n.strip() for n in re.split(r"[/,]", raw) if n.strip()]


def _pub_date(soup: BeautifulSoup) -> str:
    # Scope search to product info area to avoid matching stray dates
    area = soup.select_one("div.infoSetCont_wrap") or soup.select_one("table.tb_nor") or soup
    text = area.get_text()
    m = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
    return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else ""


def _isbn(soup: BeautifulSoup) -> str:
    meta = soup.find("meta", attrs={"property": "books:isbn"})
    if meta and meta.get("content"):
        return meta["content"]
    area = soup.select_one("div.infoSetCont_wrap") or soup.select_one("table.tb_nor") or soup
    m = re.search(r"ISBN\s*(?:13)?[:\s]*(\d{13})", area.get_text())
    return m.group(1) if m else ""


def _categories(soup: BeautifulSoup) -> list[str]:
    bc = soup.select_one("div.gd_goodsLocation")
    if not bc:
        return []
    skip = {"HOME", "국내도서", "외국도서"}
    return [a.get_text(strip=True) for a in bc.select("a")
            if a.get_text(strip=True) not in skip]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_yes24.py <yes24-product-url>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(fetch(sys.argv[1]), ensure_ascii=False, indent=2))
