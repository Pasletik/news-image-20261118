#!/usr/bin/env python3
"""Draw entry.png for the make.fun news-image-20261118 bounty.

One 1024x1024 infographic summing up Wednesday 18 November 2026:
a big date header plus six panels, each with a flat icon drawn from
scratch (Pillow primitives only), a short headline and one factual
sub-line. No photos, no external assets, no network.

Deterministic: fixed coordinates, fixed fonts, no randomness, so
re-running this script reproduces the identical PNG bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"
REGULAR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

NAVY = (15, 42, 74)
GOLD = (245, 179, 1)
PANEL_BG = (247, 243, 234)
HEADLINE = (22, 40, 63)
SUBLINE = (68, 86, 107)
WHITE = (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Word-wrap text to lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, path, start, minimum, max_w, max_lines):
    """Largest font size (shrinking by 2) whose wrap fits max_lines."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 2
    return font(path, minimum)


# ---------------------------------------------------------------- icons

def icon_missile(draw, cx, cy, color):
    """A missile streaking up-right, drawn on a layer then rotated."""
    layer = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # flame behind the tail
    ld.polygon([(8, 62), (30, 70), (8, 78)], fill=(245, 130, 1, 255))
    ld.polygon([(14, 58), (34, 70), (14, 82)], fill=(245, 179, 1, 255))
    # body
    ld.rounded_rectangle([28, 58, 96, 82], radius=10, fill=color + (255,))
    # nose
    ld.polygon([(96, 58), (122, 70), (96, 82)], fill=color + (255,))
    # fins
    ld.polygon([(34, 58), (48, 40), (56, 58)], fill=color + (255,))
    ld.polygon([(34, 82), (48, 100), (56, 82)], fill=color + (255,))
    # window
    ld.ellipse([84, 64, 94, 76], fill=(255, 255, 255, 255))
    layer = layer.rotate(-32, resample=Image.BICUBIC, center=(70, 70))
    draw._image.paste(layer, (cx - 70, cy - 70), layer)


def icon_flags(draw, cx, cy, color):
    """Two flags on poles: China (red, one gold star) and Russia (tricolour)."""
    # poles
    draw.line([(cx - 34, cy - 46), (cx - 34, cy + 48)], fill=(70, 80, 95), width=4)
    draw.line([(cx + 30, cy - 46), (cx + 30, cy + 48)], fill=(70, 80, 95), width=4)
    # China flag, upper left
    draw.rectangle([cx - 32, cy - 46, cx + 12, cy - 16], fill=(205, 32, 32))
    draw.ellipse([cx - 24, cy - 40, cx - 12, cy - 28], fill=(255, 215, 0))
    # Russia flag, lower right (white / blue / red bands)
    draw.rectangle([cx - 8, cy - 6, cx + 32, cy + 4], fill=(255, 255, 255))
    draw.rectangle([cx - 8, cy + 4, cx + 32, cy + 14], fill=(30, 90, 180))
    draw.rectangle([cx - 8, cy + 14, cx + 32, cy + 24], fill=(205, 32, 32))


def icon_ballot(draw, cx, cy, color):
    """A ballot box with a paper slip and a green check mark."""
    # paper slip sticking out of the slot
    draw.polygon(
        [(cx - 8, cy - 52), (cx + 18, cy - 52), (cx + 12, cy - 24), (cx - 14, cy - 24)],
        fill=(255, 255, 255),
        outline=(70, 80, 95),
    )
    draw.line([(cx - 4, cy - 44), (cx + 12, cy - 44)], fill=(120, 130, 145), width=2)
    draw.line([(cx - 4, cy - 36), (cx + 12, cy - 36)], fill=(120, 130, 145), width=2)
    # box
    draw.rounded_rectangle([cx - 40, cy - 24, cx + 40, cy + 48], radius=6,
                           fill=color, outline=(22, 40, 63), width=2)
    # slot
    draw.line([(cx - 22, cy - 24), (cx + 22, cy - 24)], fill=(22, 40, 63), width=4)
    # green check
    draw.line([(cx - 26, cy + 12), (cx - 10, cy + 28), (cx + 28, cy - 12)],
              fill=(30, 160, 90), width=8, joint="curve")


def icon_bridge(draw, cx, cy, color):
    """A bridge with a broken span: arched deck in two pieces, one falling."""
    # arch: a half-ellipse arc over the deck
    draw.arc([cx - 52, cy - 52, cx + 52, cy + 28], start=180, end=360,
             fill=color, width=5)
    # deck, left and right segments with a gap in the middle
    draw.line([(cx - 54, cy + 8), (cx - 12, cy + 8)], fill=color, width=7)
    draw.line([(cx + 12, cy + 8), (cx + 54, cy + 8)], fill=color, width=7)
    # short vertical suspenders from arch to deck
    for sx in (-38, -26, 26, 38):
        draw.line([(cx + sx, cy - 30), (cx + sx, cy + 8)], fill=color, width=2)
    # falling deck piece below the gap, tilted
    draw.polygon([(cx - 10, cy + 26), (cx + 12, cy + 20), (cx + 14, cy + 30), (cx - 8, cy + 36)],
                 fill=color)
    # water
    draw.line([(cx - 52, cy + 48), (cx - 20, cy + 48), (cx - 4, cy + 54), (cx + 28, cy + 54), (cx + 52, cy + 48)],
              fill=(60, 130, 190), width=3)


