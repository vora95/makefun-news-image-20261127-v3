#!/usr/bin/env python3
"""THE WORLD IN ONE DAY -- Friday 27 November 2026.

A one-page front page summing up the day's world news in one image.
Pure Pillow, no network, deterministic: two runs write identical bytes.
Writes /output/entry.png (1024 x 1024, under 1 MiB).

42 stories, 10 regions, 20 sources, 14 drawn scenes. Every story was
reported on Friday 27 November 2026 (event or first report).
"""
import hashlib
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (166, 25, 46)
NAVY = (31, 58, 95)
GREY = (90, 90, 86)
LGREY = (120, 116, 108)
GREEN = (30, 125, 50)
AMBER = (178, 106, 0)
PURPLE = (106, 74, 158)
SLATE = (90, 107, 124)
CREAM2 = (242, 236, 220)

TAG_COLORS = {
    "CONFIRMED": GREEN,
    "OFFICIAL": NAVY,
    "REPORTED": SLATE,
    "CLAIM": AMBER,
    "FORECAST": PURPLE,
}

_SERIF = "LiberationSerif-Regular.ttf"
_SERIF_B = "LiberationSerif-Bold.ttf"
_SERIF_I = "LiberationSerif-Italic.ttf"
_SANS = "LiberationSans-Regular.ttf"
_SANS_B = "LiberationSans-Bold.ttf"

_FONT_FILES = {
    "serif": _SERIF,
    "serif-bold": _SERIF_B,
    "serif-italic": _SERIF_I,
    "sans": _SANS,
    "sans-bold": _SANS_B,
}

_SYSTEM_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/noto",
]

_SYSTEM_NAMES = {
    "serif": ["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf",
              "NotoSerif-Regular.ttf"],
    "serif-bold": ["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf",
                   "NotoSerif-Bold.ttf"],
    "serif-italic": ["LiberationSerif-Italic.ttf", "DejaVuSerif-Italic.ttf",
                     "NotoSerif-Italic.ttf"],
    "sans": ["LiberationSans-Regular.ttf", "DejaVuSans.ttf",
             "NotoSans-Regular.ttf"],
    "sans-bold": ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf",
                  "NotoSans-Bold.ttf"],
}


def font(kind, size):
    """Load a font: bundled copy first, then system copies, then default."""
    here = os.path.dirname(os.path.abspath(__file__))
    bundled = os.path.join(here, "fonts", _FONT_FILES[kind])
    for path in [bundled]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    for d in _SYSTEM_DIRS:
        for name in _SYSTEM_NAMES[kind]:
            try:
                return ImageFont.truetype(os.path.join(d, name), size)
            except Exception:
                pass
    return ImageFont.load_default()


