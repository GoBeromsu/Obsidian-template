# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client>=2.0", "google-auth>=2.0", "google-auth-oauthlib>=1.0"]
# ///
"""
Upload caption (subtitle) tracks to a YouTube video via Data API v3.

This complements upload.py: upload.py handles the video + snippet + localizations
(title/description per locale); subtitle.py handles actual closed-caption .srt
tracks per language, which the localizations resource cannot carry.

Usage:
    # Upload one SRT per language from a directory (files named <code>.srt):
    uv run subtitle.py VIDEO_ID --dir /tmp/subs --langs en,es,hi,ar,fr,pt,ru,zh,ko

    # Upload a single track:
    uv run subtitle.py VIDEO_ID --file /tmp/subs/ko.srt --lang ko

    # List existing caption tracks:
    uv run subtitle.py VIDEO_ID --list

Behavior:
    - Skips a language whose track already exists, unless --replace is given
      (then it deletes the old track and re-inserts).
    - File code -> YouTube BCP-47 caption language is normalized (e.g. zh -> zh-Hans).

Credentials: same as upload.py
    YT_CREDENTIALS_PATH  ~/.config/youtube-upload/credentials.json
    YT_TOKEN_PATH         ~/.config/youtube-upload/token.json

Outputs JSON summary to stdout; status to stderr.
"""

import argparse
import json
import os
import sys
from pathlib import Path

if os.getenv("OAUTHLIB_INSECURE_TRANSPORT") != "1":
    raise RuntimeError("Set OAUTHLIB_INSECURE_TRANSPORT=1 before running this script.")

# force-ssl is required for the captions resource (plain "youtube" scope returns 403).
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
DEFAULT_CREDENTIALS = Path("~/.config/youtube-upload/credentials.json").expanduser()
DEFAULT_TOKEN = Path("~/.config/youtube-upload/token.json").expanduser()

# File-name code -> YouTube caption/localization BCP-47 language code.
LANG_MAP = {
    "zh": "zh-Hans",
    "zh-cn": "zh-Hans",
    "pt": "pt",
    "pt-br": "pt-BR",
}


def yt_lang(code: str) -> str:
    return LANG_MAP.get(code.lower(), code)


def get_credentials(credentials_path: Path, token_path: Path):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_path.write_text(creds.to_json())
        return creds
    if not credentials_path.exists():
        print(f"ERROR: OAuth credentials not found at {credentials_path}", file=sys.stderr)
        sys.exit(1)
    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json())
    return creds


def list_captions(youtube, video_id: str):
    resp = youtube.captions().list(part="snippet", videoId=video_id).execute()
    return {item["snippet"]["language"]: item["id"] for item in resp.get("items", [])}


def insert_caption(youtube, video_id: str, language: str, srt_path: str, name: str = ""):
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(srt_path, mimetype="application/octet-stream", resumable=False)
    body = {
        "snippet": {
            "videoId": video_id,
            "language": language,
            "name": name,
            "isDraft": False,
        }
    }
    resp = youtube.captions().insert(part="snippet", body=body, media_body=media).execute()
    return resp["id"]


def main():
    p = argparse.ArgumentParser(description="Upload YouTube caption tracks")
    p.add_argument("video_id")
    p.add_argument("--dir", help="Directory of <code>.srt files")
    p.add_argument("--langs", help="Comma-separated file codes to upload from --dir")
    p.add_argument("--file", help="Single SRT file")
    p.add_argument("--lang", help="Language code for --file")
    p.add_argument("--name", default="", help="Track display name (default: empty = default track)")
    p.add_argument("--replace", action="store_true", help="Replace existing track for a language")
    p.add_argument("--list", action="store_true", help="List existing caption tracks and exit")
    args = p.parse_args()

    creds_path = Path(os.getenv("YT_CREDENTIALS_PATH", str(DEFAULT_CREDENTIALS))).expanduser()
    token_path = Path(os.getenv("YT_TOKEN_PATH", str(DEFAULT_TOKEN))).expanduser()
    creds = get_credentials(creds_path, token_path)

    from googleapiclient.discovery import build

    youtube = build("youtube", "v3", credentials=creds)

    existing = list_captions(youtube, args.video_id)

    if args.list:
        print(json.dumps({"video_id": args.video_id, "existing": existing}, ensure_ascii=False))
        return

    # Build work list of (file_code, srt_path)
    jobs = []
    if args.file:
        if not args.lang:
            print("ERROR: --lang required with --file", file=sys.stderr)
            sys.exit(1)
        jobs.append((args.lang, args.file))
    elif args.dir and args.langs:
        for code in [c.strip() for c in args.langs.split(",") if c.strip()]:
            path = os.path.join(args.dir, f"{code}.srt")
            if not os.path.exists(path):
                print(f"WARN: missing {path}, skipping", file=sys.stderr)
                continue
            jobs.append((code, path))
    else:
        print("ERROR: provide --file/--lang or --dir/--langs", file=sys.stderr)
        sys.exit(1)

    results = []
    for code, path in jobs:
        lang = yt_lang(code)
        if lang in existing:
            if args.replace:
                youtube.captions().delete(id=existing[lang]).execute()
                print(f"Deleted existing {lang} track", file=sys.stderr, flush=True)
            else:
                print(f"Skip {lang}: track already exists (use --replace)", file=sys.stderr, flush=True)
                results.append({"lang": lang, "status": "skipped_exists"})
                continue
        cid = insert_caption(youtube, args.video_id, lang, path, args.name)
        print(f"Uploaded caption {lang} ({code}.srt) -> {cid}", file=sys.stderr, flush=True)
        results.append({"lang": lang, "status": "uploaded", "caption_id": cid})

    print(json.dumps({"video_id": args.video_id, "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