def icon_virus(draw, cx, cy, color):
    """A virus: spiked circle with a white medical cross inside."""
    for k in range(10):
        ang = 2 * math.pi * k / 10
        x1 = cx + int(26 * math.cos(ang))
        y1 = cy + int(26 * math.sin(ang))
        x2 = cx + int(38 * math.cos(ang))
        y2 = cy + int(38 * math.sin(ang))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=4)
        draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=color)
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=color)
    # white cross
    draw.rectangle([cx - 6, cy - 16, cx + 6, cy + 16], fill=WHITE)
    draw.rectangle([cx - 16, cy - 6, cx + 16, cy + 6], fill=WHITE)


def icon_cyclone(draw, cx, cy, color):
    """A cyclone spiral: an Archimedean spiral with a calm eye."""
    pts = []
    for i in range(0, 181):
        t = i / 180.0 * 4.2 * math.pi
        r = 3 + 8.0 * t / math.pi
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    draw.line(pts, fill=color, width=6, joint="curve")
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255),
                 outline=color, width=3)


# ---------------------------------------------------------------- layout

PANELS = [
    dict(
        headline="IRAN STRIKES KUWAIT, BAHRAIN",
        sub="Strikes US bases after US hit Qeshm island",
        tint=(253, 236, 234), icon=icon_missile, color=(192, 57, 43),
    ),
    dict(
        headline="XI, PUTIN MEET IN SHENZHEN",
        sub="Pledge against trade curbs before Trump talks",
        tint=(232, 240, 250), icon=icon_flags, color=(46, 109, 180),
    ),
    dict(
        headline="PELTOLA WINS ALASKA",
        sub="Democrats take projected 56-44 majority",
        tint=(241, 232, 247), icon=icon_ballot, color=(125, 60, 152),
    ),
    dict(
        headline="KERCH BRIDGE HIT AGAIN",
        sub="Part of road span falls into the strait",
        tint=(230, 240, 245), icon=icon_bridge, color=(44, 110, 143),
    ),
    dict(
        headline="EBOLA SURGE IN CONGO",
        sub="Cases top 11,000; 5,400 dead, UN says",
        tint=(251, 236, 234), icon=icon_virus, color=(169, 50, 38),
    ),
    dict(
        headline="CYCLONE XAVIER HITS",
        sub="Category 5 storm hits northern atolls",
        tint=(253, 240, 227), icon=icon_cyclone, color=(202, 111, 30),
    ),
]


def main():
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)

    # ---- header
    draw.rectangle([0, 0, W, 150], fill=NAVY)
    f_title = font(BLACK, 46)
    draw.text((W // 2, 24), "WORLD NEWS", font=f_title, fill=GOLD, anchor="ma")
    f_date = font(BLACK, 64)
    draw.text((W // 2, 74), "18 NOVEMBER 2026", font=f_date, fill=WHITE, anchor="ma")
    draw.rectangle([0, 150, W, 156], fill=GOLD)

    # ---- grid: 2 columns x 3 rows
    margin, gap = 16, 16
    pw = (W - 2 * margin - gap) // 2
    ph = (H - 172 - 2 * margin - 2 * gap) // 3
    strip_w = 116

    for i, p in enumerate(PANELS):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = 172 + row * (ph + gap)

        draw.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=10, fill=PANEL_BG)
        # icon strip
        draw.rounded_rectangle([x0, y0, x0 + strip_w, y0 + ph], radius=10, fill=p["tint"])
        draw.rectangle([x0 + strip_w - 10, y0, x0 + strip_w, y0 + ph], fill=p["tint"])
        p["icon"](draw, x0 + strip_w // 2, y0 + ph // 2, p["color"])

        # text area
        tx = x0 + strip_w + 16
        tw = pw - strip_w - 32
        f_head = fit(draw, p["headline"], BOLD, 40, 26, tw, 2)
        head_lines = wrap(draw, p["headline"], f_head, tw)
        f_sub = fit(draw, p["sub"], REGULAR, 27, 19, tw, 3)
        sub_lines = wrap(draw, p["sub"], f_sub, tw)

        y = y0 + 26
        for line in head_lines:
            draw.text((tx, y), line, font=f_head, fill=HEADLINE)
            y += f_head.size + 4
        y += 8
        for line in sub_lines:
            draw.text((tx, y), line, font=f_sub, fill=SUBLINE)
            y += f_sub.size + 4

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
