#!/usr/bin/env python3
"""Mr.MONEY news card: python3 make_card.py "<headline>" "<category>" "<date>" out.png
category one of: اقتصاد | بزنس | منوعات | سياسة
4:5 (1080x1350) in the Mr.MONEY identity: grid paper, navy torn panel, kraft tape,
red MR.MONEY stamp, ink badge with orange keyword, gold numbers.
Needs fonts/Cairo.ttf (variable) next to this script and Pillow with raqm."""
import os, random, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
M = 60  # safe margin
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Cairo.ttf")

PAPER = "#D9D6CE"
GRID = "#CBC7BD"
NAVY = "#2F4A6B"
KRAFT = "#C99F5E"
CREAM = "#ECE4D0"
INK = "#2B2A27"
OFFWHITE = "#F3EEE3"
RED = "#B8322A"
GOLD = "#F2B13C"
ORANGE = "#E66A21"
LIGHT = "#F7F2E6"

AR = dict(direction="rtl", language="ar")
NUM = re.compile(r"[0-9٠-٩]")


def font(size, weight="Black"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def width(d, t, f):
    b = d.textbbox((0, 0), t, font=f, **AR)
    return b[2] - b[0]


def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        test = (cur + " " + w).strip()
        if width(d, test, f) <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_line_rtl(d, x_right, y_mid, line, f, color, num_color):
    """Draw words right-to-left so words with digits can be coloured gold."""
    sp = width(d, "ا ا", f) - 2 * width(d, "ا", f)
    x = x_right
    for w in line.split():
        ww = width(d, w, f)
        c = num_color if NUM.search(w) else color
        d.text((x, y_mid), w, font=f, fill=c, anchor="rm", **AR)
        x -= ww + sp


def torn_polygon(x0, y0, x1, y1, rnd, step=18, amp=9):
    pts = []
    x = x0
    while x < x1:
        pts.append((x, y0 + rnd.uniform(-amp, amp)))
        x += step
    pts.append((x1, y0))
    y = y0
    while y < y1:
        pts.append((x1 + rnd.uniform(-amp / 2, amp / 2), y))
        y += step * 2
    x = x1
    while x > x0:
        pts.append((x, y1 + rnd.uniform(-amp, amp)))
        x -= step
    pts.append((x0, y1))
    y = y1
    while y > y0:
        pts.append((x0 + rnd.uniform(-amp / 2, amp / 2), y))
        y -= step * 2
    return pts


def tape(img, cx, cy, w, h, angle):
    t = Image.new("RGBA", (w, h), KRAFT + "E6")
    td = ImageDraw.Draw(t)
    for i in range(0, w, 7):  # torn ends
        td.rectangle((i, 0, i + 3, 3), fill=(0, 0, 0, 0))
        td.rectangle((i + 3, h - 3, i + 6, h), fill=(0, 0, 0, 0))
    t = t.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))


def shadow(img, box, radius=0, offset=(8, 10), blur=10, alpha=70):
    s = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    x0, y0, x1, y1 = box
    sd.rounded_rectangle((x0 + offset[0], y0 + offset[1], x1 + offset[0], y1 + offset[1]),
                         radius=radius, fill=(0, 0, 0, alpha))
    img.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))


def stamp(img, label):
    sw, sh = 250, 110
    s = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    sd = ImageDraw.Draw(s)
    sd.rounded_rectangle((0, 0, sw - 1, sh - 1), radius=6, fill=RED)
    sd.rounded_rectangle((7, 7, sw - 8, sh - 8), radius=4, outline=OFFWHITE, width=3)
    sd.text((sw / 2, 40), "MR.MONEY", font=font(40), fill=OFFWHITE, anchor="mm")
    sd.line((40, 66, sw - 40, 66), fill=OFFWHITE, width=3)
    sd.text((sw / 2, 86), label, font=font(26, "ExtraBold"), fill=OFFWHITE, anchor="mm", **AR)
    s = s.rotate(-2, expand=True, resample=Image.BICUBIC)
    # stamp sits top-LEFT on the card (Arabic reading starts right with the badge)
    img.alpha_composite(s, (M - 4, M - 4))


def main(headline, category, date, out):
    rnd = random.Random(headline)
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # grid paper
    for x in range(0, W, 36):
        d.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H, 36):
        d.line((0, y, W, y), fill=GRID, width=1)

    # MR.MONEY stamp (top-left)
    stamp(img, "أخبار اليوم")

    # series badge (top-right): ink pill, "ربع" + orange category
    bf = font(44)
    word1, word2 = "ربع", category
    w1, w2 = width(d, word1, bf), width(d, word2, bf)
    gap, pad = 16, 28
    bw = w1 + w2 + gap + 2 * pad
    bx1, by0 = W - M, M + 8
    bx0, by1 = bx1 - bw, by0 + 84
    d.rounded_rectangle((bx0, by0, bx1, by1), radius=6, fill=INK)
    d.text((bx1 - pad, (by0 + by1) / 2), word1, font=bf, fill=OFFWHITE, anchor="rm", **AR)
    d.text((bx1 - pad - w1 - gap, (by0 + by1) / 2), word2, font=bf, fill=ORANGE, anchor="rm", **AR)

    # date on a cream paper label with kraft tape
    df = font(34, "ExtraBold")
    dw = width(d, date, df) + 56
    lx1, ly0 = W - M - 10, 250
    lx0, ly1 = lx1 - dw, ly0 + 70
    shadow(img, (lx0, ly0, lx1, ly1), offset=(4, 6), blur=6, alpha=50)
    d = ImageDraw.Draw(img)
    d.rectangle((lx0, ly0, lx1, ly1), fill=CREAM)
    d.text(((lx0 + lx1) / 2, (ly0 + ly1) / 2 - 2), date, font=df, fill=INK, anchor="mm", **AR)
    tape(img, lx1 - 12, ly0 + 4, 90, 30, -28)

    # navy torn panel with the headline
    px0, py0, px1, py1 = M + 10, 370, W - M - 10, 1170
    poly = torn_polygon(px0, py0, px1, py1, rnd)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).polygon([(x + 10, y + 14) for x, y in poly], fill=(0, 0, 0, 80))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    d = ImageDraw.Draw(img)
    d.polygon(poly, fill=NAVY)
    tape(img, px0 + 40, py0 + 6, 170, 46, 32)
    tape(img, px1 - 40, py1 - 6, 170, 46, 32)
    d = ImageDraw.Draw(img)

    inner = 70
    maxw = (px1 - px0) - 2 * inner
    a_top, a_bot = py0 + 70, py1 - 90
    for size in (92, 84, 76, 68, 62, 56, 50):
        hf = font(size)
        lines = wrap(d, headline, hf, maxw)
        lh = int(size * 1.6)
        if len(lines) * lh <= a_bot - a_top:
            break
    y = a_top + (a_bot - a_top - len(lines) * lh) / 2
    for ln in lines:
        draw_line_rtl(d, px1 - inner, y + lh / 2, ln, hf, OFFWHITE, GOLD)
        y += lh
    # kraft underline accent
    d.rectangle((px1 - inner - 180, y + 6, px1 - inner, y + 16), fill=KRAFT)

    img.convert("RGB").save(out, "PNG", optimize=True)


if __name__ == "__main__":
    main(*sys.argv[1:5])
