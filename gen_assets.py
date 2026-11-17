#!/usr/bin/env python3
"""Generate PNG assets + preview for the 'Volt' face (Amazfit Active 2 Square, 390x450)."""
import math, os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets", "default.s")
os.makedirs(A, exist_ok=True)
F = "/usr/share/fonts/google-noto/"
BIG = ImageFont.truetype(F + "NotoSans-CondensedBlackItalic.ttf", 215)
SMALL = ImageFont.truetype(F + "NotoSans-CondensedBlackItalic.ttf", 30)
DATE = ImageFont.truetype(F + "NotoSans-CondensedBlackItalic.ttf", 40)
WEEK = ImageFont.truetype(F + "NotoSans-Black.ttf", 34)

YEL = (240, 240, 20, 255)
DIM = (90, 90, 10, 255)
WHITE = (255, 255, 255, 255)
GREY = (225, 225, 225, 255)
BLACK = (0, 0, 0, 255)
W, H = 390, 450

# ---------- layout (shared with JS) ----------
L = {
    "big_w": 100, "big_h": 170,
    "hour_x": 170, "hour_y": 18, "min_x": 170, "min_y": 200,
    "ring_x": 64, "ring_r": 46, "ring_w": 10,
    "bat_y": 66, "step_y": 176, "heart_y": 284, "wx_y": 392,
    "date_y": 392, "week_x": 150, "month_x": 248, "day_x": 312,
    "sm_w": 18, "sm_h": 30,
}

def save(img, name):
    img.save(os.path.join(A, name))

def glyph(text, font, size, fill, outline=None, stroke=0, dx=0):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bb = d.textbbox((0, 0), text, font=font, stroke_width=stroke)
    x = (size[0] - (bb[2] - bb[0])) / 2 - bb[0] + dx
    y = (size[1] - (bb[3] - bb[1])) / 2 - bb[1]
    d.text((x, y), text, font=font, fill=fill, stroke_width=stroke, stroke_fill=outline)
    return img

# big time digits (normal + AOD dim outline)
for i in range(10):
    save(glyph(str(i), BIG, (L["big_w"], L["big_h"]), YEL), f"big_{i}.png")
    save(glyph(str(i), BIG, (L["big_w"], L["big_h"]), BLACK, outline=DIM, stroke=3), f"aod_{i}.png")

# small outlined white digits (steps / hr / temp)
for i in range(10):
    save(glyph(str(i), SMALL, (L["sm_w"], L["sm_h"]), BLACK, outline=WHITE, stroke=2), f"sm_{i}.png")
save(glyph("-", SMALL, (L["sm_w"], L["sm_h"]), BLACK, outline=WHITE, stroke=2), "sm_minus.png")
save(glyph("°", SMALL, (L["sm_w"], L["sm_h"]), BLACK, outline=WHITE, stroke=2), "sm_deg.png")
save(glyph("%", SMALL, (26, L["sm_h"]), BLACK, outline=WHITE, stroke=2), "sm_pct.png")
save(glyph("-", SMALL, (L["sm_w"] * 2, L["sm_h"]), BLACK, outline=WHITE, stroke=2), "sm_none.png")

# date digits: light grey italic; separator yellow
for i in range(10):
    save(glyph(str(i), DATE, (24, 44), GREY), f"dt_{i}.png")
dash = Image.new("RGBA", (16, 44), (0, 0, 0, 0))
ImageDraw.Draw(dash).rectangle((3, 20, 12, 27), fill=YEL)
save(dash, "dt_sep.png")

# weekday labels (outlined)
for i, w in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
    save(glyph(w, WEEK, (92, 44), BLACK, outline=WHITE, stroke=2), f"wk_{i}.png")

# ---------- background ----------
bg = Image.new("RGBA", (W, H), BLACK)
d = ImageDraw.Draw(bg)
cx, r = L["ring_x"], L["ring_r"]
# heart outline
def heart(d, cx, cy, s, col, w):
    pts = []
    for t in range(0, 361, 3):
        a = math.radians(t)
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x * s, cy - y * s - 4))
    d.line(pts, fill=col, width=w, joint="curve")
