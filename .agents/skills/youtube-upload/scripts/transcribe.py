# /// script
# requires-python = ">=3.10"
# dependencies = ["mlx-audio>=0.3.1"]
# ///
"""
Local English transcription using mlx-audio + Qwen3-ASR on Apple Silicon.

Usage:
    python transcribe.py INPUT.wav [--model MODEL] [--max-tokens N]

Outputs JSON to stdout:
    {"transcript": "...", "duration_seconds": 123.4, "language": "en"}

All status messages go to stderr so stdout remains clean JSON.

CRITICAL: max_tokens defaults to 200000. The upstream mlx-audio default (8192)
silently truncates audio longer than ~40 minutes.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time


def check_platform():
    if sys.platform != "darwin" or platform.machine() not in ("arm64", "aarch64"):
        print(
            "ERROR: Local MLX transcription requires macOS on Apple Silicon (M1+).",
            file=sys.stderr,
        )
        sys.exit(1)


def get_duration(file_path: str) -> float:
    """Get media duration in seconds via ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return float(result.stdout.strip())
    except Exception:
        return 0.0


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe video/audio to English text using mlx-audio Qwen3-ASR"
    )
    parser.add_argument("input", help="Video or audio file path (mp4, wav, etc.)")
    parser.add_argument(
        "--model",
        default="mlx-community/Qwen3-ASR-1.7B-8bit",
        help="HuggingFace model ID (default: Qwen3-ASR-1.7B-8bit)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=200000,
        help="Max generation tokens (default: 200000, covers ~3 hours)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    check_platform()

    # Get duration before loading the model
    duration = get_duration(args.input)
    if duration > 3600:
        print(
            f"WARNING: Video is {duration/60:.0f} minutes. Transcription may take several minutes.",
            file=sys.stderr,
        )

    from mlx_audio.stt.generate import load_model

    print(f"Loading model {args.model}...", file=sys.stderr, flush=True)
    t0 = time.time()
    model = load_model(args.model)
    load_time = time.time() - t0
    print(f"Model loaded in {load_time:.1f}s", file=sys.stderr, flush=True)

    print(f"Transcribing: {os.path.basename(args.input)}", file=sys.stderr, flush=True)
    t1 = time.time()

    # mlx-audio's model.generate() accepts video/audio files directly
    result = model.generate(args.input, max_tokens=args.max_tokens, verbose=True)

    elapsed = time.time() - t1
    text = result.text if hasattr(result, "text") else str(result)
    gen_tokens = result.generation_tokens if hasattr(result, "generation_tokens") else "N/A"

    print(
        f"Done: {elapsed:.1f}s, {len(text)} chars, {gen_tokens} tokens",
        file=sys.stderr,
        flush=True,
    )

    # If duration wasn't available from ffprobe, estimate from transcription speed
    if duration <= 0:
        duration = elapsed  # rough fallback

    output = {
        "transcript": text,
        "duration_seconds": round(duration, 1),
        "language": "en",
    }
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
