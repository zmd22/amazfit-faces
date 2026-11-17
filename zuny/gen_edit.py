#!/usr/bin/env python3
"""Edit-mode assets for Zuny + generated watchface/mid.js (option table for the editable slot)."""
import json, os
from PIL import Image, ImageDraw
import gen_assets as g  # regenerates base assets on import

A = g.A
ORA, LIM, CYA = g.ORA, g.LIM, g.CYA

def frame(w, h, col, dashed=False):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if dashed:
        for x in range(0, w, 12): d.line((x, 1, x + 6, 1), fill=col, width=3); d.line((x, h - 2, x + 6, h - 2), fill=col, width=3)
        for y in range(0, h, 12): d.line((1, y, 1, y + 6), fill=col, width=3); d.line((w - 2, y, w - 2, y + 6), fill=col, width=3)
    else:
        d.rounded_rectangle((1, 1, w - 2, h - 2), 14, outline=col, width=4)
    return im

SLOTS = {"acc": (200, 138), "mid": (178, 128), "bot": (376, 66)}
for k, (w, h) in SLOTS.items():
    g.save(frame(w, h, g.ACCENTS["cya"] + (255,)), f"ed_{k}_sel.png")
    g.save(frame(w, h, (120, 120, 120, 255), dashed=True), f"ed_{k}_uns.png")
tip = Image.new("RGBA", (130, 34), (0, 0, 0, 0))
ImageDraw.Draw(tip).rounded_rectangle((0, 0, 129, 33), 16, fill=(40, 40, 40, 255))
g.save(tip, "ed_tip.png")

for k in g.ACCENTS:
    p = Image.new("RGBA", SLOTS["acc"], (0, 0, 0, 255))
    for i, c in enumerate("06"):
        p.alpha_composite(Image.open(f"{A}/h_{k}_{c}.png").convert("RGBA"), (2 + i * g.BIGW, 4))
    g.save(p, f"ed_acc_{k}.png")

# ---- big weather row (orange): condition words sized to fit left of temp ----
for i, n in enumerate(g.wx):
    size = 52 if len(n) <= 7 else 40 if len(n) <= 10 else 32
    g.save(g.txt(n, size, 300, ORA, line=77, base=60), f"wb_{i}.png")

# ---- cyan number set for the editable slot ----
cw, (casc, cdesc) = g.digitset("c", 56, 300, CYA)
CL = casc + cdesc
for name, s in (("neg", "-"), ("deg", "°"), ("dot", "."), ("col", ":"), ("pct", "%"), ("none", "--"), ("sl", "/")):
    g.save(g.txt(s, 56, 300, CYA), f"c_{name}.png")
for u in ("bpm", "kcal", "km", "m", "min", "h"):
    g.save(g.txt(" " + u, 26, 300, CYA, line=CL, base=casc), f"c_u_{u}.png")
sasc, sdesc = g.font(40, 600).getmetrics()
g.save(g.txt("  kcal", 28, 300, LIM, line=sasc + sdesc, base=sasc), "s_kcal.png")

for i, n in enumerate(g.wx):
    g.save(g.txt(n, 30 if len(n) < 11 else 24, 300, CYA, line=48, base=37), f"wc_{i}.png")

