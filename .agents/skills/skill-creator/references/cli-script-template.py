#!/usr/bin/env python3
"""Standard CLI script template for Antigravity Agent Skills.

Design Principles:
1. Subcommands: Map major workflow steps to CLI subcommands (argparse).
2. File Output: All data outputs must be saved to files via --output (never dump large JSON to stdout).
3. Token Efficient: Stdout is strictly for concise progress/summary messages.
4. Python stdlib preferred: Keep dependencies minimal (urllib, json, time, argparse).
5. Rate Limiting: Respect API quotas with exponential backoff on 429 and transient 5xx errors.
"""

import argparse
import json
import os
import sys
import time
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request


class RateLimitError(Exception):
    """Raised when API rate limits are encountered and exhausted."""
    pass


class APIClient:
    """Example API client with built-in rate limiting and backoff."""

    BASE_URL = "https://api.example.com/v1"
    REQUESTS_PER_SECOND = 2

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("EXAMPLE_API_KEY")
        self.delay = 1.0 / self.REQUESTS_PER_SECOND
        self.last_request_time = 0.0

    def _wait_for_rate_limit(self):
        """Throttle requests to satisfy the rate limit."""
        elapsed = time.monotonic() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

    def request(self, endpoint: str, params: dict = None, retries: int = 3) -> dict:
        """Make an HTTP GET request with retries and backoff."""
        url = f"{self.BASE_URL}{endpoint}"
        if params:
            url = f"{url}?{urllib_parse.urlencode(params)}"

        headers = {
            "Accept": "application/json",
            "User-Agent": "Antigravity-Agent-Skill/1.0"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(retries):
            self._wait_for_rate_limit()
            req = urllib_request.Request(url, headers=headers)
            try:
                with urllib_request.urlopen(req, timeout=30) as response:
                    self.last_request_time = time.monotonic()
                    data = response.read().decode("utf-8")
                    return json.loads(data)
            except urllib_error.HTTPError as e:
                self.last_request_time = time.monotonic()
                err_body = e.read().decode("utf-8", errors="replace")
                if e.code == 429:
                    wait_time = 2 ** attempt
                    sys.stderr.write(f"[Warning] Rate limited (429). Retrying in {wait_time}s...\n")
                    if attempt == retries - 1:
                        raise RateLimitError(f"HTTP 429: Rate limit exceeded for {url}: {err_body}")
                    time.sleep(wait_time)
                elif 500 <= e.code < 600:
                    wait_time = 2 ** attempt
                    sys.stderr.write(f"[Warning] Server error ({e.code}). Retrying in {wait_time}s...\n")
                    if attempt == retries - 1:
                        raise RuntimeError(f"Server error {e.code} for {url}: {err_body}")
                    time.sleep(wait_time)
                else:
                    raise RuntimeError(f"HTTP {e.code} error requesting {url}: {err_body}")
            except Exception as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"Network error requesting {url}: {e}")
                time.sleep(1)


def cmd_search(args):
    """Subcommand: search"""
    client = APIClient()
    results = {"query": args.query, "limit": args.limit, "items": []}
    
    # Perform actual query logic here
    # mock:
    results["items"] = [{"id": 1, "name": f"Result for {args.query}"}]

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Success: Found {len(results['items'])} items. Saved to {args.output}")


def cmd_fetch(args):
    """Subcommand: fetch item details"""
    client = APIClient()
    item = {"item_id": args.item_id, "status": "active"}

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(item, f, indent=2, ensure_ascii=False)

    print(f"Success: Details for {args.item_id} written to {args.output}")


def main():
    parser = argparse.ArgumentParser(description="Helper script for Antigravity skill.")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # Subcommand: search
    p_search = subparsers.add_parser("search", help="Search items by query")
    p_search.add_argument("--query", "-q", required=True, help="Search query string")
    p_search.add_argument("--limit", "-l", type=int, default=10, help="Max results to fetch")
    p_search.add_argument("--output", "-o", required=True, help="Path to output JSON file")
    p_search.set_defaults(func=cmd_search)

    # Subcommand: fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch item details")
    p_fetch.add_argument("--item-id", required=True, help="Item ID")
    p_fetch.add_argument("--output", "-o", required=True, help="Path to output JSON file")
    p_fetch.set_defaults(func=cmd_fetch)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
