#!/usr/bin/env python3
"""Draw the world-news infographic for Sunday 22 November 2026.

Deterministic, stdlib + Pillow only, no network. Writes entry.png
(1024x1024, <= 1 MiB) to $MAKEFUN_OUTPUT_DIR or the current directory.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (24, 28, 38)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GREEN = (34, 120, 66)
ORANGE = (214, 110, 20)
GOLD = (196, 148, 20)
GREY = (96, 100, 108)
CARD = (255, 255, 255)
LINE = (200, 192, 176)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 34)
F_KICK = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 40)
F_CARD_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 23)
F_CARD_BODY = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 17)


def wrap(draw, text, fnt, max_w):
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


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_headline(draw, text, fnt, max_w, min_size=24):
    """Shrink headline font until it fits on one line; returns font."""
    size = fnt.size
    while size > min_size:
        f = font("DejaVuSans-Bold.ttf", size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font("DejaVuSans-Bold.ttf", min_size)


def globe(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 216, 235),
                 outline=NAVY, width=4)
    hw = int(r * 0.866)
    for dy in (-r // 2, 0, r // 2):
        w = hw if dy else r
        draw.line([cx - w, cy + dy, cx + w, cy + dy],
                  fill=(60, 120, 160), width=3)
    draw.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
                 outline=(60, 120, 160), width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=GREEN, width=8)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 120, fill=GREEN, width=8)


def card_icon(draw, cx, cy):
    draw.rounded_rectangle([cx - 52, cy - 36, cx + 52, cy + 36], radius=10,
                           fill=NAVY, outline=NAVY)
    draw.rectangle([cx - 52, cy - 20, cx + 52, cy - 6], fill=GOLD)
    draw.text((cx - 46, cy + 2), "10%", font=font("DejaVuSans-Bold.ttf", 34),
              fill=(255, 255, 255))
    draw.text((cx + 8, cy + 8), "", font=F_BODY, fill=(255, 255, 255))


def shield_icon(draw, cx, cy):
    pts = [(cx, cy - 52), (cx + 44, cy - 34), (cx + 44, cy + 6),
           (cx, cy + 52), (cx - 44, cy + 6), (cx - 44, cy - 34)]
    draw.polygon(pts, fill=RED, outline=NAVY, width=3)
    draw.line([cx - 20, cy - 2, cx - 6, cy + 14, cx + 22, cy - 18],
              fill=(255, 255, 255), width=7, joint="curve")


def burst_icon(draw, cx, cy):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = 54 if i % 2 == 0 else 26
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE, outline=RED, width=3)
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(255, 220, 90),
                 outline=RED, width=3)


def percent_icon(draw, cx, cy):
    draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52], fill=TEAL,
                 outline=NAVY, width=4)
    draw.text((cx - 30, cy - 36), "%", font=font("DejaVuSans-Bold.ttf", 64),
              fill=(255, 255, 255))


def boat_icon(draw, cx, cy):
    draw.polygon([(cx - 54, cy + 6), (cx + 54, cy + 6), (cx + 36, cy + 40),
                  (cx - 36, cy + 40)], fill=(120, 72, 30), outline=NAVY,
                 width=3)
    draw.line([cx, cy - 44, cx, cy + 6], fill=NAVY, width=5)
    draw.polygon([(cx + 4, cy - 44), (cx + 4, cy - 4), (cx + 40, cy - 4)],
                 fill=(255, 255, 255), outline=NAVY, width=2)
    for dx in (-34, 0, 34):
        draw.arc([cx + dx - 18, cy + 44, cx + dx + 18, cy + 66],
                 200, 340, fill=TEAL, width=5)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((28, 16), "WORLD NEWS", font=F_TITLE, fill=(255, 255, 255))
    d.text((996, 34), "ONE DAY  •  SIX STORIES",
           font=font("DejaVuSans-Bold.ttf", 24), fill=(200, 214, 235),
           anchor="ra")

    # ---- Date strip ----
    d.rectangle([0, 96, W, 140], fill=RED)
    d.text((512, 102), "SUNDAY 22 NOVEMBER 2026",
           font=F_DATE, fill=(255, 255, 255), anchor="ma")

    # ---- Lead story: COP31 ----
    lx, ly, lw = 28, 158, 620
    d.text((lx, ly), "CLIMATE  •  ANTALYA, TURKEY",
           font=F_KICK, fill=RED)
    head = "CLIMATE TALKS NEAR A DEAL"
    hf = fit_headline(d, head, F_HEAD, lw)
    d.text((lx, ly + 30), head, font=hf, fill=INK)
    body = ("After talks ran past their deadline into the early hours of "
            "Sunday, COP31 unveiled a new package it hopes all sides can "
            "agree on. Delegates meet on Sunday morning to approve it.")
    draw_lines(d, wrap(d, body, F_BODY, lw), lx, ly + 88, F_BODY, INK, 30)
    # globe panel
    gx0, gy0, gx1, gy1 = 692, 158, 996, 380
    d.rounded_rectangle([gx0, gy0, gx1, gy1], radius=14, fill=(226, 238, 244),
                        outline=LINE, width=2)
    globe(d, (gx0 + gx1) // 2, (gy0 + gy1) // 2 - 8, 78)
    d.text(((gx0 + gx1) // 2, gy1 - 34), "COP31",
           font=font("DejaVuSans-Bold.ttf", 26), fill=NAVY, anchor="ma")
    d.line([28, 396, 996, 396], fill=LINE, width=2)

    # ---- Four cards ----
    cards = [
        ("UNITED STATES", "TRUMP VOWS 10% CARD-RATE CAP",
         "Will work with the incoming Democratic Congress to cap card "
         "interest at 10%.", card_icon),
        ("DEFENCE  •  NORTH AMERICA", "PENTAGON CURBS CANADA TIES",
         "New limits on military cooperation; intelligence, NORAD and "
         "NATO unaffected.", shield_icon),
        ("WAR IN UKRAINE", "MISSILES HIT ZELENSKYY'S HOME CITY",
         "A Russian strike on Kryvyi Rih kills 2 and wounds 60, including "
         "six children.", burst_icon),
        ("EUROPE  •  ECONOMY", "EU PLANS 3% TAX ON BIG TECH",
         "A levy on digital giants to help fund the 2028-2034 budget. "
         "EU leaders meet next week.", percent_icon),
    ]
    cw, chh, gap = 478, 196, 20
    for i, (kick, head, body, icon) in enumerate(cards):
        x0 = 28 + (i % 2) * (cw + gap)
        y0 = 412 + (i // 2) * (chh + gap)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + chh], radius=12,
                            fill=CARD, outline=LINE, width=2)
        icon(d, x0 + 62, y0 + 62)
        tx = x0 + 132
        d.text((tx, y0 + 14), kick, font=font("DejaVuSans-Bold.ttf", 17),
               fill=RED)
        hlines = wrap(d, head, F_CARD_HEAD, cw - 150)[:2]
        hy = draw_lines(d, hlines, tx, y0 + 38, F_CARD_HEAD, INK, 31)
        lines = wrap(d, body, F_CARD_BODY, cw - 150)
        draw_lines(d, lines[:3], tx, hy + 6, F_CARD_BODY, (52, 56, 66), 25)

    # ---- Bottom strip: Nigeria ----
    sx0, sy0 = 28, 844
    d.rounded_rectangle([sx0, sy0, 996, sy0 + 116], radius=12, fill=NAVY)
    boat_icon(d, sx0 + 72, sy0 + 46)
    d.text((sx0 + 132, sy0 + 14), "AFRICA  •  NIGERIA",
           font=font("DejaVuSans-Bold.ttf", 17), fill=(255, 190, 90))
    d.text((sx0 + 132, sy0 + 38), "24 DEAD AS BOAT CAPSIZES",
           font=font("DejaVuSans-Bold.ttf", 30), fill=(255, 255, 255))
    d.text((sx0 + 132, sy0 + 76),
           "A boat carrying mourners to a funeral overturns in Bayelsa State.",
           font=F_CARD_BODY, fill=(210, 218, 230))

    # ---- Footer ----
    d.text((512, 978), "Reported 22 November 2026  •  Sources: Reuters, AP, AFP",
           font=F_FOOT, fill=GREY, anchor="ma")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
