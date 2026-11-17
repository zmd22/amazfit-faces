import sys
from PIL import Image, ImageOps
L=[l.rstrip() for l in open(sys.argv[1]).read().splitlines()]
w=max(len(l) for l in L);s=12
im=Image.new('1',(w*s,len(L)*2*s),1)
for y,l in enumerate(L):
  for x,c in enumerate(l):
    for dy,on in ((0,c in '█▀'),(1,c in '█▄')):
      if not on and not (y==0 and dy==0): im.paste(0,(x*s,(y*2+dy)*s,(x+1)*s,(y*2+dy+1)*s))
ImageOps.expand(im,border=4*s,fill=1).save(sys.argv[2])
