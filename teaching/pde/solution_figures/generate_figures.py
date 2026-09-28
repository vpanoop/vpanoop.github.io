"""Regenerate the vector PDF characteristic sketches (requires PyMuPDF)."""
import math
from pathlib import Path
import fitz

OUT = Path(__file__).resolve().parent
BLUE = (0.12, 0.30, 0.55)
RED = (0.70, 0.18, 0.12)
GRAY = (0.48, 0.48, 0.48)

class Plot:
    def __init__(self, bounds):
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=440, height=300)
        self.bounds = bounds
        self.rect = fitz.Rect(44, 16, 414, 266)
        self.page.draw_rect(self.rect, color=(.8,.8,.8), width=.5)
        xmin,xmax,ymin,ymax=bounds
        for x in range(math.ceil(xmin),math.floor(xmax)+1):
            p=self.point(x,ymin)
            self.page.insert_text((p.x-3,280),str(x),fontsize=9)
            self.line([(x,ymin),(x,ymax)],color=(.91,.91,.91),width=.4)
        for y in range(math.ceil(ymin),math.floor(ymax)+1):
            p=self.point(xmin,y)
            self.page.insert_text((22,p.y+3),str(y),fontsize=9)
            self.line([(xmin,y),(xmax,y)],color=(.91,.91,.91),width=.4)
        if ymin<=0<=ymax:self.line([(xmin,0),(xmax,0)],color=GRAY,width=.7)
        if xmin<=0<=xmax:self.line([(0,ymin),(0,ymax)],color=GRAY,width=.7)
        self.page.insert_text((420,270),'x',fontsize=11)
        self.page.insert_text((30,12),'y',fontsize=11)
    def point(self,x,y):
        a,b,c,d=self.bounds
        return fitz.Point(44+(x-a)/(b-a)*370,266-(y-c)/(d-c)*250)
    def line(self,pts,color=BLUE,width=1.15,dashes=None):
        # Split curves at excluded points and poles; keep every segment inside axes.
        a,b,c,d=self.bounds
        buf=[]
        def flush():
            if len(buf)>1:
                shape=self.page.new_shape();shape.draw_polyline(buf)
                shape.finish(color=color,width=width,dashes=dashes,closePath=False);shape.commit()
            buf.clear()
        for x,y in pts:
            if not(math.isfinite(x) and math.isfinite(y) and a<=x<=b and c<=y<=d):
                flush();continue
            p=self.point(x,y)
            buf.append(p)
        flush()
    def curve(self,f,start,end,n=1200,**kw):
        pts=[]
        for i in range(n+1):
            t=start+(end-start)*i/n
            try:pts.append(f(t))
            except (ValueError,ZeroDivisionError,OverflowError):pts.append((math.nan,math.nan))
        self.line(pts,**kw)
    def arrow(self,x,y,dx,dy,color=BLUE):
        p=self.point(x,y);q=self.point(x+dx,y+dy)
        v=q-p; length=abs(v)
        if not length:return
        v=v/length
        self.page.draw_line(p,q,color=color,width=1.1)
        normal=fitz.Point(-v.y,v.x)
        for sign in [-1,1]:self.page.draw_line(q,q-v*5+normal*(2.5*sign),color=color,width=1.1)
    def save(self,name):self.doc.save(OUT/name,deflate=True)

p=Plot((-4,2,-2,4))
for C in [-1,-.3,0,.18,.5,1,2]:
    for lo,hi in [(-4,-2),(-2,2)]:p.curve(lambda x:(x,C*(x+2)**2),lo,hi)
p.line([(-2,-2),(-2,4)],color=GRAY,dashes='[3 3] 0')
p.line([(-1,0),(-1,4)],color=RED,width=2)
p.arrow(-.5,1.125,.18,.29);p.arrow(-3,.5,-.18,.18)
p.save('problem-1.pdf')

p=Plot((0,3,0,4))
for m in [.25,.5,1,2,math.e,4,8]:p.curve(lambda x:(x,m*x),0,3)
p.curve(lambda x:(x,1/x),.25,3,color=RED,width=1.8)
p.curve(lambda t:(math.cos(t),math.sin(t)),0,math.pi/2,color=RED,width=1.8,dashes='[4 3] 0')
p.curve(lambda x:(x,math.exp(x)),0,math.log(4),color=(.32,.48,.18),width=1.8)
p.arrow(1.2,1.2,.2,.2)
p.save('problem-2.pdf')

p=Plot((-3,3,0,4))
for s in [-2.5,-1.5,-.7,0,.7,1.5,2.5]:p.curve(lambda y:(s*y,y),.02,4)
p.line([(-3,1),(3,1)],color=RED,width=2)
p.arrow(1.26,1.8,.168,.24)
p.save('problem-3a.pdf')

# Equal physical scales for x and y preserve the circular geometry.
p=Plot((-3.7,3.7,-2.5,2.5))
for r in [.5,1,1.5,2,2.4]:p.curve(lambda t:(r*math.cos(t),r*math.sin(t)),0,2*math.pi)
p.line([(-3.7,0),(3.7,0)],color=RED,width=2)
p.arrow(0,1.5,.23,-.018)
p.save('problem-3b.pdf')

p=Plot((0,3,-3,3))
for s in [-3,-1.5,-.5,0,.5,1.5,3]:
    p.curve(lambda x:(x,s*x/(x+s*(x-1))) if x+s*(x-1)>0 else (math.nan,math.nan),.001,3)
p.line([(1,-3),(1,3)],color=RED,width=2)
p.curve(lambda x:(x,x/(x-1)),.001,3,color=GRAY,dashes='[4 3] 0')
p.arrow(1.3,.65/1.45,.12,-.0143)
p.save('problem-3c.pdf')

p=Plot((-3,3,-3,3))
for s in [-2,-1,-.4,.4,1,2]:p.curve(lambda t:(s*math.sinh(t),s*math.cosh(t)),-3,3)
for c in [.5,1.5]:
    for sign in [-1,1]:p.curve(lambda t:(sign*c*math.cosh(t),c*math.sinh(t)),-3,3,color=GRAY,dashes='[3 3] 0')
p.line([(0,-3),(0,3)],color=RED,width=2)
p.line([(-3,-3),(3,3)],color=GRAY,dashes='[3 3] 0')
p.line([(-3,3),(3,-3)],color=GRAY,dashes='[3 3] 0')
p.arrow(.6,1.17,.22,.12)
p.save('problem-3d.pdf')
print('Wrote six vector PDF sketches.')
