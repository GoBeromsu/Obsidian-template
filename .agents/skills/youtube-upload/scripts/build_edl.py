#!/usr/bin/env python3
"""Build a dead-air + stammer cut EDL and its ffmpeg filtergraph.

Consumes three inputs derived from a single raw take and emits two files:
  <out>.json  — the edit decision list (keep segments, stats, chapter seeds)
  <out>.fc    — an ffmpeg `-/filter_complex <out>.fc` graph that cuts in one pass

Two removal sources are merged onto one timeline, inverted to keep-segments, and
written as a split/trim/concat graph (robust for hundreds of segments — a single
giant select='between(...)+...' expression fails at init with "Cannot allocate
memory" past ~130 terms). Verified HLG/BT.2020 sources get a final HLG->SDR
hable tonemap with dithering; SDR BT.709 sources do not.

  1. Silence dead-air — remove silences >= MIN_SILENCE, keeping PAD seconds of
     breathing room on each side (larger PAD = looser, less choppy).
  2. Repeated stammer / false-start — from word-level ASR, a run of the same
     normalized token repeated within STAMMER_GAP seconds is a stutter
     ("our, our, ourrr agent"); keep only the LAST occurrence in the run.
  3. Energy snap — every removal boundary is snapped to the local audio-energy
     MINIMUM within +-SNAP_WIN, so a splice lands at the quietest nearby instant
     (a real gap) and never clips a syllable. This is what keeps cuts from
     landing mid-word; silencedetect edges and whisper word-starts alone do not.

Inputs:
  --silence  ffmpeg silencedetect log (stderr capture); see SKILL.md Step 0
  --words    mlx-whisper word-timestamp JSON, or "-" to skip stammer removal
  --wav      16 kHz mono PCM wav of the take (drives the energy snap)
  --duration take duration in seconds (ffprobe format=duration)
  --out      output basename (writes <out>.json and <out>.fc)
  --source-video source video to inspect with ffprobe (required in auto mode)
  --source-color auto, sdr-bt709, or hlg-bt2020

Every tuning value is an env-var default (YT_*) overridable by the matching flag.
A sibling .env (KEY=VALUE lines) seeds any YT_* not already set in the process
environment. Precedence: CLI flag > shell-exported YT_* > .env > built-in default
(a value already exported in the shell shadows the .env line of the same name).
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import wave
from itertools import accumulate
from os import environ

DEFAULTS = {
    "MIN_SILENCE": 1.2,     # only cut silences at least this long (dead air)
    "CUT_PAD": 0.28,        # breathing room kept each side of speech
    "MIN_KEEP": 0.30,       # drop kept slivers shorter than this
    "MERGE_GAP": 0.55,      # merge two keeps if the removed gap between them < this
    "STAMMER_GAP": 1.0,     # max gap between repeats to count as one stammer run
    "STAMMER_MIN": 2,       # >= this many same-token hits triggers a cut
    "STAMMER_MINCUT": 0.15, # skip stammer removals shorter than this (micro-jumps)
    "SNAP_WIN": 0.20,       # energy-snap search half-window, seconds
    "SNAP_FRAME": 0.010,    # energy hop, seconds
    "TONEMAP_NPL": 100.0,   # display peak luminance for the linear-light stage
}
INT_KEYS = {"STAMMER_MIN"}

# String-valued color knobs (resolved like DEFAULTS but never cast to a number).
STR_DEFAULTS = {
    "COLOR_LOOK": "hable",         # tonemap operator: hable | mobius | reinhard
    "DITHER": "error_diffusion",   # zscale dithering — prevents tonemap banding
}


def load_dotenv(path):
    if not path or not os.path.isfile(path):
        return
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        # Only fills in a var the process environment doesn't already have —
        # an exported YT_* still wins over the .env value of the same name.
        environ.setdefault(k.strip(), v.split("#", 1)[0].strip())


def resolve(args):
    cfg = {}
    for k, d in DEFAULTS.items():
        flag = getattr(args, k.lower())
        env = os.environ.get("YT_" + k)
        val = flag if flag is not None else (env if env is not None else d)
        cfg[k] = int(val) if k in INT_KEYS else float(val)
    for k, d in STR_DEFAULTS.items():
        flag = getattr(args, k.lower())
        env = os.environ.get("YT_" + k)
        cfg[k] = flag if flag is not None else (env if env is not None else d)
    return cfg


# ---------- source color classification ----------
COLOR_MODES = ("auto", "sdr-bt709", "hlg-bt2020")


def probe_source_color(path):
    command = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=color_primaries,color_transfer,color_space",
        "-of", "json", path,
    ]
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True)
    except FileNotFoundError:
        raise SystemExit(
            "ERROR: ffprobe was not found while detecting source color. Install "
            "ffmpeg, or pass --source-color sdr-bt709|hlg-bt2020 explicitly.")
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or f"exit status {exc.returncode}"
        raise SystemExit(
            f"ERROR: ffprobe could not inspect --source-video {path!r}: {detail}. "
            "Fix the input/probe, or pass --source-color "
            "sdr-bt709|hlg-bt2020 explicitly.")
    try:
        data = json.loads(result.stdout)
        stream = data["streams"][0]
        if not isinstance(stream, dict):
            raise TypeError
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        raise SystemExit(
            f"ERROR: ffprobe returned no readable video color metadata for "
            f"--source-video {path!r}. Fix the input/probe, or pass "
            "--source-color sdr-bt709|hlg-bt2020 explicitly.")
    metadata = {}
    for key in ("color_primaries", "color_transfer", "color_space"):
        value = stream.get(key)
        metadata[key] = (
            str(value).strip().lower() if value is not None else None)
        if not metadata[key]:
            metadata[key] = None
    return metadata


def choose_color_path(mode, source_video):
    if mode != "auto":
        metadata = {
            "color_primaries": None,
            "color_transfer": None,
            "color_space": None,
        }
        detected_by = "explicit"
        source_color = mode
    else:
        if not source_video:
            raise SystemExit(
                "ERROR: --source-video is required when --source-color=auto. "
                "Provide the video for ffprobe, or explicitly pass "
                "--source-color sdr-bt709|hlg-bt2020.")
        metadata = probe_source_color(source_video)
        detected_by = "ffprobe"
        values = (
            metadata["color_primaries"],
            metadata["color_transfer"],
            metadata["color_space"],
        )
        if values == ("bt709", "bt709", "bt709"):
            source_color = "sdr-bt709"
        elif values == ("bt2020", "arib-std-b67", "bt2020nc"):
            source_color = "hlg-bt2020"
        else:
            shown = ", ".join(
                f"{key}={value or 'missing'}" for key, value in metadata.items())
            if metadata["color_transfer"] == "smpte2084":
                reason = "PQ/SMPTE ST 2084 is not supported by this EDL tonemap"
            else:
                reason = "metadata is missing, unknown, or inconsistent"
            raise SystemExit(
                f"ERROR: cannot choose a safe color path: {reason} ({shown}). "
                "Correct the source metadata, or explicitly pass "
                "--source-color sdr-bt709|hlg-bt2020 after verifying the source.")

    path = (
        "bt709-sdr-passthrough"
        if source_color == "sdr-bt709"
        else "hlg-bt2020-to-bt709-sdr"
    )
    return {
        "mode": mode,
        "detected_by": detected_by,
        "source_video": source_video,
        "source_metadata": metadata,
        "source_color": source_color,
        "path": path,
    }


# ---------- energy envelope (prefix-sum windowed RMS, no external deps) ----------
class Energy:
    def __init__(self, wav_path, frame, win_s=0.025):
        import array
        w = wave.open(wav_path, "rb")
        self.sr = w.getframerate()
        ch = w.getnchannels()
        sw = w.getsampwidth()
        raw = w.readframes(w.getnframes())
        w.close()
        if sw != 2:  # array('h') below assumes 16-bit; anything else silently corrupts snaps
            raise SystemExit(
                f"--wav must be 16-bit PCM (got sampwidth={sw}); re-extract with: "
                "ffmpeg -i IN -vn -acodec pcm_s16le -ar 16000 -ac 1 OUT.wav")
        a = array.array("h")
        a.frombytes(raw)
        if ch == 2:
            a = a[0::2]
        sq = [float(x) * float(x) for x in a]
        self.pref = [0.0] + list(accumulate(sq))
        self.hop = max(1, int(frame * self.sr))
        self.win = max(self.hop, int(win_s * self.sr))
        self.n = len(a)

    def _rms(self, sample):
        s = max(0, sample - self.win // 2)
        e = min(self.n, sample + self.win // 2)
        if e <= s:
            return 0.0
        return math.sqrt((self.pref[e] - self.pref[s]) / (e - s))

    def snap(self, t, win, forward):
        if forward:
            lo, hi = int((t - 0.06) * self.sr), int((t + win) * self.sr)
        else:
            lo, hi = int((t - win) * self.sr), int((t + 0.06) * self.sr)
        lo, hi = max(0, lo), min(self.n, hi)
        if hi <= lo:
            return t
        best_s, best_v, s = lo, None, lo
        while s <= hi:
            v = self._rms(s)
            if best_v is None or v < best_v:
                best_v, best_s = v, s
            s += self.hop
        return best_s / self.sr


# ---------- cut sources ----------
def parse_silence(path):
    starts, ends = [], []
    for line in open(path):
        m = re.search(r"silence_start:\s*(-?[0-9.]+)", line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r"silence_end:\s*([0-9.]+)", line)
        if m:
            ends.append(float(m.group(1)))
    n = min(len(starts), len(ends))
    return list(zip(starts[:n], ends[:n]))


def silence_removals(silences, cfg):
    out = []
    for s, e in silences:
        if (e - s) < cfg["MIN_SILENCE"]:
            continue
        rs, re_ = s + cfg["CUT_PAD"], e - cfg["CUT_PAD"]
        if re_ - rs > 0:
            out.append((rs, re_))
    return out


_norm = re.compile(r"[^0-9a-z가-힣]+")


def flatten_words(asr_path):
    data = json.load(open(asr_path))
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            t = _norm.sub("", w.get("word", "").lower())
            if t:
                words.append((t, float(w["start"]), float(w["end"])))
    return words


def stammer_removals(words, cfg):
    out = []
    i, n = 0, len(words)
    while i < n:
        tok = words[i][0]
        j, run = i + 1, [(words[i][1], words[i][2])]
        while j < n and words[j][0] == tok and (words[j][1] - run[-1][1]) <= cfg["STAMMER_GAP"]:
            run.append((words[j][1], words[j][2]))
            j += 1
        if len(run) >= cfg["STAMMER_MIN"]:
            rs, re_ = run[0][0], run[-1][0]
            if (re_ - rs) >= cfg["STAMMER_MINCUT"]:
                out.append((rs, re_))
            i = j
        else:
            i += 1
    return out


def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def keeps_from_removals(removals, duration, cfg):
    keeps, cur = [], 0.0
    for rs, re_ in merge(removals):
        rs = max(0.0, rs)
        if rs > cur:
            keeps.append([cur, rs])
        cur = max(cur, re_)
    if cur < duration:
        keeps.append([cur, duration])
    out = []
    for k in keeps:
        if out and (k[0] - out[-1][1]) < cfg["MERGE_GAP"]:
            out[-1][1] = k[1]
        else:
            out.append(k)
    return [(a, b) for a, b in out if (b - a) >= cfg["MIN_KEEP"]]


def write_filtergraph(path, keeps, look, npl, dither, color_path,
                      explicit_source_color=False):
    n = len(keeps)
    lines = [f"[0:v]split={n}" + "".join(f"[v{i}]" for i in range(n)) + ";",
             f"[0:a]asplit={n}" + "".join(f"[a{i}]" for i in range(n)) + ";"]
    for i, (a, b) in enumerate(keeps):
        lines.append(f"[v{i}]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[vt{i}];")
        lines.append(f"[a{i}]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[at{i}];")
    lines.append("".join(f"[vt{i}][at{i}]" for i in range(n)) +
                 f"concat=n={n}:v=1:a=1[vc][ac];")
    if color_path == "hlg-bt2020-to-bt709-sdr":
        # Verified HLG BT.2020 10-bit -> SDR Rec.709 conversion.
        input_color = (
            "primariesin=bt2020:transferin=arib-std-b67:matrixin=bt2020nc:"
            if explicit_source_color else ""
        )
        lines.append(f"[vc]zscale={input_color}t=linear:npl={npl:g},format=gbrpf32le,"
                     f"tonemap=tonemap={look}:desat=0,"
                     f"zscale=p=bt709:t=bt709:m=bt709:r=tv:d={dither},"
                     f"format=yuv420p[v];")
    elif color_path == "bt709-sdr-passthrough":
        lines.append("[vc]format=yuv420p[v];")
    else:
        raise ValueError(f"unsupported color path: {color_path}")
    lines.append("[ac]anull[a]")
    open(path, "w").write("\n".join(lines))


def main():
    p = argparse.ArgumentParser(description="Build dead-air+stammer cut EDL.")
    p.add_argument("--silence", required=True)
    p.add_argument("--words", required=True, help='word-timestamp JSON, or "-"')
    p.add_argument("--wav", required=True)
    p.add_argument("--duration", required=True, type=float)
    p.add_argument("--out", required=True)
    p.add_argument("--source-video",
                   help="video to inspect with ffprobe in auto color mode")
    p.add_argument("--source-color", choices=COLOR_MODES, default="auto",
                   help="source color mode (default: auto via --source-video)")
    p.add_argument("--look", dest="color_look", default=None,
                   help="tonemap operator (env YT_COLOR_LOOK; hable|mobius|reinhard)")
    p.add_argument("--dither", dest="dither", default=None,
                   help="zscale dither (env YT_DITHER)")
    p.add_argument("--env", default=None, help="path to a .env (KEY=VALUE)")
    for k in DEFAULTS:
        p.add_argument("--" + k.lower().replace("_", "-"), dest=k.lower(),
                       default=None)
    args = p.parse_args()

    env_path = args.env or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    load_dotenv(env_path)
    cfg = resolve(args)
    color = choose_color_path(args.source_color, args.source_video)

    sil = silence_removals(parse_silence(args.silence), cfg)
    words = flatten_words(args.words) if args.words != "-" else []
    stam = stammer_removals(words, cfg)

    eng = Energy(args.wav, cfg["SNAP_FRAME"])
    snapped = []
    for rs, re_ in merge(sil + stam):
        ns = eng.snap(rs, cfg["SNAP_WIN"], forward=True)
        ne = eng.snap(re_, cfg["SNAP_WIN"], forward=False)
        if ne - ns > 0.02:
            snapped.append((ns, ne))

    keeps = keeps_from_removals(snapped, args.duration, cfg)
    if not keeps:  # every segment removed -> split=0/concat=n=0 would crash ffmpeg
        raise SystemExit(
            "ERROR: every segment was removed — nothing left to keep. Loosen "
            "MIN_SILENCE / MIN_KEEP / CUT_PAD, or check the input take.")
    kept = sum(b - a for a, b in keeps)
    # chapter seeds: the start of each kept segment is a candidate boundary
    json.dump({
        "source_duration": round(args.duration, 3),
        "kept_duration": round(kept, 3),
        "removed_duration": round(args.duration - kept, 3),
        "num_segments": len(keeps),
        "stammer_cuts": len(stam),
        "color": color,
        "config": cfg,
        "keeps": [[round(a, 3), round(b, 3)] for a, b in keeps],
        "chapter_seed_starts": [round(a, 3) for a, _ in keeps],
    }, open(args.out + ".json", "w"), indent=2, ensure_ascii=False)
    write_filtergraph(args.out + ".fc", keeps,
                      cfg["COLOR_LOOK"], cfg["TONEMAP_NPL"], cfg["DITHER"],
                      color["path"], color["detected_by"] == "explicit")

    print(f"{args.out}: {args.duration:.1f}s -> {kept:.1f}s "
          f"(cut {args.duration - kept:.1f}s, {len(keeps)} segments, "
          f"{len(stam)} stammer-runs removed)", file=sys.stderr)


if __name__ == "__main__":
    main()