def wrap(text, fnt, max_w):
    """Greedy word wrap; hard-splits a word that alone exceeds max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
            continue
        if cur:
            lines.append(cur)
        while fnt.getlength(word) > max_w and len(word) > 1:
            n = 1
            while n < len(word) and fnt.getlength(word[: n + 1]) <= max_w:
                n += 1
            lines.append(word[:n])
            word = word[n:]
        cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(d, x0, x1, y, width=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def tag(d, x, y, text):
    """Status pill; returns width used."""
    f = font("sans-bold", 9)
    tw = f.getlength(text)
    d.rounded_rectangle([x, y, x + tw + 10, y + 13], radius=6,
                        fill=TAG_COLORS[text])
    d.text((x + 5, y + 1), text, font=f, fill=(255, 255, 255))
    return tw + 10


def chip(d, x, y, text):
    """Small red chip inside a scene; returns width used."""
    f = font("sans-bold", 10)
    tw = f.getlength(text)
    d.rectangle([x, y, x + tw + 10, y + 16], fill=RED)
    d.text((x + 5, y + 2), text, font=f, fill=(255, 255, 255))
    return tw + 10


# ---------------------------------------------------------------- scenes
# Each scene draws inside (x, y, w, h). All shapes are plain Pillow calls.
# Coordinates are scaled to the box actually given (lead row is wide).

def scene_kuwait(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 35, 58))
    for sx in range(10, w - 10, 26):
        d.ellipse([x + sx, y + 6, x + sx + 2, y + 8], fill=(255, 255, 255))
        d.ellipse([x + sx + 12, y + 14, x + sx + 14, y + 16],
                  fill=(200, 200, 200))
    # city skyline silhouette along the bottom
    for bx, bw, bh in [(70, 34, 14), (110, 24, 18), (140, 40, 11),
                       (186, 28, 16), (220, 36, 12), (262, 26, 17)]:
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + bw, y + h - 12],
                    fill=(12, 18, 30))
        for wx in range(x + bx + 4, x + bx + bw - 3, 9):
            d.rectangle([wx, y + h - 12 - bh + 4, wx + 3,
                         y + h - 12 - bh + 8], fill=(255, 214, 120))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(194, 164, 110))
    # radar dish 1
    d.arc([x + 20, y + 12, x + 60, y + 44], 180, 360, fill=(230, 230, 230),
          width=3)
    d.line([(x + 40, y + 28), (x + 40, y + h - 12)], fill=(230, 230, 230),
           width=3)
    d.line([(x + 40, y + 22), (x + 58, y + 10)], fill=(230, 230, 230), width=2)
    # radar dish 2 (smaller)
    d.arc([x + 130, y + 20, x + 160, y + 44], 180, 360,
          fill=(200, 200, 200), width=2)
    d.line([(x + 145, y + 32), (x + 145, y + h - 12)], fill=(200, 200, 200),
           width=2)
    # drones with red lights
    for dx, dy in [(200, 8), (238, 16), (258, 8)]:
        d.ellipse([x + dx, y + dy, x + dx + 9, y + dy + 4], fill=(40, 40, 40))
        d.ellipse([x + dx + 3, y + dy + 1, x + dx + 5, y + dy + 3],
                  fill=(255, 60, 60))
    # second, smaller burst mid-sky
    cx2, cy2 = x + 172, y + 18
    pts2 = []
    for i in range(10):
        ang = i * 36
        r = 8 if i % 2 == 0 else 3
        pts2.append((cx2 + r * math.cos(math.radians(ang)),
                     cy2 + r * math.sin(math.radians(ang))))
    d.polygon(pts2, fill=(255, 176, 0))
    # main explosion burst
    cx, cy = x + w - 34, y + 26
    pts = []
    for i in range(12):
        ang = i * 30
        r = 14 if i % 2 == 0 else 6
        pts.append((cx + r * math.cos(math.radians(ang)),
                    cy + r * math.sin(math.radians(ang))))
    d.polygon(pts, fill=(255, 176, 0))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 230, 120))
    chip(d, x + 6, y + 4, "2 KILLED")


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 30, 48))
    widths = [30, 22, 34, 24, 32, 22, 34, 26, 30, 24]
    fracs = [0.62, 0.85, 0.52, 0.75, 0.58, 0.9, 0.62, 0.8, 0.66, 0.72]
    bx = 4
    for bw, fr in zip(widths, fracs):
        bh = int((h - 6) * fr)
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(12, 14, 24))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(x + bx + 4, x + bx + bw - 3, 9):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
        bx += bw + 4
    # smoke columns
    for sx in [40, 140, 220]:
        d.ellipse([x + sx, y + 4, x + sx + 24, y + 20], fill=(120, 120, 130))
        d.ellipse([x + sx + 8, y + 14, x + sx + 32, y + 32],
                  fill=(90, 90, 100))
    d.ellipse([x + w - 48, y + 6, x + w - 24, y + 30], fill=(255, 120, 40))
    chip(d, x + w - 66, y + h - 20, "10 KILLED")


def scene_jazan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 44, 40))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(30, 24, 22))
    fracs = [0.55, 0.42, 0.68, 0.48, 0.62, 0.38, 0.58, 0.52, 0.44, 0.64]
    tx = 8
    for i, fr in enumerate(fracs):
        tw = 16 if i % 2 == 0 else 11
        th = int((h - 18) * fr)
        d.rectangle([x + tx, y + h - 14 - th, x + tx + tw, y + h - 14],
                    fill=(70, 66, 62))
        d.rectangle([x + tx + 2, y + h - 14 - th - 5, x + tx + tw - 2,
                     y + h - 14 - th], fill=(70, 66, 62))
        tx += tw + 14
    d.line([(x + 8, y + h - 22), (x + w - 8, y + h - 22)], fill=(70, 66, 62),
           width=3)
    # orange glow behind the flames
    d.ellipse([x + 180, y + 4, x + 228, y + 34], fill=(255, 120, 40))
    d.ellipse([x + 80, y + 10, x + 116, y + 32], fill=(255, 120, 40))
    # flames (bigger)
    d.polygon([(x + 192, y + 32), (x + 204, y + 4), (x + 216, y + 32)],
              fill=(255, 140, 0))
    d.polygon([(x + 196, y + 32), (x + 204, y + 14), (x + 212, y + 32)],
              fill=(255, 220, 80))
    d.polygon([(x + 88, y + 32), (x + 97, y + 12), (x + 106, y + 32)],
              fill=(255, 140, 0))
    # black smoke
    d.ellipse([x + 24, y + 4, x + 56, y + 18], fill=(25, 25, 25))
    d.ellipse([x + 250, y + 6, x + 282, y + 20], fill=(25, 25, 25))
    chip(d, x + w - 70, y + h - 18, "BRENT $96")


def scene_bangkok(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 214, 232))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 110, 96))
    fracs = [0.65, 0.85, 0.55, 0.75, 0.6]
    bx = 8
    for fr in fracs:
        bw = 30 if bx < 100 else 26
        bh = int((h - 12) * fr)
        d.rectangle([x + bx, y + h - 12 - bh, x + bx + bw, y + h - 12],
                    fill=(96, 92, 88))
        bx += bw + 8
    # fireball
    d.ellipse([x + w // 2 - 16, y + 4, x + w // 2 + 16, y + 32],
              fill=(255, 120, 0))
    d.ellipse([x + w // 2 - 9, y + 10, x + w // 2 + 9, y + 26],
              fill=(255, 210, 60))
    # smoke plume
    d.ellipse([x + 10, y + 2, x + 42, y + 16], fill=(40, 40, 40))
    d.ellipse([x + 26, y + 8, x + 58, y + 22], fill=(40, 40, 40))
    chip(d, x + 6, y + 4, "9 HURT")


def scene_blackfriday(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 210))
    shops = [(8, (166, 25, 46)), (66, (31, 58, 95)), (124, (0, 122, 90))]
    for sx, col in shops:
        d.rectangle([x + sx, y + 16, x + sx + 52, y + h - 4],
                    fill=(255, 255, 255), outline=col, width=2)
        for i in range(4):
            d.polygon([(x + sx + i * 13, y + 16), (x + sx + i * 13 + 13, y + 16),
                       (x + sx + i * 13 + 7, y + 24), (x + sx + i * 13, y + 24)],
                      fill=col if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x + sx + 18, y + 30, x + sx + 34, y + h - 4], fill=col)
    # shopping bags
    for bx, col in [(150, (255, 176, 0)), (168, (166, 25, 46))]:
        d.rectangle([x + bx, y + h - 20, x + bx + 14, y + h - 6], fill=col)
        d.arc([x + bx + 3, y + h - 26, x + bx + 11, y + h - 16], 180, 360,
              fill=INK, width=2)
    chip(d, x + 6, y + 4, "$12.9B")


def scene_nz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    # ballot box
    d.rectangle([x + 14, y + 14, x + 74, y + h - 8], fill=NAVY)
    d.rectangle([x + 26, y + 8, x + 62, y + 16], fill=(255, 255, 255),
                outline=NAVY, width=2)
    d.line([(x + 34, y + 12), (x + 54, y + 12)], fill=INK, width=3)
    d.text((x + 22, y + 22), "VOTE", font=font("sans-bold", 11),
           fill=(255, 255, 255))
    # seat bar 67 / 131
    d.rectangle([x + 88, y + 16, x + w - 10, y + 26], fill=(210, 210, 205))
    d.rectangle([x + 88, y + 16, x + 88 + int((w - 98) * 67 / 131), y + 26],
                fill=RED)
    d.text((x + 88, y + 30), "67 / 131", font=font("sans-bold", 13), fill=INK)
    d.text((x + 152, y + 33), "SEATS", font=font("sans-bold", 8), fill=GREY)


def scene_uk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 8, y + 4), "77,000", font=font("serif-bold", 20), fill=RED)
    d.text((x + 8, y + 28), "LOWEST SINCE '97", font=font("sans-bold", 9),
           fill=INK)
    pts = [(x + 100, y + 12), (x + 118, y + 16), (x + 136, y + 14),
           (x + 154, y + 24), (x + 172, y + 28), (x + 184, y + 34)]
    d.line(pts, fill=NAVY, width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=NAVY)
    d.polygon([(x + 186, y + 36), (x + 174, y + 30), (x + 182, y + 24)],
              fill=NAVY)


def scene_storm(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 78, 92))
    for cx, cw in [(4, 62), (64, 70), (128, 58)]:
        d.ellipse([x + cx, y + 2, x + cx + cw, y + 18], fill=(52, 58, 70))
    # lightning
    d.polygon([(x + 122, y + 14), (x + 112, y + 28), (x + 120, y + 28),
               (x + 110, y + 38), (x + 128, y + 24), (x + 120, y + 24)],
              fill=(255, 220, 60))
    # rain
    for rx in range(12, 92, 14):
        d.line([(x + rx, y + 26), (x + rx - 5, y + 38)], fill=(180, 200, 220),
               width=2)
    # toppled tree
    d.line([(x + 16, y + h - 4), (x + 64, y + h - 16)], fill=(90, 60, 30),
           width=4)
    d.ellipse([x + 56, y + h - 22, x + 84, y + h - 6], fill=(40, 110, 60))
    # deflated balloon
    d.ellipse([x + w - 44, y + h - 20, x + w - 10, y + h - 6],
              fill=(200, 200, 200))
    chip(d, x + 6, y + 4, "900,000 OUT")


def scene_ibiza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(56, 130, 190))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(30, 90, 150))
    # capsized hull, tilted (bigger)
    d.polygon([(x + 20, y + 12), (x + 132, y + 8), (x + 140, y + 22),
               (x + 28, y + 28)], fill=(150, 60, 50))
    d.rectangle([x + 52, y + 10, x + 116, y + 16], fill=(120, 40, 35))
    # waves
    for wx0, wy0 in [(16, 30), (60, 32), (104, 30)]:
        d.arc([x + wx0, y + wy0, x + wx0 + 32, y + wy0 + 8], 180, 360,
              fill=(255, 255, 255), width=2)
    # foam
    for fx, fy in [(36, 28), (76, 30), (112, 28), (136, 30)]:
        d.ellipse([x + fx, y + fy, x + fx + 12, y + fy + 5],
                  fill=(255, 255, 255))
    chip(d, x + 6, y + 4, "7,000T")


def scene_gdp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + 2), "3.4% \u2192 4.3%", font=font("sans-bold", 11),
           fill=INK)
    d.text((x + w - 52, y + 2), "'FAKE?'", font=font("serif-bold", 14),
           fill=RED)
    d.rectangle([x + 14, y + h - 14, x + 34, y + h - 3],
                fill=(150, 150, 145))
    d.rectangle([x + 44, y + h - 24, x + 64, y + h - 3], fill=RED)
    d.text((x + 18, y + h - 11), "Q2", font=font("sans-bold", 8),
           fill=(255, 255, 255))
    d.text((x + 48, y + h - 12), "Q3", font=font("sans-bold", 8),
           fill=(255, 255, 255))
    d.line([(x + 72, y + h - 10), (x + 96, y + h - 22)], fill=NAVY, width=3)
    d.polygon([(x + 96, y + h - 22), (x + 89, y + h - 14),
               (x + 85, y + h - 21)], fill=NAVY)


def scene_depardieu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 214))
    # courthouse pediment + columns
    d.polygon([(x + 10, y + 12), (x + w // 2, y + 2), (x + w - 10, y + 12)],
              fill=(120, 110, 95))
    for cx in [22, 62, 102]:
        d.rectangle([x + cx, y + 14, x + cx + 8, y + h - 12],
                    fill=(150, 140, 120))
    d.rectangle([x + 8, y + h - 14, x + w - 8, y + h - 8],
                fill=(120, 110, 95))
    # scales of justice
    d.line([(x + w - 28, y + 16), (x + w - 28, y + 32)], fill=INK, width=2)
    d.line([(x + w - 42, y + 20), (x + w - 14, y + 20)], fill=INK, width=2)
    d.arc([x + w - 44, y + 20, x + w - 34, y + 30], 0, 180, fill=INK, width=2)
    d.arc([x + w - 22, y + 20, x + w - 12, y + 30], 0, 180, fill=INK, width=2)


def scene_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(188, 214, 232))
    d.text((x + 6, y + 8), "+20%", font=font("serif-bold", 17), fill=RED)
    cols = [(166, 25, 46), (255, 176, 0), (0, 122, 90), (31, 58, 95)]
    for i, col in enumerate(cols):
        cx = x + 72 + (i % 2) * 40
        cy = y + 6 + (i // 2) * 12
        d.rectangle([cx, cy, cx + 36, cy + 10], fill=col)
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(40, 90, 140))
    # hull
    d.polygon([(x + 8, y + 30), (x + w - 8, y + 30), (x + w - 22, y + h - 2),
               (x + 22, y + h - 2)], fill=(40, 40, 40))


def scene_mecca(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # dome + minarets
    d.pieslice([x + w // 2 - 16, y + 8, x + w // 2 + 16, y + 28], 180, 360,
               fill=(212, 175, 55))
    d.rectangle([x + w // 2 - 20, y + 20, x + w // 2 + 20, y + h - 4],
                fill=(230, 220, 195))
    for mx in [x + 12, x + w - 16]:
        d.rectangle([mx, y + 6, mx + 4, y + h - 4], fill=(200, 190, 160))
        d.polygon([(mx - 2, y + 6), (mx + 2, y), (mx + 6, y + 6)],
                  fill=(212, 175, 55))
    # three banners
    for i, col in enumerate([(0, 122, 90), (0, 102, 51), (200, 30, 40)]):
        d.rectangle([x + 8 + i * 12, y + h - 12, x + 8 + i * 12 + 8, y + h - 4],
                    fill=col)


def scene_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 220))
    sq = 8
    ox, oy = x + 6, y + 3
    for r in range(4):
        for c in range(4):
            fill = (255, 255, 255) if (r + c) % 2 == 0 else (40, 40, 40)
            d.rectangle([ox + c * sq, oy + r * sq, ox + (c + 1) * sq,
                         oy + (r + 1) * sq], fill=fill)
    # pieces: white king, black queen
    d.ellipse([ox + 1, oy + 1, ox + 15, oy + 15], fill=(255, 255, 255),
              outline=INK, width=1)
    d.text((ox + 4, oy + 2), "K", font=font("serif-bold", 10), fill=INK)
    d.ellipse([ox + 17, oy + 17, ox + 31, oy + 31], fill=(20, 20, 20),
              outline=INK, width=1)
    d.text((ox + 20, oy + 18), "Q", font=font("serif-bold", 10),
           fill=(255, 255, 255))
    d.text((x + 46, y + 4), "1\u00bd-1\u00bd", font=font("sans-bold", 11),
           fill=INK)
    d.text((x + 46, y + 18), "60 MOVES", font=font("sans-bold", 8), fill=GREY)
    d.text((x + 46, y + 28), "REST DAY", font=font("sans-bold", 8), fill=RED)


SCENES = {
    "kuwait": scene_kuwait,
    "gaza": scene_gaza,
    "jazan": scene_jazan,
    "bangkok": scene_bangkok,
    "blackfriday": scene_blackfriday,
    "nz": scene_nz,
    "uk": scene_uk,
    "storm": scene_storm,
    "ibiza": scene_ibiza,
    "gdp": scene_gdp,
    "depardieu": scene_depardieu,
    "tariffs": scene_tariffs,
    "mecca": scene_mecca,
    "chess": scene_chess,
}

# ---------------------------------------------------------------- data

LEADS = [
    dict(scene="kuwait", kicker="1  \u2022  KUWAIT  \u2022  MIDDLE EAST",
         head="Two Italians killed in Iranian drone strike on Kuwait",
         body="Drones hit an air-defence station, killing two Rheinmetall "
              "Italia technicians; Iran denies any role.",
         why="First deadly strike on a Gulf ally's soil in this crisis -- "
             "and the victims are Europeans.",
         tag="CONFIRMED", source="Reuters"),
    dict(scene="gaza", kicker="2  \u2022  GAZA  \u2022  WAR",
         head="Israel kills 10 in Gaza; Hamas weighs its reply",
         body="Strikes kill Hamas official Khaled Abu Nada and his wife in "
              "Deir al-Balah, on a third straight night of attacks.",
         why="Hamas says it may not withstand more strikes -- the year-old "
             "truce is fraying in public.",
         tag="REPORTED", source="Reuters"),
    dict(scene="jazan", kicker="3  \u2022  SAUDI ARABIA  \u2022  JAZAN",
         head="Houthi strike hits Jazan refinery; one worker killed",
         body="A projectile hits Aramco's Jazan refinery, killing a "
              "Nepalese worker and halting some operations.",
         why="The first confirmed refinery hit of the five-day exchange; "
             "Brent tops $96.",
         tag="CONFIRMED", source="Reuters"),
]

ROW2 = [
    dict(scene="bangkok", kicker="4  \u2022  THAILAND  \u2022  BANGKOK",
         head="Blast at Bangkok refinery injures nine",
         body="Fire at Bangchak's Phra Khanong plant; three critical, all "
              "units shut.",
         tag="REPORTED", source="AP"),
    dict(scene="blackfriday", kicker="5  \u2022  USA  \u2022  BLACK FRIDAY",
         head="Black Friday opens: $12.9bn day ahead",
         body="Adobe forecasts a record $12.9bn online; 126m Americans plan "
              "to shop.",
         tag="FORECAST", source="Adobe"),
    dict(scene="nz", kicker="6  \u2022  NEW ZEALAND  \u2022  POLITICS",
         head="NZ final count lands today",
         body="400,000 special votes decide a 67-seat coalition edge; "
              "result due today.",
         tag="OFFICIAL", source="NZ Herald"),
    dict(scene="uk", kicker="7  \u2022  UNITED KINGDOM  \u2022  MIGRATION",
         head="UK net migration lowest since 1997",
         body="ONS puts net migration at 77,000, down from 204,000; the "
              "lowest in 29 years.",
         tag="OFFICIAL", source="ONS"),
    dict(scene="storm", kicker="8  \u2022  USA  \u2022  STORM",
         head="Thanksgiving storm cuts power to 900,000",
         body="A nor'easter darkens the holiday; the 100th Macy's parade "
              "moves to Saturday.",
         tag="REPORTED", source="WSJ"),
]

ROW3 = [
    dict(scene="ibiza", kicker="9  \u2022  SPAIN  \u2022  IBIZA",
         head="Tanker capsizes off Ibiza; one dead",
         body="Med Emre, carrying up to 7,000t of diesel, keels over; 17 "
              "rescued.",
         tag="REPORTED", source="Reuters"),
    dict(scene="gdp", kicker="10  \u2022  USA  \u2022  ECONOMY",
         head="Trump calls GDP figures 'fake', demands probe",
         body="Q3 growth revised up to 4.3% from 3.4%; Trump alleges an "
              "error.",
         tag="REPORTED", source="Reuters"),
    dict(scene="depardieu", kicker="11  \u2022  FRANCE  \u2022  COURTS",
         head="Depardieu to stand trial for alleged 2018 rape",
         body="A Paris court orders trial over the Charlotte Arnould case.",
         tag="OFFICIAL", source="Reuters"),
    dict(scene="tariffs", kicker="12  \u2022  CHINA  \u2022  TRADE",
         head="China vows response to new US tariffs",
         body="Beijing reserves the right to act as Washington proposes "
              "new duties.",
         tag="OFFICIAL", source="AFP"),
    dict(scene="mecca", kicker="13  \u2022  PAKISTAN  \u2022  ALLIANCE",
         head="Mecca alliance meets in Islamabad",
         body="Pakistan, Saudi Arabia and Turkey open talks on their "
              "defence pact.",
         tag="REPORTED", source="Reuters"),
    dict(scene="chess", kicker="14  \u2022  GENEVA  \u2022  CHESS",
         head="Gukesh, Sindarov draw again; rest day today",
         body="Game 3 ends in a 60-move draw, 1 1/2-1 1/2; Game 4 is "
              "Saturday.",
         tag="OFFICIAL", source="Chess.com"),
]

BRIEFS = [
    ("MUSK", "Every US child to get two SpaceX shares, worth ~$18bn",
     "Reuters"),
    ("SINNER", "Out of Australian Open 2027 after knee surgery", "AP"),
    ("N. KOREA", "Halts KN-23 missile shipments to Russia, Kyiv intel says",
     "Reuters"),
    ("AMAZON", "Workers strike in 20+ countries for Black Friday",
     "UNI Global"),
    ("KARACHI", "Building collapse kills 3, injures 14", "Dawn"),
    ("NFL", "Bears stun Lions 39-35 on last-second TD", "AP"),
    ("EU", "Leaders debate 1.6T budget; Ukraine aid on the table", "Reuters"),
    ("S. AFRICA", "Court kills Ramaphosa impeachment report", "Business Day"),
    ("INDIA", "Cabinet clears 11,000-crore equipment scheme", "Mint"),
    ("CRICKET", "India A face Sri Lanka A in Rising Stars semi", "TOI"),
    ("SNOOKER", "Pankaj Advani wins Crucible Cup", "TOI"),
    ("INDIA", "Tata Trusts challenge Chandrasekaran return", "Mint"),
    ("INDIA", "Top court seeks stronger food labels", "TOI"),
    ("S. KOREA", "Exam top scorer probed in AI cheat case", "Korea Herald"),
    ("CHINA", "Shuts golf courses in new clampdown", "SCMP"),
    ("NATO", "Intern spying suspect stays in jail", "Reuters"),
    ("USA", "Army declares Iowa blast a success", "AP"),
    ("INDIA", "China border 'generally stable', Beijing says", "Reuters"),
    ("NZ", "Half of Black Friday deals no cheaper, study finds",
     "Consumer NZ"),
    ("RUGBY", "Barrett to captain All Blacks for first time", "NZ Herald"),
    ("JAPAN", "School absences hit record 359,000", "Japan Times"),
    ("SPAIN", "Races to stop oil spill off Ibiza", "Reuters"),
    ("COLOMBIA", "Hostage recounts 17-hour siege", "AP"),
    ("HONG KONG", "Marks deadly fire anniversary", "SCMP"),
    ("GERMANY", "Arrests 2 Iraqis over synagogue plot", "dpa"),
    ("INDONESIA", "Hunt miners trapped in illegal gold mine", "AP"),
    ("ECB", "Hernandez de Cos to lead ECB", "Reuters"),
    ("SUDAN", "Khartoum spurns Addis bid", "Reuters"),
]

NUMBERS = [
    ("2", "Italians killed\nin Kuwait"),
    ("10", "killed\nin Gaza"),
    ("9", "hurt in\nBangkok blast"),
    ("77,000", "UK net migration,\n29-year low"),
    ("$12.9B", "Black Friday\nonline forecast"),
    ("126M", "Americans\nshopping today"),
    ("900,000", "without power\nin US storm"),
    ("400,000", "NZ special\nvotes"),
]

TIMELINE = [
    ("00:05", "This page goes to press"),
    ("01:00", "NZ final count lands"),
    ("05:00", "Amazon strikes, Germany"),
    ("11:00", "Black Friday opens, US"),
    ("13:00", "Mecca alliance opens"),
    ("14:00", "Chess rest day, Geneva"),
]

DATECHECK = [
    "Macy's parade postponement -- announced Wed 25 Nov (the storm that "
    "forced it is today's news).",
    "Houthi claim on Ras Tanura -- Wed 25 Nov; coalition says it was "
    "intercepted, no damage.",
    "US tariffs on 14 partners proposed -- Wed 25 Nov; China's reply is "
    "today's news.",
    "26/11 Mumbai attacks anniversary -- Thu 26 Nov tributes, not today's "
    "news.",
    "COP31 ends with no deal -- Sun 22 Nov.",
    "Indonesia factory fire, 24 dead -- 22 Nov.",
]

# (lon, lat) of the 12 pinned stories, in story-number order.
PINS = [
    (47, 29), (34, 31), (42, 17), (100, 14), (175, -41), (0, 51),
    (-77, 39), (2, 39), (2, 49), (6, 46), (73, 34), (77, 29),
]

# Small display offsets (px) so clustered pins do not overlap.
PIN_OFFSETS = {2: (-8, -8), 3: (0, 10), 11: (0, -9), 12: (7, 8)}

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 73), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-85, 30), (-90, 21), (-95, 18), (-100, 16), (-105, 20),
     (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 12), (-70, 12), (-62, 10), (-52, 5), (-50, 0),
     (-40, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-73, -53), (-73, -40), (-73, -25), (-78, -15), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 12), (44, 0), (40, -10), (35, -20), (32, -29),
     (25, -34), (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4),
     (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (20, 70),
     (12, 65), (5, 60), (-5, 58), (-10, 52), (-10, 43)],
    [(30, 70), (40, 68), (60, 69), (75, 73), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 45), (140, 40), (130, 35), (127, 33), (120, 30), (110, 20),
     (105, 10), (100, 8), (98, 15), (95, 20), (90, 22), (85, 20), (80, 15),
     (77, 8), (73, 20), (68, 25), (60, 25), (55, 26), (50, 29), (48, 30),
     (44, 30), (40, 36), (35, 36), (30, 36)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
     (142, -11), (137, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
]


# ---------------------------------------------------------------- build

def draw_lead_card(d, x, y, w, story):
    x, y, w = int(x), int(y), int(w)
    SCENES[story["scene"]](d, x, y, w, 52)
    y += 58
    d.text((x, y), story["kicker"], font=font("sans-bold", 9), fill=RED)
    y += 12
    head_f = font("serif-bold", 18)
    y = draw_lines(d, x, y, wrap(story["head"], head_f, w), head_f, INK, 20)
    y += 2
    body_f = font("sans", 10)
    y = draw_lines(d, x, y, wrap(story["body"], body_f, w), body_f, INK, 12)
    y += 3
    why_f = font("serif-italic", 10)
    why = "WHY IT MATTERS  " + story["why"]
    y = draw_lines(d, x, y, wrap(why, why_f, w), why_f, (90, 40, 40), 12)
    y += 4
    used = tag(d, x, y, story["tag"])
    src_f = font("sans", 9)
    d.text((x + used + 6, y + 1), story["source"], font=src_f, fill=GREY)
    return y + 14


def draw_scene_card(d, x, y, w, story, scene_h, head_size, body_size):
    x, y, w = int(x), int(y), int(w)
    SCENES[story["scene"]](d, x, y, w, scene_h)
    y += scene_h + 5
    d.text((x, y), story["kicker"], font=font("sans-bold", 8), fill=RED)
    y += 11
    head_f = font("serif-bold", head_size)
    y = draw_lines(d, x, y, wrap(story["head"], head_f, w), head_f, INK,
                   head_size + 2)
    y += 1
    body_f = font("sans", body_size)
    y = draw_lines(d, x, y, wrap(story["body"], body_f, w), body_f, INK,
                   body_size + 2)
    y += 3
    used = tag(d, x, y, story["tag"])
    src_f = font("sans", 8)
    d.text((x + used + 5, y + 1), story["source"], font=src_f, fill=GREY)
    return y + 14


def draw_map(d, x, y, w, h):
    x, y, w, h = int(x), int(y), int(w), int(h)
    d.text((x, y), "WHERE IT HAPPENED", font=font("sans-bold", 10), fill=INK)
    d.text((x + w - 130, y), "Pins match story numbers.",
           font=font("sans", 9), fill=GREY)
    y += 14
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238),
                outline=(150, 160, 170))

    def proj(lon, lat):
        px = x + (lon + 170) / 360.0 * w
        py = y + (75 - lat) / 130.0 * h
        return (px, py)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(196, 186, 164),
                  outline=(150, 140, 120))
    for i, (lon, lat) in enumerate(PINS, start=1):
        px, py = proj(lon, lat)
        ox, oy = PIN_OFFSETS.get(i, (0, 0))
        px, py = px + ox, py + oy
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        tf = font("sans-bold", 8)
        tw = tf.getlength(str(i))
        d.text((px - tw / 2, py - 5), str(i), font=tf, fill=(255, 255, 255))
    return y + h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)
    d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=1)

    x0, x1 = 16, W - 16
    y = 14

    # kicker
    d.text((x0, y), "THE WORLD IN ONE DAY", font=font("sans-bold", 14),
           fill=INK)
    right = "42 STORIES  \u2022  10 REGIONS  \u2022  20 SOURCES"
    rf = font("sans-bold", 11)
    d.text((x1 - rf.getlength(right), y + 2), right, font=rf, fill=RED)
    y += 22
    hline(d, x0, x1, y, width=2)
    y += 5

    # masthead
    mast = "FRIDAY 27 NOVEMBER 2026"
    mf = font("serif-bold", 54)
    d.text(((W - mf.getlength(mast)) / 2, y), mast, font=mf, fill=INK)
    y += 60
    stand = ("Two Italians killed in Kuwait, ten dead in Gaza, a refinery "
             "burning in Jazan -- Black Friday opens as a storm darkens "
             "Thanksgiving.")
    sf = font("serif-italic", 14)
    slines = wrap(stand, sf, x1 - x0)
    for line in slines:
        d.text(((W - sf.getlength(line)) / 2, y), line, font=sf, fill=INK)
        y += 18
    y += 2
    hline(d, x0, x1, y, width=2)
    y += 3
    hline(d, x0, x1, y, width=1)
    y += 5

    # UTC timeline
    d.rectangle([x0, y, x1, y + 26], fill=NAVY)
    tf = font("sans-bold", 10)
    d.text((x0 + 8, y + 7), "THE DAY IN UTC", font=tf, fill=(255, 255, 255))
    tx = x0 + 118
    cell = (x1 - tx - 6) / len(TIMELINE)
    for t, label in TIMELINE:
        d.text((tx, y + 7), t, font=font("sans-bold", 10),
               fill=(255, 214, 120))
        tw = font("sans-bold", 10).getlength(t)
        lab = label
        lf = font("sans", 9)
        while lf.getlength(lab) > cell - tw - 14 and len(lab) > 4:
            lab = lab[:-1]
        d.text((tx + tw + 4, y + 8), lab, font=lf, fill=(255, 255, 255))
        tx += cell
    y += 32

    # numbers strip
    cell_w = (x1 - x0) / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        cx = x0 + i * cell_w
        nf = font("serif-bold", 22)
        d.text((cx + (cell_w - nf.getlength(num)) / 2, y), num, font=nf,
               fill=RED)
        lf = font("sans", 8)
        ly = y + 26
        for line in label.split("\n"):
            d.text((cx + (cell_w - lf.getlength(line)) / 2, ly), line,
                   font=lf, fill=INK)
            ly += 10
        if i:
            d.line([(cx, y + 2), (cx, y + 44)], fill=(200, 194, 180), width=1)
    y += 48
    hline(d, x0, x1, y, width=1)
    y += 4

    # lead row: 3 cards
    col_w = (x1 - x0 - 20) / 3
    for i, story in enumerate(LEADS):
        draw_lead_card(d, x0 + i * (col_w + 10), y, col_w, story)
    y += 184
    hline(d, x0, x1, y, width=1)
    y += 4

    # row 2: 5 cards
    col_w = (x1 - x0 - 32) / 5
    for i, story in enumerate(ROW2):
        draw_scene_card(d, x0 + i * (col_w + 8), y, col_w, story, 44, 13, 9)
    y += 132
    hline(d, x0, x1, y, width=1)
    y += 4

    # row 3: 6 cards
    col_w = (x1 - x0 - 40) / 6
    for i, story in enumerate(ROW3):
        draw_scene_card(d, x0 + i * (col_w + 8), y, col_w, story, 38, 12, 9)
    y += 140
    hline(d, x0, x1, y, width=2)
    y += 4

    # briefs header
    d.text((x0, y), "ALSO ON FRIDAY 27 NOVEMBER  --  28 MORE STORIES",
           font=font("sans-bold", 11), fill=INK)
    y += 16
    hline(d, x0, x1, y, width=1)
    y += 4

    # briefs: 2 columns x 14 rows
    col_w = (x1 - x0 - 16) / 2
    bf = font("sans", 10)
    bfb = font("sans-bold", 10)
    for row in range(14):
        for col in range(2):
            idx = 15 + row + col * 14
            lead, text, src = BRIEFS[idx - 15]
            bx = x0 + col * (col_w + 16)
            by = y + row * 12
            num = str(idx)
            d.text((bx, by), num, font=bfb, fill=RED)
            nx = bx + bfb.getlength(num) + 5
            head_txt = lead + " -- "
            d.text((nx, by), head_txt, font=bfb, fill=INK)
            tx = nx + bfb.getlength(head_txt)
            d.text((tx, by), text, font=bf, fill=INK)
            sx = tx + bf.getlength(text) + 4
            d.text((sx, by), "-- " + src, font=bf, fill=GREY)
    y += 14 * 12 + 4
    hline(d, x0, x1, y, width=1)
    y += 4

    # bottom row: map + date check
    map_w = 500
    dc_x = x0 + map_w + 10
    dc_w = x1 - dc_x
    map_end = draw_map(d, x0, y, map_w, 72)
    d.rectangle([dc_x, y, x1, y + 88], outline=RED, width=2)
    d.text((dc_x + 8, y + 4), "DATE CHECK -- WHAT WE LEFT OUT",
           font=font("sans-bold", 10), fill=RED)
    dy = y + 20
    df = font("sans", 9)
    for line in DATECHECK:
        for ln in wrap(line, df, dc_w - 16):
            d.text((dc_x + 8, dy), ln, font=df, fill=INK)
            dy += 11
    y = max(map_end, y + 88) + 4

    # footer
    hline(d, x0, x1, y, width=1)
    y += 4
    ff = font("sans", 8)
    foot1 = ("Sources: Reuters, CNN, AP, BBC, WSJ, ONS, NZ Herald, Times of "
             "Israel, Chess.com, UNI Global, Adobe, NRF, Dawn, Mint, TOI. "
             "Every story was reported on Friday 27 November 2026.")
    foot2 = ("Tags: CONFIRMED = 2+ outlets  \u2022  OFFICIAL = on the record  "
             "\u2022  REPORTED = one outlet  \u2022  CLAIM = one side says  "
             "\u2022  FORECAST = due today.  Pictures and map: original, "
             "drawn in code. -- Drawn 27 Nov 2026.")
    for line in (foot1, foot2):
        d.text(((W - ff.getlength(line)) / 2, y), line, font=ff, fill=GREY)
        y += 10

    assert y <= H - 8, "layout overflow: y=%d" % y
    os.makedirs("/output", exist_ok=True)
    out = "/output/entry.png"
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print("wrote %s %d bytes sha256=%s" % (out, len(data),
                                           hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
