from render import *
from hub import mini_controls
from PIL import Image, ImageDraw

def bell(d,cx,cy,col):
    d.pieslice((cx-8,cy-9,cx+8,cy+9),180,360,fill=col); d.rectangle((cx-8,cy,cx+8,cy+4),fill=col)
    d.rectangle((cx-10,cy+4,cx+10,cy+6),fill=col); d.ellipse((cx-2,cy+7,cx+2,cy+11),fill=col)

def c1(ann):  # heavy stack left, hub words in a right column
    im=Image.new("RGB",(W,H),BLACK); d=ImageDraw.Draw(im)
    T(d,(6,-44),"06",210,MAG,800); T(d,(6,150),"01",210,WHITE,800)
    x=250
    T(d,(x,22),"sat",30,WHITE,300); T(d,(x,56),"oct 3",22,GREY,300)
    T(d,(x,108),"12°",46,ORA,300); T(d,(x,164),"sunny",22,ORA,300)
    T(d,(x,214),"8,554",40,LIM,300); T(d,(x,262),"steps",22,LIM,300)
    d.rectangle((x,294,x+124,296),fill=DGREY); d.rectangle((x,294,x+int(124*.855),296),fill=LIM)
    T(d,(x,316),"music",38,CYA,300)
    mini_controls(d,x+6,384,CYA)
    T(d,(16,412),"67%",18,GREY)
    if ann: tap(d,(x-6,104,386,196),ORA); tap(d,(x-6,210,386,300),LIM); tap(d,(x-6,316,386,364),CYA)
    for i in range(3) if ann else []: tap(d,(x+i*42,368,x+i*42+38,402),WHITE)
    return im

def c2(ann):  # heavy stack top-left, hub lines bleed off under / beside
    im=Image.new("RGB",(W,H),BLACK); d=ImageDraw.Draw(im)
    T(d,(6,-36),"06",166,MAG,800); T(d,(6,108),"01",166,WHITE,800)
    T(d,(212,30),"saturday",28,WHITE,300); T(d,(212,64),"october 3 · 67%",22,GREY,300); bell(d,220,108,WHITE); T(d,(236,94),"07:30",22,WHITE,400)
    T(d,(212,150),"sunny",34,ORA,300); T(d,(212,190),"12°",56,ORA,300)
    T(d,(16,384),"8,554",40,LIM,600); T(d,(140,394),"steps",28,LIM,300)
    d.rectangle((0,441,W,H),fill=(40,52,22)); d.rectangle((0,441,int(W*.855),H),fill=LIM)
    T(d,(16,286),"music",52,CYA,300); mini_controls(d,250,322,CYA)
    if ann: tap(d,(216,146,386,262),ORA); tap(d,(10,380,386,449),LIM); tap(d,(10,290,200,352),CYA); tap(d,(208,92,300,122),WHITE); tap(d,(208,30,386,90),GREY); tap(d,(8,4,200,138),MAG); tap(d,(8,150,200,282),WHITE)
    for i in range(3) if ann else []: tap(d,(244+i*42,304,244+i*42+38,340),CYA)
    return im

names=[("C1 · stack + column",c1),("C2 · stack + lines",c2)]
tiles=[[frame(fn(a)) for _,fn in names] for a in (False,True)]
tw,th=tiles[0][0].size
sheet=Image.new("RGB",(tw*2+30,th*2+120),(20,20,22)); d=ImageDraw.Draw(sheet)
for r,row in enumerate(tiles):
    for i,t in enumerate(row):
        x,y=10+i*(tw+10),40+r*(th+60); sheet.paste(t,(x,y))
        T(d,(x+4,y-32),names[i][0]+(" — tap zones" if r else ""),22,WHITE,500)
sheet.save("stack.png"); print("ok")
