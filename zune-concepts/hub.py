import os
from render import *
from PIL import Image, ImageDraw

def mini_controls(d, x, y, col):
    # prev, play, next at small size, starting x, centered y
    d.rectangle((x, y-9, x+3, y+9), fill=col); d.polygon([(x+16,y-9),(x+16,y+9),(x+4,y)], fill=col)
    d.polygon([(x+44,y-11),(x+44,y+11),(x+62,y)], fill=col)
    d.polygon([(x+86,y-9),(x+86,y+9),(x+98,y)], fill=col); d.rectangle((x+99, y-9, x+102, y+9), fill=col)

def clock(d, y=-14):
    T(d, (14, y), "06", 128, WHITE, 800)
    x = 14 + d.textlength("06", font=f(128, 800))
    T(d, (x+2, y), ":", 128, MAG, 800)
    T(d, (x+40, y), "01", 128, WHITE, 800)
    T(d, (W-16, 150), "sat oct 3 · 67%", 18, GREY, anchor="ra")

def steps_line(d, y):
    T(d, (20, y), "8,554 steps", 52, LIM, 300)
    d.rectangle((22, y+70, 368, y+73), fill=DGREY); d.rectangle((22, y+70, 22+int(346*.855), y+73), fill=LIM)

def b1(ann):  # music line = always "music" + inline controls
    im = Image.new("RGB",(W,H),BLACK); d = ImageDraw.Draw(im); clock(d)
    d.rectangle((0,196,5,246), fill=MAG)
    T(d,(20,178),"music",58,MAG,300); mini_controls(d,250,222,MAG)
    T(d,(20,264),"sunny 12°",52,ORA,300)
    steps_line(d,340)
    if ann: tap(d,(14,184,225,256),MAG); tap(d,(244,204,282,240),CYA); tap(d,(284,204,320,240),CYA); tap(d,(326,204,362,240),CYA); tap(d,(14,264,389,334),ORA); tap(d,(14,340,389,440),LIM)
    return im

def b2(ann):  # third line rotates: tap the word to cycle music / heart / battery (music shown)
    im = Image.new("RGB",(W,H),BLACK); d = ImageDraw.Draw(im); clock(d)
    T(d,(20,178),"sunny 12°",58,ORA,300); T(d,(22,250),"h 15 · l 6",18,GREY)
    T(d,(20,268),"72 bpm",58,MAG,300); T(d,(22,340),"resting 54",18,GREY)
    d.line((0,372,W,372),fill=DGREY)
    T(d,(20,384),"8,554",40,LIM,600); mini_controls(d,262,410,CYA)
    if ann: tap(d,(14,184,389,262),ORA); tap(d,(14,268,389,360),MAG); tap(d,(14,378,180,440),LIM); tap(d,(256,390,368,432),CYA)
    return im

def b3(ann):  # music as a full-width pivot word bleeding off, controls under it
    im = Image.new("RGB",(W,H),BLACK); d = ImageDraw.Draw(im); clock(d)
    T(d,(20,172),"sunny 12°",58,ORA,300)
    steps_line(d,248)
    T(d,(20,336),"music",72,CYA,300); mini_controls(d,250,382,CYA)
    if ann: tap(d,(14,178,389,244),ORA); tap(d,(14,252,389,326),LIM); tap(d,(14,344,230,440),CYA); tap(d,(244,364,362,400),CYA)
    return im

if __name__ == "__main__":
    names=[("B1 · music + controls",b1),("B2 · health, music strip",b2),("B3 · music last",b3)]
    tiles=[[frame(fn(a)) for _,fn in names] for a in (False,True)]
    tw,th=tiles[0][0].size
    sheet=Image.new("RGB",(tw*3+40,th*2+120),(20,20,22)); d=ImageDraw.Draw(sheet)
    for r,row in enumerate(tiles):
        for i,t in enumerate(row):
            x,y=10+i*(tw+10),40+r*(th+60); sheet.paste(t,(x,y))
            T(d,(x+4,y-32),names[i][0]+(" — tap zones" if r else ""),22,WHITE,500)
    sheet.save("hub.png"); print("ok")
