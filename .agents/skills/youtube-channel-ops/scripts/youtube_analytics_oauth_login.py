#!/usr/bin/env python3
"""Refresh YouTube OAuth token with Analytics readonly scope.

This script is intentionally secret-safe in stdout/logs: it writes only auth URL,
status, and scope metadata. It does not print token values.

Expected files:
  ~/.config/youtube-upload/credentials.json
  ~/.config/youtube-upload/token.json

Outputs:
  /tmp/youtube_auth_url.txt
  /tmp/youtube_oauth_status.json
"""
from __future__ import annotations

import json
import os
import socket
import sys
import time
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except Exception as exc:  # pragma: no cover
    print(f"Missing google-auth-oauthlib: {exc}", file=sys.stderr)
    sys.exit(2)

CONFIG_DIR = Path.home() / ".config" / "youtube-upload"
CLIENT_SECRETS = CONFIG_DIR / "credentials.json"
TOKEN_PATH = CONFIG_DIR / "token.json"
AUTH_URL_PATH = Path("/tmp/youtube_auth_url.txt")
STATUS_PATH = Path("/tmp/youtube_oauth_status.json")
SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

# Installed-app OAuth redirects to localhost over HTTP; require the caller to
# opt in before starting the local development callback.
if os.getenv("OAUTHLIB_INSECURE_TRANSPORT") != "1":
    raise RuntimeError("Set OAUTHLIB_INSECURE_TRANSPORT=1 before running this script.")


def write_status(**data):
    safe = {k: v for k, v in data.items() if k not in {"token", "refresh_token", "client_secret"}}
    STATUS_PATH.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def main() -> int:
    if not CLIENT_SECRETS.exists():
        write_status(state="error", error=f"missing credentials: {CLIENT_SECRETS}")
        return 2

    port = int(os.getenv("YOUTUBE_OAUTH_PORT") or free_port())
    redirect_uri = f"http://127.0.0.1:{port}/"
    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRETS), scopes=SCOPES)
    flow.redirect_uri = redirect_uri

    # Do not pass include_granted_scopes=true here; Google may return a superset
    # of old scopes and google-auth-oauthlib can reject it as "Scope has changed".
    auth_url, _state = flow.authorization_url(
        access_type="offline",
        prompt="consent",
    )
    AUTH_URL_PATH.write_text(auth_url, encoding="utf-8")
    write_status(state="waiting_for_browser", redirect_uri=redirect_uri, scopes=SCOPES)
    print(f"Open OAuth URL from {AUTH_URL_PATH}", flush=True)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # keep logs quiet
            return

        def do_GET(self):  # noqa: N802
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            if "error" in params:
                err = params.get("error", ["unknown"])[0]
                write_status(state="error", error=err)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"OAuth error. You can close this tab.")
                return
            if "code" not in params:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing OAuth code; waiting for the real callback.")
                return
            try:
                full_url = redirect_uri.rstrip("/") + self.path
                flow.fetch_token(authorization_response=full_url)
                creds = flow.credentials
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
                os.chmod(TOKEN_PATH, 0o600)
                write_status(
                    state="auth_complete",
                    token_path=str(TOKEN_PATH),
                    scopes=sorted(list(creds.scopes or [])),
                    has_yt_analytics_readonly="https://www.googleapis.com/auth/yt-analytics.readonly" in (creds.scopes or []),
                    expiry=creds.expiry.isoformat() if creds.expiry else None,
                )
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"YouTube OAuth complete. You can close this tab.")
            except Exception as exc:
                write_status(state="error", error=str(exc), traceback=traceback.format_exc(limit=5))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"OAuth token exchange failed. Check /tmp/youtube_oauth_status.json.")

    server = HTTPServer(("127.0.0.1", port), Handler)
    try:
        deadline = time.time() + 15 * 60
        while time.time() < deadline:
            if STATUS_PATH.exists():
                try:
                    state = json.loads(STATUS_PATH.read_text(encoding="utf-8")).get("state")
                except Exception:
                    state = None
                if state in {"auth_complete", "error"}:
                    break
            server.timeout = 5
            server.handle_request()
        else:
            write_status(state="timeout", error="OAuth callback was not received within 15 minutes")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
