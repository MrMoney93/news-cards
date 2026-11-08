#!/usr/bin/env python3
"""News card generator: python3 make_card.py "<headline>" "<category>" "<date>" out.png
category one of: اقتصاد | بزنس | منوعات | سياسة
Needs fonts/Cairo.ttf next to this script (Pillow with raqm)."""
import sys, os
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "Cairo.ttf")
ACCENT = {"اقتصاد": (16, 185, 129), "بزنس": (59, 130, 246),
          "منوعات": (245, 158, 11), "سياسة": (239, 68, 68)}

def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f

def tw(d, t, f):
    b = d.textbbox((0, 0), t, font=f, direction="rtl", language="ar")
    return b[2] - b[0], b[3] - b[1]

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        test = (cur + " " + w).strip()
        if tw(d, test, f)[0] <= maxw:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def main(headline, category, date, out):
    acc = ACCENT.get(category, (16, 185, 129))
    img = Image.new("RGB", (W, H))
    px = img.load()
    top, bot = (12, 22, 45), (24, 40, 78)
    img.paste(top, (0, 0, W, H))
    d = ImageDraw.Draw(img)
    # decorative accent circles
    d.ellipse((-220, -220, 300, 300), outline=acc + (0,), width=3)
    d.ellipse((780, 760, 1300, 1280), outline=acc, width=3)
    # top bar
    d.rectangle((0, 0, W, 14), fill=acc)
    # category badge (top right)
    bf = font(40)
    bw, bh = tw(d, category, bf)
    pad = 26
    x1 = W - 70
    x0 = x1 - bw - 2 * pad
    d.rounded_rectangle((x0, 80, x1, 80 + 76), radius=38, fill=acc)
    d.text(((x0 + x1) / 2, 80 + 38), category, font=bf, fill="white",
           anchor="mm", direction="rtl", language="ar")
    # date (top left)
    d.text((70, 118), date, font=font(34, "Regular"), fill=(170, 185, 210),
           anchor="lm", direction="rtl", language="ar")
    # headline, auto-shrink to fit
    maxw, area_top, area_bot = W - 140, 220, 860
    for size in (84, 76, 68, 60, 54, 48):
        hf = font(size)
        lines = wrap(d, headline, hf, maxw)
        lh = int(size * 1.55)
        if len(lines) * lh <= area_bot - area_top:
            break
    total = len(lines) * lh
    y = area_top + (area_bot - area_top - total) / 2
    for ln in lines:
        d.text((W - 70, y + lh / 2), ln, font=hf, fill="white",
               anchor="rm", direction="rtl", language="ar")
        y += lh
    # accent line under headline
    d.rectangle((W - 70 - 160, y + 10, W - 70, y + 18), fill=acc)
    # footer
    d.rectangle((0, 940, W, H), fill=(8, 14, 30))
    d.text((W / 2, 1010), "محمد طلعت  |  Mohamed Talaat", font=font(40),
           fill="white", anchor="mm", direction="rtl", language="ar")
    img.quantize(48).save(out, "PNG", optimize=True)

if __name__ == "__main__":
    main(*sys.argv[1:5])