# key, editor title, label, data_type, unit, app, sample, extra
MID = [
    ("hr", "heart rate", "heart rate", "HEART", "c_u_bpm", "heart", "72", ""),
    ("cal", "calories", "calories", "CAL", "c_u_kcal", "steps", "420", ""),
    ("spo", "blood oxygen", "blood oxygen", "SPO2", "c_pct", "spo", "97", ""),
    ("stress", "stress", "stress", "STRESS", "", "stress", "32", ""),
    ("pai", "PAI", "weekly pai", "PAI_WEEKLY", "", "pai", "86", ""),
    ("dist", "distance", "distance", "DISTANCE", "c_u_km", "steps", "5.4", "dot"),
    ("stand", "stand", "stand", "STAND", "c_u_h", "steps", "8", ""),
    ("fat", "fat burning", "fat burning", "FAT_BURNING", "c_u_min", "steps", "24", ""),
    ("steps", "steps", "steps", "STEP", "", "steps", "8554", ""),
    ("hum", "humidity", "humidity", "HUMIDITY", "c_pct", "weather", "64", ""),
    ("uvi", "UV index", "uv index", "UVI", "", "weather", "3", ""),
    ("rise", "sunrise", "sunrise", "SUN_RISE", "", "weather", "07:41", "col"),
    ("set", "sunset", "sunset", "SUN_SET", "", "weather", "16:22", "col"),
    ("hilo", "high / low", "high / low", "WEATHER_HIGH", "c_deg", "weather", "15", "hilo"),
    ("alt", "altitude", "altitude", "ALTIMETER", "c_u_m", "alti", "312", "neg"),
    ("floor", "floors", "floors", "FLOOR", "", "steps", "6", ""),
    ("batt", "battery", "battery", "BATTERY", "c_pct", "battery", "67", ""),
    ("weather", "weather", None, "WEATHER_CURRENT", "c_deg", "weather", "12", "neg"),
]
def put(p, names, x, y):
    for n in names:
        im = Image.open(f"{A}/{n}.png").convert("RGBA"); p.alpha_composite(im, (x, y)); x += im.width
    return x
for key, title, label, dt, unit, app, sample, extra in MID:
    if label:
        g.save(g.txt(label, 30 if len(label) < 11 else 26, 300, CYA, line=48, base=37), f"lb_{key}.png")
    p = Image.new("RGBA", SLOTS["mid"], (0, 0, 0, 255))
    if label: put(p, [f"lb_{key}"], 4, 4)
    else:
        g.save(g.txt("sunny", 30, 300, CYA, line=48, base=37), "lb_tmp.png"); put(p, ["lb_tmp"], 4, 4)
    m = {".": "c_dot", ":": "c_col"}
    digits = [m.get(c, f"c_{c}") for c in sample]
    x = put(p, digits + ([unit] if unit else []), 4, 40)
    if extra == "hilo": put(p, ["c_sl", "c_6", "c_deg"], x, 40)
    g.save(p, f"ed_mid_{key}.png")
os.remove(f"{A}/lb_tmp.png")

def bot_preview(digits, unit):
    p = Image.new("RGBA", SLOTS["bot"], (0, 0, 0, 255))
    put(p, [f"s_{c}" for c in digits] + [unit], 6, 4); return p
g.save(bot_preview("8554", "s_unit"), "ed_bot_steps.png")
g.save(bot_preview("420", "s_kcal"), "ed_bot_cal.png")

opts = [dict(key=k, title=t, label=(f"lb_{k}.png" if l else None), dt=dt, unit=(u + ".png" if u else None),
             app=a, extra=e, type=100201 + i) for i, (k, t, l, dt, u, a, s, e) in enumerate(MID)]
with open(os.path.join(g.ROOT, "watchface", "mid.js"), "w") as fh:
    fh.write("// generated by gen_edit.py\nexport const MID = " + json.dumps(opts, indent=1) + "\n")
# full-face preview (new layout): weather row + heart-rate slot
def face(out):
    p = Image.new("RGBA", (g.W, g.H), (0, 0, 0, 255))
    base = Image.open(os.path.join(g.ROOT, "preview.png")).convert("RGBA")
    p.alpha_composite(base.crop((0, 0, g.W, 146)), (0, 0)); p.alpha_composite(base.crop((0, 146, 206, 282)), (0, 146))
    p.alpha_composite(base.crop((0, 380, g.W, g.H)), (0, 380))
    put(p, ["lb_hr"], 212, 147); put(p, ["c_7", "c_2", "c_u_bpm"], 212, 190)
    put(p, ["wb_3"], 14, 284)
    tw = sum(Image.open(f"{A}/{n}.png").width for n in ["t_1", "t_2", "t_deg"])
    put(p, ["t_1", "t_2", "t_deg"], 382 - tw, 284)
    p.convert("RGB").save(out)
face(os.path.join(g.ROOT, "preview.png")); Image.open(os.path.join(g.ROOT, "preview.png")).save(f"{A}/preview.png")
print("edit ok", len(opts), "slot options; cyan line", CL, "digit w", cw)