heart(d, cx, L["heart_y"], 3.0, YEL, 9)
# weather ring (static, yellow half)
wy = L["wx_y"]
d.arc((cx - r, wy - r, cx + r, wy + r), 0, 360, fill=(45, 45, 5, 255), width=L["ring_w"])
d.arc((cx - r, wy - r, cx + r, wy + r), -90, 90, fill=YEL, width=L["ring_w"])
# step/battery ring tracks
for y in (L["bat_y"], L["step_y"]):
    d.arc((cx - r, y - r, cx + r, y + r), 0, 360, fill=(45, 45, 5, 255), width=L["ring_w"])
# footprints above steps ring
def foot(d, x, y, col):
    d.ellipse((x - 5, y - 9, x + 5, y + 5), fill=col, outline=BLACK)
    d.ellipse((x - 4, y + 7, x + 4, y + 13), fill=col)
foot(d, cx - 8, L["step_y"] - r + 2, YEL); foot(d, cx + 8, L["step_y"] - r - 4, YEL)
# bolt above battery ring
by = L["bat_y"] - r
d.polygon([(cx + 3, by - 10), (cx - 7, by + 3), (cx, by + 3), (cx - 3, by + 13), (cx + 7, by - 1), (cx, by - 1)], fill=YEL)
save(bg.convert("RGB"), "bg.png")

aod_bg = Image.new("RGB", (W, H), (0, 0, 0))
save(aod_bg, "aod_bg.png")

# ---------- weather icons (29, Zepp index order) ----------
def cloud(d, x, y, col, k=1.0):
    d.ellipse((x - 18*k, y - 4*k, x - 2*k, y + 10*k), outline=col, width=2)
    d.ellipse((x - 10*k, y - 14*k, x + 10*k, y + 6*k), outline=col, width=2)
    d.ellipse((x + 2*k, y - 6*k, x + 18*k, y + 10*k), outline=col, width=2)
    d.rectangle((x - 10*k, y - 1*k, x + 10*k, y + 8*k), fill=BLACK)
    d.line((x - 11*k, y + 10*k, x + 11*k, y + 10*k), fill=col, width=2)
def sun(d, x, y, col, rr=9):
    d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=col, width=2)
    for a in range(0, 360, 45):
        t = math.radians(a)
        d.line((x + math.cos(t) * (rr + 3), y + math.sin(t) * (rr + 3), x + math.cos(t) * (rr + 7), y + math.sin(t) * (rr + 7)), fill=col, width=2)
def moon(d, x, y, col):
    d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=col)
    d.ellipse((x - 5, y - 15, x + 15, y + 5), fill=BLACK)
def drops(d, x, y, col, n):
    for i in range(n):
        xx = x - 10 + i * (20 / max(n - 1, 1))
        d.line((xx, y, xx - 3, y + 7), fill=col, width=2)
def flakes(d, x, y, col, n):
    for i in range(n):
        xx = x - 10 + i * (20 / max(n - 1, 1))
        d.text((xx - 3, y - 2), "*", fill=col)
def bolt(d, x, y, col):
    d.line((x + 3, y, x - 3, y + 7, x + 3, y + 7, x - 3, y + 14), fill=col, width=2)
def fog(d, x, y, col):
    for i in range(3):
        d.line((x - 14, y + i * 6, x + 14, y + i * 6), fill=col, width=2)

