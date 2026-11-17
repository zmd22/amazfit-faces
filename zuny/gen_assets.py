#!/usr/bin/env python3
"""Zuny — assets + preview for Amazfit Active 2 (NFC) Square, 390x450."""
import os, json
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets", "default.s")
os.makedirs(A, exist_ok=True)
VF = "/home/altxego/Desktop/Claude Code/diskos-disco/ui/fonts/zune/OpenSans-VF.ttf"
W, H = 390, 450

ACCENTS = {"mag": (236, 0, 140), "ora": (247, 148, 29), "cya": (0, 174, 239), "lim": (141, 198, 63), "pur": (150, 80, 220)}
ORA, CYA, LIM = ACCENTS["ora"], ACCENTS["cya"], ACCENTS["lim"]
WHITE, GREY, AODC = (255, 255, 255), (150, 150, 150), (110, 110, 110)

def font(size, wght):
    f = ImageFont.truetype(VF, size); f.set_variation_by_axes([wght, 100]); return f

def save(im, name): im.save(os.path.join(A, name))

def txt(s, size, wght, col, line=None, base=None, width=None, outline=False):
    """Text image with fixed line box so baselines align. line/base default from font."""
    f = font(size, wght)
    asc, desc = f.getmetrics()
    line = line or asc + desc
    base = base if base is not None else asc
    w = int(width or max(1, round(f.getlength(s))))
    im = Image.new("RGBA", (w, line), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if outline:
        d.text((0, base), s, font=f, anchor="ls", fill=(0, 0, 0, 255), stroke_width=2, stroke_fill=col + (255,))
    else:
        d.text((0, base), s, font=f, anchor="ls", fill=col + (255,))
    return im

# ---------- big time ----------
BIG = 166; BIGW = 98
fb = font(BIG, 800); asc_b = fb.getmetrics()[0]
TOP, BOT = 52, 184           # crop band (glyph top 57, baseline 178/180)
def bigdigit(i, col, outline=False):
    im = txt(str(i), BIG, 800, col, width=BIGW, outline=outline)
    return im.crop((0, TOP, BIGW, BOT))
for k, c in ACCENTS.items():
    for i in range(10): save(bigdigit(i, c), f"h_{k}_{i}.png")
for i in range(10):
    save(bigdigit(i, WHITE), f"m_{i}.png")
    save(bigdigit(i, AODC, True), f"a_{i}.png")

# ---------- small sets ----------
def digitset(prefix, size, wght, col):
    f = font(size, wght); w = round(f.getlength("0"))
    for i in range(10): save(txt(str(i), size, wght, col, width=w), f"{prefix}_{i}.png")
    return w, f.getmetrics()
# date day / battery (grey 22)
dw, (dasc, ddesc) = digitset("g", 26, 500, GREY)
save(txt("%", 26, 500, GREY), "g_pct.png")
# alarm (white 22)
digitset("w", 26, 500, WHITE)
save(txt(":", 26, 500, WHITE), "w_col.png")
# temperature (orange 56)
tw_, (tasc, tdesc) = digitset("t", 56, 300, ORA)
save(txt("-", 56, 300, ORA), "t_neg.png"); save(txt("°", 56, 300, ORA), "t_deg.png")
save(txt("--", 56, 300, ORA), "t_none.png")
# steps (lime 40 semibold) + unit "steps" in 28 on same baseline
sw, (sasc, sdesc) = digitset("s", 40, 600, LIM)
save(txt("  steps", 28, 300, LIM, line=sasc + sdesc, base=sasc), "s_unit.png")

# ---------- words ----------
for i, n in enumerate(["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]):
    save(txt(n, 32, 400, WHITE), f"wk_{i}.png")
months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
for i, n in enumerate(months):  # same line box as grey digits so day follows on baseline
    save(txt(n + " ", 26, 500, GREY), f"mo_{i}.png")
wx = ["cloudy", "showers", "snow showers", "sunny", "overcast", "light rain", "light snow", "rain", "snow",
      "heavy snow", "heavy rain", "sandstorm", "sleet", "fog", "haze", "storm", "blizzard", "dust",
      "downpour", "hail", "storm", "downpour", "dust", "sandstorm", "rainstorm", "unknown", "cloudy", "showers", "clear"]
for i, n in enumerate(wx):
    save(txt(n, 34 if len(n) < 10 else 26, 300, ORA, line=48, base=37), f"wx_{i}.png")
save(txt("music", 68, 300, CYA), "music.png")

# bell (alarm on)
bell = Image.new("RGBA", (22, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(bell); cx, cy = 10, 13
d.pieslice((cx - 8, cy - 9, cx + 8, cy + 9), 180, 360, fill=WHITE); d.rectangle((cx - 8, cy, cx + 8, cy + 4), fill=WHITE)
d.rectangle((cx - 10, cy + 4, cx + 10, cy + 6), fill=WHITE); d.ellipse((cx - 2, cy + 7, cx + 2, cy + 11), fill=WHITE)
save(bell, "bell.png")

# music controls (one image, three tap zones laid over it)
ctl = Image.new("RGBA", (110, 30), (0, 0, 0, 0)); d = ImageDraw.Draw(ctl); x, y = 4, 15
d.rectangle((x, y - 9, x + 3, y + 9), fill=CYA); d.polygon([(x + 16, y - 9), (x + 16, y + 9), (x + 4, y)], fill=CYA)
d.polygon([(x + 44, y - 11), (x + 44, y + 11), (x + 62, y)], fill=CYA)
d.polygon([(x + 86, y - 9), (x + 86, y + 9), (x + 98, y)], fill=CYA); d.rectangle((x + 99, y - 9, x + 102, y + 9), fill=CYA)
save(ctl, "ctl.png")

# steps bar levels 0..20
NB = 21
for i in range(NB):
    b = Image.new("RGB", (W, 9), (40, 52, 22)); ImageDraw.Draw(b).rectangle((0, 0, int(W * i / (NB - 1)) - 1, 8), fill=LIM) if i else None
    save(b, f"bar_{i}.png")

save(Image.new("RGBA", (4, 4), (0, 0, 0, 0)), "hit.png")
save(Image.new("RGB", (W, H), (0, 0, 0)), "bg.png")

# app icon
ic = Image.new("RGBA", (248, 248), (0, 0, 0, 255))
g = txt("z", 220, 800, ACCENTS["mag"]); ic.alpha_composite(g, ((248 - g.width) // 2, -30))
save(ic, "icon.png")

# ---------- layout shared with JS ----------
L = dict(
    hour=(6, -36 + TOP), minute=(6, 108 + TOP), big_w=BIGW,
    week=(212, 34), month=(212, 76), batt=(212, 4), alarm_bell=(211, 116), alarm=(238, 110),
    wx=(212, 150 - 3), temp=(212, 190), music=(14, 282),
    steps=(16, 384), bar=(0, 441), nb=NB, dw=dw, sw=sw, tw=tw_,
    accents=list(ACCENTS.keys()), accent_rgb={k: "0x%02x%02x%02x" % v for k, v in ACCENTS.items()},
)
json.dump(L, open(os.path.join(ROOT, "layout.json"), "w"), indent=1)

# ---------- preview (same coordinates the JS uses) ----------
def preview(out, accent="mag", aod=False, hh="06", mm="01", wk=5, mon=9, day="3", bat="67", alarm="07:30",
            wxi=3, temp="12", steps="8554", prog=.855):
    p = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    def P(n, xy): p.alpha_composite(Image.open(os.path.join(A, n)).convert("RGBA"), (int(xy[0]), int(xy[1])))
    def row(names, x, y):
        for n in names: P(n, (x, y)); x += Image.open(os.path.join(A, n)).width
        return x
    hp = "a" if aod else f"h_{accent}"; mp = "a" if aod else "m"
    for i, c in enumerate(hh): P(f"{hp}_{c}.png", (L["hour"][0] + i * BIGW, max(0, L["hour"][1])))
    for i, c in enumerate(mm): P(f"{mp}_{c}.png", (L["minute"][0] + i * BIGW, L["minute"][1]))
    P(f"wk_{wk}.png", L["week"])
    row([f"mo_{mon}.png"] + [f"g_{c}.png" for c in day], *L["month"])
    if not aod:
        bn = [f"g_{c}.png" for c in bat] + ["g_pct.png"]
        row(bn, *L["batt"])
        if alarm:
            P("bell.png", L["alarm_bell"]); row([("w_col.png" if c == ":" else f"w_{c}.png") for c in alarm], *L["alarm"])
        P(f"wx_{wxi}.png", L["wx"]); row([f"t_{c}.png" for c in temp] + ["t_deg.png"], *L["temp"])
        P("music.png", L["music"])
        row([f"s_{c}.png" for c in steps] + ["s_unit.png"], *L["steps"])
        P(f"bar_{round(prog * (NB - 1))}.png", L["bar"])
    p.convert("RGB").save(out)

if __name__ == "__main__":
    preview(os.path.join(ROOT, "preview.png"))
    preview(os.path.join(ROOT, "preview-aod.png"), aod=True)
    preview(os.path.join(ROOT, "preview-cyan.png"), accent="cya", alarm=None)
    Image.open(os.path.join(ROOT, "preview.png")).save(os.path.join(A, "preview.png"))
    print("ok")
