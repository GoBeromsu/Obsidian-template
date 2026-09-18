# /// script
# requires-python = ">=3.10"
# dependencies = ["Pillow>=10.0"]
# ///
"""
Generate a YouTube thumbnail: face photo + bold text overlay.

Usage:
    # Face-only mode (face fills canvas, text on left):
    python generate_thumbnail.py --face face.png --text "HOOK" --output thumb.jpg

    # Background mode (bg image + face inset + centered text):
    python generate_thumbnail.py --face face.png --background bg.png --text "HOOK" --output thumb.jpg

Output: 1280x720 JPEG.
"""

import argparse
import os
import sys
import textwrap
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1280, 720
BG_COLOR = (26, 26, 46)  # #1a1a2e dark navy
FONT_PATH = "/System/Library/Fonts/Supplemental/Impact.ttf"
FONT_INDEX = 0
FONT_MIN = 48
FONT_MAX = 140
MAX_LINES = 3

# Impact has no Hangul glyphs — Hangul hook text renders as tofu boxes.
# Tried in order; each entry is (path, ttc_index).
HANGUL_FONT_CANDIDATES = [
    (os.path.expanduser("~/Library/Fonts/NotoSansKR-Black.ttf"), 0),
    ("/Library/Fonts/NotoSansKR-Black.ttf", 0),
    ("/System/Library/Fonts/AppleSDGothicNeo.ttc", 16),  # Heavy
    ("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 0),
]


def _contains_hangul(text: str) -> bool:
    return any(
        "가" <= ch <= "힣"      # syllables
        or "ᄀ" <= ch <= "ᇿ"   # jamo
        or "㄰" <= ch <= "㆏"   # compatibility jamo
        for ch in text
    )


def select_font(text: str) -> None:
    """Switch to a Hangul-capable display font when the hook text needs one."""
    global FONT_PATH, FONT_INDEX
    if not _contains_hangul(text):
        return
    for path, index in HANGUL_FONT_CANDIDATES:
        if os.path.exists(path):
            FONT_PATH, FONT_INDEX = path, index
            _load_font.cache_clear()
            return
    print("WARNING: no Hangul-capable font found; text may render as boxes",
          file=sys.stderr)


def cover_crop(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    """Resize and center-crop image to exactly fill target dimensions."""
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h

    if img_ratio > target_ratio:
        new_h = target_h
        new_w = int(target_h * img_ratio)
    else:
        new_w = target_w
        new_h = int(target_w / img_ratio)

    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


@lru_cache(maxsize=32)
def _load_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size, index=FONT_INDEX)


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_w: int, max_h: int,
             stroke_width: int = 4):
    """Find optimal font size and line wrapping for the text region."""
    upper = text.upper()

    for size in range(FONT_MAX, FONT_MIN - 1, -4):
        font = _load_font(size)
        for wrap_w in range(len(upper), 3, -1):
            lines = textwrap.wrap(upper, width=wrap_w, break_long_words=False,
                                  break_on_hyphens=False)
            if len(lines) > MAX_LINES:
                break
            bboxes = [
                draw.textbbox((0, 0), ln, font=font, stroke_width=stroke_width)
                for ln in lines
            ]
            text_w = max(b[2] - b[0] for b in bboxes)
            line_h = max(b[3] - b[1] for b in bboxes)
            total_h = line_h * len(lines) + 12 * (len(lines) - 1)
            if text_w <= max_w and total_h <= max_h:
                return font, lines, line_h
            if total_h > max_h:
                break

    font = _load_font(FONT_MIN)
    lines = textwrap.wrap(upper, width=10)[:MAX_LINES]
    bbox = draw.textbbox((0, 0), lines[0], font=font, stroke_width=4)
    return font, lines, bbox[3] - bbox[1]


# ── Face-only mode (original) ────────────────────────────────────────────

def create_gradient() -> Image.Image:
    """Dark-to-transparent gradient overlay (left to right)."""
    text_max_x, gradient_end = 520, 700
    pixels = []
    for x in range(WIDTH):
        if x < text_max_x:
            pixels.append(210)
        elif x < gradient_end:
            progress = (x - text_max_x) / (gradient_end - text_max_x)
            pixels.append(int(210 * (1 - progress)))
        else:
            pixels.append(0)
    alpha_row = Image.new("L", (WIDTH, 1))
    alpha_row.putdata(pixels)

    alpha_full = alpha_row.resize((WIDTH, HEIGHT), Image.NEAREST)
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR + (255,))
    overlay.putalpha(alpha_full)
    return overlay


