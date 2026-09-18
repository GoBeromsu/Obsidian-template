#!/usr/bin/env -S uv run --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Fail-closed semantic policy review for a YouTube upload.

The review runs through the authenticated GJC route.  Private input is written to
an owner-readable prompt file rather than placed in process arguments, and GJC
runs without tools, sessions, repository rules, or a repository working tree.

Exit codes:
  0 — review completed and passed
  1 — input or reviewer execution/evidence error
  2 — completed review found policy violations above the threshold
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_POLICY = SKILL_DIR / "references" / "upload-policy.md"
DEFAULT_MODEL = "openai-codex/gpt-5.6-sol"
DEFAULT_TIMEOUT = 180
ALLOWED_SEVERITIES = {"high", "medium", "low"}
VIOLATION_FIELDS = {"rule", "category", "severity", "quote", "suggestion"}

PROMPT_TEMPLATE = """You are a fail-closed pre-upload semantic policy reviewer.
Review every character of the supplied transcript and public metadata against
POLICY. ASR may contain phonetic errors, so use context rather than exact term
matching. Be conservative about false positives, but report every violation.

Return exactly one JSON object, without markdown or prose, with this shape:
{{
  "input_digest": "{digest}",
  "violations": [
    {{
      "rule": "1.1",
      "category": "사람",
      "severity": "high",
      "quote": "an exact quote from the transcript or public metadata",
      "suggestion": "a concrete correction"
    }}
  ]
}}
The input_digest must be copied exactly. Each quote must be a non-empty verbatim
substring of the supplied transcript or rendered metadata. Use an empty
violations array only when the complete input has no violation.

INPUT DIGEST: {digest}

POLICY:
{policy}

PUBLIC METADATA (canonical JSON):
{metadata}

TRANSCRIPT:
{transcript}
"""


class ReviewError(RuntimeError):
    """A safe-to-display validation or backend error."""