def wicon(kind):
    im = Image.new("RGBA", (50, 44), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x, y = 25, 16
    c = WHITE
    k = kind
    if k == "sun": sun(d, x, y + 4, YEL, 10)
    elif k == "moon": moon(d, x, y + 4, c)
    elif k == "fog": fog(d, x, y, c)
    else:
        if k.startswith("pc"): sun(d, x + 10, y - 4, YEL, 6)
        if k.startswith("pn"): moon(d, x + 10, y - 4, c)
        cloud(d, x, y, c)
        if "rain" in k: drops(d, x, y + 14, c, {"rain1": 2, "rain2": 3, "rain3": 4}.get(k.split("-")[-1], 3))
        if "snow" in k: flakes(d, x, y + 12, c, 3)
        if "storm" in k: bolt(d, x, y + 12, YEL)
        if "sleet" in k: drops(d, x - 4, y + 14, c, 2); flakes(d, x + 6, y + 12, c, 2)
        if "dust" in k: fog(d, x, y + 14, (200, 170, 90, 255))
    return im
kinds = ["cloud", "pc-rain2", "pc-snow", "sun", "cloud", "rain1", "snow", "rain2", "snow",
         "snow", "rain3", "dust", "sleet", "fog", "fog", "storm", "snow", "dust",
         "rain3", "sleet", "storm", "rain3", "dust", "dust", "rain3", "cloud", "pn", "pn-rain2", "moon"]
for i, k in enumerate(kinds):
    save(wicon(k), f"wx_{i}.png")

# icon for app list
ic = Image.new("RGBA", (248, 248), (0, 0, 0, 255))
ImageDraw.Draw(ic).ellipse((0, 0, 247, 247), fill=BLACK)
g = glyph("V", ImageFont.truetype(F + "NotoSans-CondensedBlackItalic.ttf", 200), (248, 248), YEL)
ic.alpha_composite(g)
save(ic, "icon.png")

with open(os.path.join(ROOT, "layout.json"), "w") as fh:
    json.dump(L, fh, indent=1)

# ---------- preview (mirrors watchface/index.js) ----------
def preview(out, hh="14", mm="18", steps=8554, hr=57, temp=-4, bat=72, wk=0, mon="05", day="01", wx=5):
    p = Image.open(os.path.join(A, "bg.png")).convert("RGBA")
    dd = ImageDraw.Draw(p)
    for y, val in ((L["bat_y"], bat / 100), (L["step_y"], min(steps / 10000, 1))):
        dd.arc((cx - r, y - r, cx + r, y + r), -90, -90 + 360 * val, fill=YEL, width=L["ring_w"])
    def paste(name, x, y): p.alpha_composite(Image.open(os.path.join(A, name)), (int(x), int(y)))
    for i, ch in enumerate(hh): paste(f"big_{ch}.png", L["hour_x"] + i * L["big_w"], L["hour_y"])
    for i, ch in enumerate(mm): paste(f"big_{ch}.png", L["min_x"] + i * L["big_w"], L["min_y"])
    def num(s, y, unit=None):
        names = [("sm_minus.png" if c == "-" else f"sm_{c}.png") for c in s] + ([unit] if unit else [])
        x = cx - len(names) * L["sm_w"] / 2
        for n in names: paste(n, x, y); x += Image.open(os.path.join(A, n)).width
    num(str(bat), L["bat_y"] - 15, "sm_pct.png")
    num(str(steps), L["step_y"] - 15)
    num(str(hr), L["heart_y"] - 20)
    paste(f"wx_{wx}.png", cx - 25, L["wx_y"] - 36)
    num(str(temp), L["wx_y"] + 6, "sm_deg.png")
    paste(f"wk_{wk}.png", L["week_x"], L["date_y"])
    paste(f"dt_{mon[0]}.png", L["month_x"], L["date_y"]); paste(f"dt_{mon[1]}.png", L["month_x"] + 24, L["date_y"])
    paste("dt_sep.png", L["month_x"] + 48, L["date_y"])
    paste(f"dt_{day[0]}.png", L["day_x"], L["date_y"]); paste(f"dt_{day[1]}.png", L["day_x"] + 24, L["date_y"])
    p.convert("RGB").save(out)

if __name__ == "__main__":
    preview(os.path.join(ROOT, "preview.png"))
    # store preview (zepp uses it in the face picker)
    Image.open(os.path.join(ROOT, "preview.png")).save(os.path.join(A, "preview.png"))
    print("ok")
