# /// script
# requires-python = ">=3.10"
# dependencies = ["mlx-whisper>=0.4.0"]
# ///
"""
Transcribe a wav file into a TIMESTAMPED SRT using mlx-whisper.

Why this exists alongside transcribe.py:
    transcribe.py (Qwen3-ASR) returns flat text with NO timestamps — great for
    the readable transcript and metadata, useless for subtitles. Subtitle tracks
    (and especially *translated* tracks) need real per-segment timing. Whisper
    (whisper-large-v3-turbo) emits segment start/end times, so we use it as the
    timing backbone for the whole multilingual subtitle set: every translated
    track reuses these exact timestamps.

Usage:
    uv run transcribe_srt.py INPUT.wav OUTPUT.srt [--language en]

Outputs:
    - OUTPUT.srt                       (raw, timestamped — clean it before publishing)
    - OUTPUT.segments.json             (compact [{i,start,end,text}] for translation reuse)
    - JSON {"segments": N, "srt": path, "duration_seconds": float} to stdout
"""
import argparse
import json
import sys


def fmt_ts(seconds: float) -> str:
    """SRT timestamp: HH:MM:SS,mmm"""
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(segments) -> str:
    lines = []
    n = 0
    for seg in segments:
        text = seg["text"].strip()
        if not text:
            continue
        n += 1
        lines.append(f"{n}\n{fmt_ts(seg['start'])} --> {fmt_ts(seg['end'])}\n{text}\n")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="wav -> timestamped SRT via mlx-whisper")
    p.add_argument("input", help="Input wav (16kHz mono recommended)")
    p.add_argument("output", help="Output .srt path")
    p.add_argument("--language", default="en", help="Spoken language code (default: en)")
    p.add_argument("--model", default="mlx-community/whisper-large-v3-turbo",
                   help="mlx-whisper model repo")
    args = p.parse_args()

    import mlx_whisper

    print(f"Transcribing {args.input} with {args.model} ({args.language})...",
          file=sys.stderr, flush=True)
    result = mlx_whisper.transcribe(
        args.input,
        path_or_hf_repo=args.model,
        language=args.language,
        word_timestamps=False,
        verbose=False,
    )
    segments = result["segments"]

    srt = build_srt(segments)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(srt)

    seg_json = [
        {"i": i, "start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for i, s in enumerate(
            (s for s in segments if s["text"].strip()), 1
        )
    ]
    seg_path = args.output.replace(".srt", ".segments.json")
    with open(seg_path, "w", encoding="utf-8") as f:
        json.dump(seg_json, f, ensure_ascii=False, indent=0)

    duration = segments[-1]["end"] if segments else 0.0
    print(f"Wrote {len(seg_json)} segments -> {args.output}", file=sys.stderr, flush=True)
    print(json.dumps({
        "segments": len(seg_json),
        "srt": args.output,
        "segments_json": seg_path,
        "duration_seconds": round(duration, 1),
    }))


if __name__ == "__main__":
    main()
