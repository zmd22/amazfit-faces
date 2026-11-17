#!/usr/bin/env python3
"""Concept renders for a Zune-inspired Active 2 Square face (390x450). Not a build."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
VF = "/home/altxego/Desktop/Claude Code/diskos-disco/ui/fonts/zune/OpenSans-VF.ttf"
W, H = 390, 450
MAG, ORA, CYA, LIM, PUR = (236, 0, 140), (247, 148, 29), (0, 174, 239), (141, 198, 63), (150, 80, 220)
WHITE, GREY, DGREY, BLACK = (255, 255, 255), (150, 150, 150), (70, 70, 70), (0, 0, 0)

def f(size, wght=300):
    ft = ImageFont.truetype(VF, size)
    try: ft.set_variation_by_axes([wght, 100])
    except Exception: ft.set_variation_by_axes([wght])
    return ft

def T(d, xy, s, size, col, wght=300, anchor="la"):
    d.text(xy, s, font=f(size, wght), fill=col, anchor=anchor)
    return d.textlength(s, font=f(size, wght))

def tap(d, box, col):  # tap-zone marker (only in annotated renders)
    x0, y0, x1, y1 = box
    for x in range(x0, x1, 8): d.line((x, y0, min(x + 4, x1), y0), fill=col); d.line((x, y1, min(x + 4, x1), y1), fill=col)
    for y in range(y0, y1, 8): d.line((x0, y, x0, min(y + 4, y1)), fill=col); d.line((x1, y, x1, min(y + 4, y1)), fill=col)

def controls(d, cx, cy, col, r=22):
    # prev | play/pause | next
    d.polygon([(cx - 70, cy), (cx - 58, cy - 9), (cx - 58, cy + 9)], fill=col); d.rectangle((cx - 74, cy - 9, cx - 71, cy + 9), fill=col)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=2)
    d.rectangle((cx - 7, cy - 8, cx - 3, cy + 8), fill=col); d.rectangle((cx + 3, cy - 8, cx + 7, cy + 8), fill=col)
    d.polygon([(cx + 70, cy), (cx + 58, cy - 9), (cx + 58, cy + 9)], fill=col); d.rectangle((cx + 71, cy - 9, cx + 74, cy + 9), fill=col)

# ---- A: Pivot — huge time bleeding off edge, pivot headers as complications
def concept_a(ann):
    im = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(im)
    T(d, (18, 14), "67%", 18, GREY)
    T(d, (W - 18, 14), "saturday, october 3", 18, GREY, anchor="ra")
    T(d, (-12, -34), "06", 190, MAG, 300)
    T(d, (176, 70), "01", 190, WHITE, 300)
    T(d, (20, 300), "saturday, october 3", 20, GREY) if False else None
    # pivot row: headers cropped off right
    x = 20
    for word, col in (("weather", WHITE), ("music", DGREY), ("steps", DGREY)):
        x += T(d, (x, 335), word, 44, col, 300) + 18
    T(d, (20, 395), "sunny  12°", 30, ORA, 600)
    T(d, (200, 403), "h 15  l 6", 20, GREY)
    if ann:
        tap(d, (14, 335, 200, 440), ORA); tap(d, (205, 335, 389, 395), CYA)
    return im

# ---- B: Hub — Zune home menu as complications, each line a color
def concept_b(ann):
    im = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(im)
    T(d, (20, 10), "06:01", 96, WHITE, 300)
    T(d, (W - 18, 30), "sat", 22, GREY, anchor="ra"); T(d, (W - 18, 58), "oct 3", 22, GREY, anchor="ra")
    d.rectangle((0, 146, 5, 196), fill=MAG)
    T(d, (20, 128), "northern lights", 58, MAG, 300)
    T(d, (22, 200), "The Midnight · now playing", 18, GREY)
    T(d, (20, 228), "sunny 12°", 58, ORA, 300)
    T(d, (22, 300), "h 15 · l 6 · berlin", 18, GREY)
    T(d, (20, 322), "8,554 steps", 58, LIM, 300)
    d.rectangle((22, 400, 22 + 346, 404), fill=DGREY); d.rectangle((22, 400, 22 + int(346 * .855), 404), fill=LIM)
    T(d, (22, 414), "86% of 10,000", 18, GREY)
    if ann:
        tap(d, (14, 130, 389, 224), MAG); tap(d, (14, 228, 389, 318), ORA); tap(d, (14, 322, 389, 440), LIM)
    return im

# ---- C: Bold stack — heavy weight time, colored tiles row
def concept_c(ann):
    im = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(im)
    T(d, (8, -40), "06", 200, MAG, 800)
    T(d, (8, 128), "01", 200, WHITE, 800)
    T(d, (W - 16, 30), "saturday", 26, WHITE, 300, anchor="ra")
    T(d, (W - 16, 62), "october 3", 22, GREY, anchor="ra")
    T(d, (W - 16, 92), "67%", 22, GREY, anchor="ra")
    # three tiles
    tiles = (("12°", "sunny", ORA), ("8.5k", "steps", LIM), ("", "play", CYA))
    for i, (big, small, col) in enumerate(tiles):
        x = 12 + i * 126
        d.rectangle((x, 352, x + 116, 438), fill=col)
        T(d, (x + 10, 350), big, 46, BLACK, 700)
        T(d, (x + 10, 408), small, 20, BLACK, 600)
        if not big: d.polygon([(x + 14, 364), (x + 14, 400), (x + 44, 382)], fill=BLACK)
    if ann:
        for i in range(3): tap(d, (8 + i * 126, 348, 8 + i * 126 + 124, 442), WHITE)
    return im

# ---- D: Now playing — music first, time is the accent
def concept_d(ann):
    im = Image.new("RGB", (W, H), BLACK); d = ImageDraw.Draw(im)
    T(d, (20, 4), "06", 120, MAG, 300); T(d, (164, 4), ":", 120, DGREY, 300); T(d, (196, 4), "01", 120, WHITE, 300)
    T(d, (W - 18, 154), "sat 3", 20, GREY, anchor="ra"); T(d, (W - 18, 180), "67%", 20, GREY, anchor="ra")
    T(d, (20, 150), "northern", 64, WHITE, 600)
    T(d, (20, 214), "lights", 64, WHITE, 600)
    T(d, (22, 292), "the midnight · afterglow", 20, PUR, 400)
    controls(d, W // 2, 352, WHITE)
    d.line((0, 392, W, 392), fill=DGREY)
    T(d, (20, 404), "sunny 12°", 26, ORA, 600)
    T(d, (W - 20, 404), "8,554", 26, LIM, 600, anchor="ra")
    if ann:
        tap(d, (102, 328, 142, 376), CYA); tap(d, (172, 328, 218, 376), CYA); tap(d, (248, 328, 288, 376), CYA)
        tap(d, (14, 398, 150, 440), ORA); tap(d, (240, 398, 376, 440), LIM)
    return im

def frame(im):  # square watch bezel mock
    pad = 24
    out = Image.new("RGB", (W + pad * 2, H + pad * 2), (35, 35, 38))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, W - 1, H - 1), 48, fill=255)
    out.paste(im, (pad, pad), m)
    return out

if __name__ == "__main__":
    names = [("A · pivot", concept_a), ("B · hub", concept_b), ("C · bold stack", concept_c), ("D · now playing", concept_d)]
    rows = []
    for ann in (False, True):
        tiles = [frame(fn(ann)) for _, fn in names]
        rows.append(tiles)
    tw, th = rows[0][0].size
    sheet = Image.new("RGB", (tw * 4 + 50, th * 2 + 120), (20, 20, 22))
    d = ImageDraw.Draw(sheet)
    for r, tiles in enumerate(rows):
        for i, t in enumerate(tiles):
            x, y = 10 + i * (tw + 10), 40 + r * (th + 60)
            sheet.paste(t, (x, y))
            T(d, (x + 4, y - 32), names[i][0] + (" — tap zones" if r else ""), 22, WHITE, 500)
    sheet.save(os.path.join(HERE, "concepts.png"))
    for n, fn in names:
        frame(fn(False)).save(os.path.join(HERE, n.split(" ")[0] + ".png"))
    print("ok")