def generate_face_only(face_path: str, text: str, output_path: str):
    """Face fills canvas, dark gradient left, text on left side."""
    canvas = cover_crop(Image.open(face_path).convert("RGB"), WIDTH, HEIGHT)

    canvas_rgba = canvas.convert("RGBA")
    gradient = create_gradient()
    canvas_rgba = Image.alpha_composite(canvas_rgba, gradient)
    canvas = canvas_rgba.convert("RGB")

    draw = ImageDraw.Draw(canvas)
    margin = 60
    font, lines, line_h = fit_text(draw, text, 520 - margin * 2, HEIGHT - margin * 4)

    total_h = line_h * len(lines) + 12 * (len(lines) - 1)
    y_start = (HEIGHT - total_h) // 2

    for i, line in enumerate(lines):
        y = y_start + i * (line_h + 12)
        draw.text((margin, y), line, font=font, fill="white",
                  stroke_width=4, stroke_fill="black")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    canvas.save(output_path, "JPEG", quality=95)
    print(f"Thumbnail saved: {output_path} ({WIDTH}x{HEIGHT})", file=sys.stderr)


# ── Background mode (bg + face inset + centered text) ────────────────────

def generate_with_background(face_path: str, bg_path: str, text: str, output_path: str):
    """Background image + face inset (bottom-right) + centered text."""
    # 1. Background fills canvas
    bg = cover_crop(Image.open(bg_path).convert("RGB"), WIDTH, HEIGHT)
    canvas = bg.convert("RGBA")

    # 2. Dim overlay for text readability
    dim = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 120))
    canvas = Image.alpha_composite(canvas, dim)

    # 3. Face inset (bottom-right, circular mask with border)
    face_size = 220
    face_margin = 40
    face_img = cover_crop(Image.open(face_path).convert("RGB"), face_size, face_size)

    # Circular mask
    mask = Image.new("L", (face_size, face_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, face_size, face_size), fill=255)

    # White border circle
    border_size = face_size + 8
    border = Image.new("RGBA", (border_size, border_size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.ellipse((0, 0, border_size, border_size), fill=(255, 255, 255, 200))

    face_rgba = Image.new("RGBA", (face_size, face_size), (0, 0, 0, 0))
    face_rgba.paste(face_img, mask=mask)

    # Position: bottom-right
    bx = WIDTH - border_size - face_margin
    by = HEIGHT - border_size - face_margin
    canvas.paste(border, (bx, by), border)
    canvas.paste(face_rgba, (bx + 4, by + 4), face_rgba)

    # 4. Centered text
    canvas_rgb = canvas.convert("RGB")
    draw = ImageDraw.Draw(canvas_rgb)
    margin = 80
    font, lines, line_h = fit_text(draw, text, WIDTH - margin * 2, HEIGHT - margin * 2)

    total_h = line_h * len(lines) + 14 * (len(lines) - 1)
    y_start = (HEIGHT - total_h) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=5)
        line_w = bbox[2] - bbox[0]
        x = (WIDTH - line_w) // 2
        y = y_start + i * (line_h + 14)
        draw.text((x, y), line, font=font, fill="white",
                  stroke_width=5, stroke_fill="black")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    canvas_rgb.save(output_path, "JPEG", quality=95)
    print(f"Thumbnail saved: {output_path} ({WIDTH}x{HEIGHT})", file=sys.stderr)


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate YouTube thumbnail")
    parser.add_argument("--face", required=True, help="Path to face photo")
    parser.add_argument("--background", default=None,
                        help="Background image (graph view, etc.). Enables centered layout.")
    parser.add_argument("--text", required=True, help="Hook text (3-5 words)")
    parser.add_argument("--output", required=True, help="Output JPEG path")
    args = parser.parse_args()

    select_font(args.text)

    if not os.path.exists(args.face):
        print(f"ERROR: Face image not found: {args.face}", file=sys.stderr)
        sys.exit(1)

    if args.background:
        if not os.path.exists(args.background):
            print(f"ERROR: Background image not found: {args.background}", file=sys.stderr)
            sys.exit(1)
        generate_with_background(args.face, args.background, args.text, args.output)
    else:
        generate_face_only(args.face, args.text, args.output)


if __name__ == "__main__":
    main()