def canonical_metadata(metadata: Any) -> str:
    if not isinstance(metadata, dict):
        raise ReviewError("metadata must be a JSON object")
    return json.dumps(metadata, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def input_digest(transcript: str, metadata_json: str, policy: str) -> str:
    payload = json.dumps(
        {"transcript": transcript, "metadata": metadata_json, "policy": policy},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def build_prompt(transcript: str, metadata_json: str, policy: str, digest: str) -> str:
    return PROMPT_TEMPLATE.format(
        digest=digest, policy=policy, metadata=metadata_json, transcript=transcript
    )


def requested_backend(model: str) -> tuple[str, str]:
    if "/" not in model:
        raise ReviewError("model must be a provider/model identifier")
    provider, model_id = model.split("/", 1)
    if not provider or not model_id:
        raise ReviewError("model must be a provider/model identifier")
    if "anthropic" in provider.lower():
        raise ReviewError("Anthropic providers are not supported by this validator")
    return provider, model_id


def _message_text(message: Any) -> str:
    if not isinstance(message, dict) or message.get("role") != "assistant":
        raise ReviewError("reviewer completion did not contain an assistant result")
    content = message.get("content")
    if not isinstance(content, list):
        raise ReviewError("reviewer completion contained malformed content")
    parts = [part.get("text") for part in content if isinstance(part, dict) and part.get("type") == "text"]
    if not parts or any(not isinstance(part, str) for part in parts):
        raise ReviewError("reviewer completion contained malformed text")
    return "".join(parts)


def _event_scope(event: dict[str, Any], label: str) -> tuple[str, int]:
    scope = event.get("scope")
    if not isinstance(scope, dict):
        raise ReviewError(f"{label} has no scope object")
    attempt = scope.get("attemptId")
    generation = scope.get("generation")
    if not isinstance(attempt, str) or not attempt:
        raise ReviewError(f"{label} has invalid attemptId")
    if isinstance(generation, bool) or not isinstance(generation, int) or generation < 1:
        raise ReviewError(f"{label} has invalid generation")
    return attempt, generation


def parse_gjc_output(raw: str, requested_model: str) -> tuple[dict[str, Any], dict[str, str]]:
    provider, model_id = requested_backend(requested_model)
    records: list[dict[str, Any]] = []
    try:
        for line in raw.splitlines():
            if line.strip():
                record = json.loads(line)
                if not isinstance(record, dict):
                    raise ValueError
                records.append(record)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ReviewError("reviewer returned malformed JSON event records") from exc

    if not records or records[0].get("type") != "session":
        raise ReviewError("reviewer lifecycle must begin with one session")
    sessions = [record for record in records if record.get("type") == "session"]
    if len(sessions) != 1 or not isinstance(sessions[0].get("id"), str) or not sessions[0]["id"]:
        raise ReviewError("reviewer lifecycle has an invalid session")

    starts = [
        (index, record)
        for index, record in enumerate(records)
        if record.get("type") == "agent_start"
    ]
    if len(starts) != 1:
        raise ReviewError("reviewer lifecycle requires exactly one agent_start")
    start_index, start = starts[0]
    attempt, generation = _event_scope(start, "agent_start")
    for index, record in enumerate(records):
        if "scope" not in record:
            continue
        if _event_scope(record, f"event {index} ({record['type']})") != (attempt, generation):
            raise ReviewError(
                f"reviewer event {index} scope does not match agent_start"
            )

    completions = [
        (index, record["message"])
        for index, record in enumerate(records)
        if record.get("type") == "message_end"
        and isinstance(record.get("message"), dict)
        and record["message"].get("role") == "assistant"
    ]
    if len(completions) != 1:
        raise ReviewError("reviewer lifecycle requires exactly one assistant message_end")

    message_index, message = completions[0]
    if _event_scope(records[message_index], "message_end") != (attempt, generation):
        raise ReviewError("assistant message_end scope does not match agent_start")
    actual_provider = message.get("provider")
    actual_model = message.get("model")
    response_id = message.get("responseId")
    stop_reason = message.get("stopReason")
    if actual_provider != provider or actual_model != model_id:
        raise ReviewError("reviewer used a provider or model different from the requested route")
    if "anthropic" in str(actual_provider).lower():
        raise ReviewError("reviewer used a disallowed Anthropic provider")
    if stop_reason != "stop" or not isinstance(response_id, str) or not response_id:
        raise ReviewError("reviewer result lacks successful completion evidence")

    agent_ends = [
        (index, record)
        for index, record in enumerate(records)
        if record.get("type") == "agent_end"
    ]
    if len(agent_ends) != 1:
        raise ReviewError("reviewer lifecycle requires exactly one agent_end")
    final_index, final = agent_ends[0]
    if final_index != len(records) - 1 or not start_index < message_index < final_index:
        raise ReviewError(
            "reviewer lifecycle must order agent_start, assistant message_end, agent_end"
        )
    if final.get("stopReason") != "completed":
        raise ReviewError("reviewer agent_end does not report successful completion")
    if _event_scope(final, "agent_end") != (attempt, generation):
        raise ReviewError("agent_end scope does not match agent_start")
    final_messages = final.get("messages")
    if not isinstance(final_messages, list):
        raise ReviewError("agent_end.messages must be an array")
    final_assistants = [
        item for item in final_messages
        if isinstance(item, dict) and item.get("role") == "assistant"
    ]
    if len(final_assistants) != 1:
        raise ReviewError("agent_end must contain exactly one assistant message")
    final_message = final_assistants[0]
    if any(
        final_message.get(key) != message.get(key)
        for key in ("provider", "model", "responseId", "stopReason")
    ):
        raise ReviewError("agent_end assistant identity/completion does not match message_end")
    if _message_text(final_message) != _message_text(message):
        raise ReviewError("agent_end assistant content does not match message_end")

    try:
        result = json.loads(_message_text(message))
    except json.JSONDecodeError as exc:
        raise ReviewError("reviewer result is not a JSON object") from exc
    if not isinstance(result, dict):
        raise ReviewError("reviewer result is not a JSON object")
    evidence = {
        "backend": "gjc",
        "provider": actual_provider,
        "model": actual_model,
        "response_id": response_id,
        "stop_reason": stop_reason,
    }
    return result, evidence


def validate_result(result: dict[str, Any], digest: str, evidence_text: str) -> list[dict[str, str]]:
    if set(result) != {"input_digest", "violations"}:
        raise ReviewError("reviewer result does not match the required schema")
    if result["input_digest"] != digest:
        raise ReviewError("reviewer result is not bound to the supplied inputs")
    violations = result["violations"]
    if not isinstance(violations, list):
        raise ReviewError("reviewer violations must be an array")
    checked: list[dict[str, str]] = []
    for violation in violations:
        if not isinstance(violation, dict) or set(violation) != VIOLATION_FIELDS:
            raise ReviewError("reviewer violation does not match the required schema")
        if any(not isinstance(violation[field], str) or not violation[field].strip() for field in VIOLATION_FIELDS):
            raise ReviewError("reviewer violation fields must be non-empty strings")
        if violation["severity"] not in ALLOWED_SEVERITIES:
            raise ReviewError("reviewer violation has an invalid severity")
        if violation["quote"] not in evidence_text:
            raise ReviewError("reviewer violation quote is absent from the reviewed inputs")
        checked.append(violation)
    return checked


def derive_passed(violations: list[dict[str, str]]) -> bool:
    high = sum(item["severity"] == "high" for item in violations)
    medium = sum(item["severity"] == "medium" for item in violations)
    return high == 0 and medium < 2


def call_model(prompt: str, model: str, timeout: int) -> tuple[dict[str, Any], dict[str, str]]:
    requested_backend(model)
    try:
        with tempfile.TemporaryDirectory(prefix="youtube-policy-review-") as directory:
            prompt_path = Path(directory) / "review-input.txt"
            prompt_path.write_text(prompt, encoding="utf-8")
            os.chmod(prompt_path, 0o600)
            command = [
                "gjc", "--model", model, "--print", "--mode", "json",
                "--no-tools", "--no-session", "--no-rules", "--thinking", "low",
                f"@{prompt_path}",
            ]
            completed = subprocess.run(
                command,
                cwd=directory,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
    except OSError as exc:
        raise ReviewError("gjc executable is unavailable") from exc
    except subprocess.TimeoutExpired as exc:
        raise ReviewError(f"gjc review timed out after {timeout} seconds") from exc
    if completed.returncode != 0:
        raise ReviewError(f"gjc review failed with exit status {completed.returncode}")
    return parse_gjc_output(completed.stdout, model)


def read_transcript(path: str) -> str:
    return sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pre-upload semantic policy validation gate")
    parser.add_argument("--transcript", required=True, help="Transcript file path or '-' for stdin")
    parser.add_argument("--metadata", required=True, help="JSON file containing public metadata")
    parser.add_argument("--policy", default=str(DEFAULT_POLICY), help="Policy markdown file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Non-Anthropic GJC provider/model")
    parser.add_argument("--max-chars", type=int, default=80000, help="Maximum accepted transcript characters")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="GJC timeout in seconds")
    return parser.parse_args()


def error_report(message: str) -> int:
    print(json.dumps({"passed": False, "violations": [], "error": message}), flush=True)
    return 1


def main() -> int:
    args = parse_args()
    try:
        if args.max_chars < 1 or args.timeout < 1:
            raise ReviewError("max-chars and timeout must be positive")
        policy = Path(args.policy).read_text(encoding="utf-8")
        transcript = read_transcript(args.transcript)
        if not policy.strip():
            raise ReviewError("policy must not be empty or whitespace-only")
        if not transcript.strip():
            raise ReviewError("transcript must not be empty or whitespace-only")
        if len(transcript) > args.max_chars:
            raise ReviewError(
                f"transcript has {len(transcript)} characters; limit is {args.max_chars}; "
                "increase --max-chars only when the selected model can review the full input"
            )
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        metadata_json = canonical_metadata(metadata)
        digest = input_digest(transcript, metadata_json, policy)
        prompt = build_prompt(transcript, metadata_json, policy, digest)
        result, review = call_model(prompt, args.model, args.timeout)
        violations = validate_result(result, digest, transcript + "\n" + metadata_json)
    except (OSError, UnicodeError, json.JSONDecodeError, ReviewError) as exc:
        return error_report(str(exc))

    passed = derive_passed(violations)
    report = {
        "passed": passed,
        "violations": violations,
        "checked_text_length": len(transcript),
        "input_digest": digest,
        "review": review,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
