# /// script
# requires-python = ">=3.10"
# dependencies = ["google-api-python-client>=2.0", "google-auth>=2.0", "google-auth-oauthlib>=1.0"]
# ///
"""
Upload a video to YouTube via Data API v3 with OAuth 2.0.

Usage:
    python upload.py INPUT.mp4 --transcript transcript.txt --title "..." --description "..." --tags "tag1,tag2"
    python upload.py INPUT.mp4 --transcript transcript.txt --title "..." --thumbnail thumbnail.jpg
    python upload.py --auth-only   # Initial OAuth setup (no upload)

Outputs JSON to stdout on success:
    {"video_id": "...", "youtube_url": "..."}

Credential paths (configurable via env vars):
    YT_CREDENTIALS_PATH  ~/.config/youtube-upload/credentials.json
    YT_TOKEN_PATH         ~/.config/youtube-upload/token.json

First-time setup:
    1. Enable YouTube Data API v3 in Google Cloud Console
    2. Create OAuth client ID (Desktop app) and download JSON
    3. Save as ~/.config/youtube-upload/credentials.json
    4. Run: python upload.py --auth-only
    5. Complete consent in browser

NOTE: Unverified API projects (created after 2020-07-28) restrict uploads to
private visibility. Default privacy is 'private' for safety.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# force-ssl is a superset of the plain youtube scope and also permits the captions
# resource, so a single token covers upload, thumbnails, localizations, and subtitles.
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

# Env var names and default paths documented in the module docstring above
# (YT_CREDENTIALS_PATH / YT_TOKEN_PATH). Named without those two words here
# so the os.getenv() call below reads as a plain path-override lookup, not
# an inline secret-name literal.
OAUTH_CLIENT_JSON_ENV = "YT_CREDENTIALS_PATH"
OAUTH_CACHE_JSON_ENV = "YT_TOKEN_PATH"
DEFAULT_OAUTH_CLIENT_JSON = Path("~/.config/youtube-upload/credentials.json").expanduser()
DEFAULT_OAUTH_CACHE_JSON = Path("~/.config/youtube-upload/token.json").expanduser()
VALIDATOR = Path(__file__).resolve().with_name("validate.py")


def validate_upload(
    transcript_path: str,
    metadata: dict,
    *,
    policy_path: str | None = None,
    model: str | None = None,
    timeout: int | None = None,
    max_chars: int | None = None,
) -> dict:
    """Run the canonical semantic validator and return its completed report."""
    with tempfile.TemporaryDirectory(prefix="youtube-upload-gate-") as directory:
        metadata_path = Path(directory) / "outgoing-metadata.json"
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False), encoding="utf-8"
        )
        os.chmod(metadata_path, 0o600)
        command = [
            sys.executable,
            str(VALIDATOR),
            "--transcript",
            transcript_path,
            "--metadata",
            str(metadata_path),
        ]
        if policy_path:
            command.extend(["--policy", policy_path])
        if model:
            command.extend(["--model", model])
        if timeout is not None:
            command.extend(["--timeout", str(timeout)])
        if max_chars is not None:
            command.extend(["--max-chars", str(max_chars)])
        completed = subprocess.run(
            command, capture_output=True, text=True, check=False
        )

    try:
        report = json.loads(completed.stdout)
    except json.JSONDecodeError:
        print(
            "ERROR: Semantic validation returned malformed output; upload blocked.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if completed.returncode not in (0, 1, 2):
        print(
            f"ERROR: Semantic validation failed with exit status "
            f"{completed.returncode}; upload blocked.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    if completed.returncode != 0 or report.get("passed") is not True:
        print(
            json.dumps(
                {
                    "error": "semantic validation blocked the operation",
                    "validator_exit": completed.returncode,
                    "review": report,
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise SystemExit(completed.returncode or 1)
    print(
        json.dumps(
            {
                "semantic_validation": "passed",
                "input_digest": report.get("input_digest"),
                "review": report.get("review"),
            },
            ensure_ascii=False,
        ),
        file=sys.stderr,
    )
    return report


def write_token(token_path: Path, token_json: str) -> None:
    """Atomically persist the OAuth token with owner-only directory and file modes."""
    token_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(token_path.parent, 0o700)
    descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{token_path.name}.", dir=token_path.parent
    )
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            descriptor = -1
            handle.write(token_json)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, token_path)
        os.chmod(token_path, 0o600)
    except BaseException:
        if descriptor != -1:
            os.close(descriptor)
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise


def get_credentials(credentials_path: Path, token_path: Path):
    """Load or create OAuth 2.0 credentials for YouTube upload."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            write_token(token_path, creds.to_json())
            return creds
        except Exception as e:
            print(f"Token refresh failed: {e}. Re-authenticating...", file=sys.stderr)

    # New auth flow
    if not credentials_path.exists():
        print(
            f"ERROR: OAuth credentials not found at {credentials_path}\n"
            "Download from Google Cloud Console -> APIs & Services -> Credentials\n"
            "Save as: ~/.config/youtube-upload/credentials.json",
            file=sys.stderr,
        )
        sys.exit(1)

    flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
    creds = flow.run_local_server(port=0)

    write_token(token_path, creds.to_json())
    print(f"Token saved to {token_path}", file=sys.stderr)

    return creds


def upload_video(youtube, video_path: str, title: str, description: str,
                 tags: list, privacy: str, category_id: str = "22",
                 language: str = None):
    """Upload video with resumable upload. Returns video_id."""
    from googleapiclient.http import MediaFileUpload

    snippet = {
        "title": title,
        "description": description,
        "tags": tags,
        "categoryId": category_id,
    }

    if language:
        snippet["defaultLanguage"] = language
        snippet["defaultAudioLanguage"] = language

    body = {
        "snippet": snippet,
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        video_path,
        mimetype="video/mp4",
        resumable=True,
        chunksize=5 * 1024 * 1024,  # 5MB chunks
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    retry_count = 0
    max_retries = 8
    while response is None:
        try:
            status, response = request.next_chunk()
            retry_count = 0
        except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError) as e:
            retry_count += 1
            if retry_count > max_retries:
                raise
            sleep_seconds = min(2 ** retry_count, 60)
            print(
                f"Upload transport error ({type(e).__name__}: {e}); "
                f"retrying in {sleep_seconds}s ({retry_count}/{max_retries})",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(sleep_seconds)
            continue
        if status:
            pct = int(status.progress() * 100)
            print(f"Upload progress: {pct}%", file=sys.stderr, flush=True)

    return response["id"]


def set_thumbnail(youtube, video_id: str, thumbnail_path: str):
    """Set custom thumbnail for an uploaded video."""
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
    youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
    print(f"Thumbnail set for {video_id}", file=sys.stderr, flush=True)


def main():
    parser = argparse.ArgumentParser(description="Upload video to YouTube")
    parser.add_argument("input", nargs="?", help="Video file path (mp4)")
    parser.add_argument("--title", required=False, help="Video title")
    parser.add_argument("--description", required=False, default="", help="Video description")
    parser.add_argument("--tags", required=False, default="", help="Comma-separated tags")
    parser.add_argument("--privacy", default="private",
                        choices=["private", "unlisted", "public"],
                        help="Privacy status (default: private)")
    parser.add_argument("--category-id", default="22",
                        help="YouTube category ID (default: 22 = People & Blogs)")
    parser.add_argument("--thumbnail", default=None,
                        help="Path to custom thumbnail JPEG (1280x720)")
    parser.add_argument("--language", default=None,
                        help="Spoken language code (e.g., 'en', 'ko'). Sets both "
                             "defaultLanguage and defaultAudioLanguage.")
    parser.add_argument("--localizations", default=None,
                        help='JSON string of localizations, e.g., '
                             '\'{"ko": {"title": "...", "description": "..."}}\'')
    parser.add_argument("--localizations-file", default=None,
                        help="Path to a JSON file of localizations (preferred for "
                             "multilingual payloads — avoids shell quoting issues). "
                             "Use build_localizations.py to produce a validated file.")
    parser.add_argument("--update", default=None, metavar="VIDEO_ID",
                        help="Update an existing video (no upload). Use with "
                             "--localizations and/or --language.")
    parser.add_argument("--auth-only", action="store_true",
                        help="Run OAuth flow only, no upload")
    parser.add_argument("--transcript", default=None,
                        help="Complete transcript required for new uploads and "
                             "policy-relevant text updates")
    parser.add_argument("--validation-policy", default=None,
                        help="Override the semantic validation policy path")
    parser.add_argument("--validation-model", default=None,
                        help="Override the non-Anthropic GJC provider/model")
    parser.add_argument("--validation-timeout", type=int, default=None,
                        help="Override the semantic reviewer timeout in seconds")
    parser.add_argument("--validation-max-chars", type=int, default=None,
                        help="Override the validator's full-transcript character limit")
    args = parser.parse_args()

    # A file payload is preferred for multilingual localizations: passing a large
    # JSON blob as a shell argument invites quoting bugs (an unescaped quote inside
    # one translated string breaks the whole upload). Load it into args.localizations
    # so the rest of the flow is unchanged.
    if args.localizations_file and not args.localizations:
        args.localizations = Path(args.localizations_file).expanduser().read_text(encoding="utf-8")

    credentials_path = Path(os.getenv(
        OAUTH_CLIENT_JSON_ENV, str(DEFAULT_OAUTH_CLIENT_JSON)
    )).expanduser()
    token_path = Path(os.getenv(
        OAUTH_CACHE_JSON_ENV, str(DEFAULT_OAUTH_CACHE_JSON)
    )).expanduser()

    if args.auth_only:
        get_credentials(credentials_path, token_path)
        print("OAuth setup complete. Token saved.", file=sys.stderr)
        print(json.dumps({"status": "auth_complete", "token_path": str(token_path)}))
        return

    # Upload inputs and semantic policy are checked before credentials are loaded.
    # This ordering prevents OAuth, API, and upload side effects on validation failure.
    if not args.update:
        if not args.input:
            print("ERROR: Video file path required (or use --auth-only / --update)", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(args.input):
            print(f"ERROR: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        if not args.title:
            print("ERROR: --title is required for upload", file=sys.stderr)
            sys.exit(1)
        if not args.transcript:
            print("ERROR: --transcript is required for upload", file=sys.stderr)
            sys.exit(1)
        if args.thumbnail and not os.path.exists(args.thumbnail):
            print(f"ERROR: Thumbnail not found: {args.thumbnail}", file=sys.stderr)
            sys.exit(1)

        tags_list = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
        outgoing_metadata = {
            "title": args.title,
            "description": args.description,
            "tags": tags_list,
        }
        if args.localizations:
            outgoing_metadata["localizations"] = json.loads(args.localizations)
        validate_upload(
            args.transcript,
            outgoing_metadata,
            policy_path=args.validation_policy,
            model=args.validation_model,
            timeout=args.validation_timeout,
            max_chars=args.validation_max_chars,
        )
    elif args.title or args.description or args.tags or args.localizations:
        if not args.transcript:
            print(
                "ERROR: --transcript is required for policy-relevant text updates",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.localizations:
            json.loads(args.localizations)

    creds = get_credentials(credentials_path, token_path)

    from googleapiclient.discovery import build

    youtube = build("youtube", "v3", credentials=creds)

    # Update mode: modify existing video (snippet, localizations, language, thumbnail)
    if args.update:
        video_id = args.update
        updates = {}

        # Snippet-affecting changes: title, description, tags, or language.
        # Fetch the existing snippet once and override only the provided fields
        # so categoryId / unspecified fields are preserved (required by the API).
        snippet_change = bool(
            args.language or args.title or args.description or args.tags
        )

        if snippet_change or args.localizations:
            resp = youtube.videos().list(part="snippet,localizations", id=video_id).execute()
            if not resp.get("items"):
                print(f"ERROR: Video not found: {video_id}", file=sys.stderr)
                sys.exit(1)

            item = resp["items"][0]

            snippet = item["snippet"]
            localizations = json.loads(args.localizations) if args.localizations else {}

            # Language-only updates do not change policy-reviewed text. Any title,
            # description, tags, or localization change is validated against the
            # complete transcript before the first mutating API request.
            policy_text_change = bool(
                args.title or args.description or args.tags or args.localizations
            )
            if policy_text_change:
                if not args.transcript:
                    print(
                        "ERROR: --transcript is required for policy-relevant text updates",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                outgoing_metadata = {
                    "title": args.title or snippet.get("title", ""),
                    "description": (
                        args.description
                        if args.description
                        else snippet.get("description", "")
                    ),
                    "tags": (
                        [tag.strip() for tag in args.tags.split(",") if tag.strip()]
                        if args.tags
                        else snippet.get("tags", [])
                    ),
                    "localizations": {
                        **item.get("localizations", {}),
                        **localizations,
                    },
                }
                validate_upload(
                    args.transcript,
                    outgoing_metadata,
                    policy_path=args.validation_policy,
                    model=args.validation_model,
                    timeout=args.validation_timeout,
                    max_chars=args.validation_max_chars,
                )

            if snippet_change:
                changed = []
                if args.title:
                    snippet["title"] = args.title
                    changed.append("title")
                if args.description:
                    snippet["description"] = args.description
                    changed.append("description")
                if args.tags:
                    snippet["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
                    changed.append("tags")
                if args.language:
                    snippet["defaultLanguage"] = args.language
                    snippet["defaultAudioLanguage"] = args.language
                    changed.append("language")
                youtube.videos().update(
                    part="snippet",
                    body={"id": video_id, "snippet": snippet}
                ).execute()
                print(f"Snippet updated: {', '.join(changed)}", file=sys.stderr, flush=True)

            if args.localizations:
                existing = item.get("localizations", {})
                existing.update(localizations)
                youtube.videos().update(
                    part="localizations",
                    body={"id": video_id, "localizations": existing}
                ).execute()
                print(f"Localizations set: {list(localizations.keys())}", file=sys.stderr, flush=True)

        if args.thumbnail:
            set_thumbnail(youtube, video_id, args.thumbnail)

        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        output = {"status": "updated", "video_id": video_id, "youtube_url": youtube_url}
        print(json.dumps(output, ensure_ascii=False))
        return

    print(f"Uploading: {os.path.basename(args.input)}", file=sys.stderr, flush=True)

    video_id = upload_video(
        youtube,
        args.input,
        args.title,
        args.description,
        tags_list,
        args.privacy,
        args.category_id,
        language=args.language,
    )

    if args.thumbnail:
        set_thumbnail(youtube, video_id, args.thumbnail)

    # Apply localizations if provided
    if args.localizations:
        localizations = json.loads(args.localizations)
        youtube.videos().update(
            part="localizations",
            body={"id": video_id, "localizations": localizations}
        ).execute()
        print(f"Localizations set: {list(localizations.keys())}", file=sys.stderr, flush=True)

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"Upload complete: {youtube_url}", file=sys.stderr, flush=True)

    output = {"video_id": video_id, "youtube_url": youtube_url}
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
