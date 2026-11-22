"""Original orthographic Rayleigh diagrams; incident propagation is +z.

Ideal isotropic electric dipole, single scattering, no molecular depolarization.
Surface radius encodes intensity (not field amplitude). No external art is used.
"""
from pathlib import Path
from math import sin, cos, pi, sqrt
from html import escape
OUT=Path(__file__).resolve().parents[1]/'assets/polarization'
BLUE='#175da8'; INK='#141c27'
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,k):return tuple(x*k for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def radiation(n,d=None):return 1-dot(n,d)**2 if d else (1+n[2]**2)/2
RIGHT=(-.6,0,.8);UP=(-.273616,.939693,-.205212);DEPTH=(-.751754,-.342020,-.563816)
def project(p,c,scale):return (c[0]+scale*dot(p,RIGHT),c[1]-scale*dot(p,UP))
class SVG:
 def __init__(self,w,h,title):
  self.w=w;self.h=h;self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><defs><marker id="black" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="black"/></marker><marker id="blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{BLUE}"/></marker></defs><rect width="{w}" height="{h}" fill="white"/>']
 def text(self,x,y,t,size=19,color=INK,anchor='start'):
  self.a.append(f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" text-anchor="{anchor}" font-family="Arial, Noto Sans TC, sans-serif">{escape(t)}</text>')
 def line(self,a,b,color=INK,w=1.2,arrow=False,double=False,dash=False):
  marker='blue' if color==BLUE else 'black'
  self.a.append(f'<path d="M{a[0]:.2f} {a[1]:.2f}L{b[0]:.2f} {b[1]:.2f}" fill="none" stroke="{color}" stroke-width="{w}"'+(f' marker-end="url(#{marker})"' if arrow or double else '')+(f' marker-start="url(#{marker})"' if double else '')+(' stroke-dasharray="5 5"' if dash else '')+'/>')
 def circle(self,p,r,fill):self.a.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r}" fill="{fill}"/>')
 def poly(self,points,fill,stroke='#94a3b8',width=.6):
  self.a.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
 def path(self,points,color,w=1.5):
  self.a.append('<path d="'+' '.join(('M' if i==0 else 'L')+f'{x:.2f} {y:.2f}' for i,(x,y) in enumerate(points))+f'" fill="none" stroke="{color}" stroke-width="{w}"/>')
 def save(self,name):
  (OUT/name).write_text(''.join(self.a)+'</svg>\n')

def geometry(lang):
 zh=lang=='zh';T=lambda en,cn:cn if zh else en
 s=SVG(1100,700,T('Rayleigh scattering: transverse fields and observation angle','Rayleigh 散射：橫向電場與觀察方向'))
 s.text(30,36,T('(a) Incident light along +z; electric fields perpendicular to each ray','(a) 入射光沿 +z；各電場均垂直於各自的光線'),23)
 c=(470,320);scale=112;P=lambda v:project(v,c,scale)
 # A translucent y-z scattering plane. x is perpendicular to this plane.
 s.poly([P(v) for v in [(0,0,-.4),(0,2.2,-.4),(0,2.2,3.4),(0,0,3.4)]],'#f1f5f9','#dbe3ec')
 s.text(685,85,T('Scattering plane: y–z','散射面：y–z'),18)
 for endpoint,label in [((1.2,0,0),'x'),((0,2.45,0),'y'),((0,0,4),'z · kᵢₙ')]:
  s.line(P((0,0,0)),P(endpoint),'black',1.1,True);p=P(endpoint);s.text(p[0]+10,p[1]+(15 if label.startswith('z') else -5),label,19,'black')
 s.line(P((0,0,-4.1)),P((0,0,-.1)),'black',1.6,True)
 s.circle(c,7,BLUE);s.text(c[0]+14,c[1]+45,T('Molecule','分子／粒子'),18)
 # Incoherent time samples projected to each transverse plane, not a coherent ellipse.
 def sample(n,pos,size):
  p=P(pos)
  for j in range(8):
   a=j*pi/8;e=(cos(a),sin(a),0);es=add(e,mul(n,-dot(n,e)))
   if dot(es,es)<1e-10:continue
   delta=(scale*size*dot(es,RIGHT),-scale*size*dot(es,UP))
   s.line((p[0]-delta[0],p[1]-delta[1]),(p[0]+delta[0],p[1]+delta[1]),BLUE,1.4)
  s.circle(p,2.5,BLUE)
 sample((0,0,1),(0,0,-2.8),.43)
 s.text(28,125,T('Unpolarized input','非偏振入射光'),20)
 s.text(28,151,T('Eₓ and Eᵧ: equal mean intensity','Eₓ、Eᵧ 平均強度相同'),17,BLUE)
 for angle,length in [(0,3.25),(45,2.65),(90,1.85)]:
  a=angle*pi/180;n=(0,sin(a),cos(a));end=mul(n,length)
  s.line(P((0,0,0)),P(mul(n,length+.55)),'black',1.5,True)
  sample(n,end,.45)
  p=P(end)
  if angle==0:
   s.text(p[0]+70,p[1]-35,'Θ = 0°',20)
   s.text(p[0]+70,p[1]-9,T('DoLP = 0','DoLP = 0'),18,BLUE)
  elif angle==45:
   s.text(p[0]+40,p[1]-18,'Θ = 45°',20)
   s.text(p[0]+40,p[1]+8,'DoLP = 1/3',18,BLUE)
  else:
   s.text(p[0]-185,p[1]-10,'Θ = 90°',20)
   s.text(p[0]-185,p[1]+16,T('Only Eₓ remains','只留下 Eₓ'),18,BLUE)
 # Angle is defined between +z and scattered k.
 s.path([P((0,.8*sin(a*pi/180),.8*cos(a*pi/180))) for a in range(46)],'black',1)
 p=P((0,.52,.95));s.text(p[0]+8,p[1],'Θ',21,'black')
 s.text(30,426,T('Blue lines: field samples at different times, not simultaneous fixed vectors.','藍線為不同時間的電場樣本，不是同時存在的固定向量。'),18,BLUE)
 s.text(30,476,T('(b) Two independent input components; amplitudes at a common distance','(b) 兩個互不相干的入射分量；比較同一距離的散射場振幅'),22)
 for i,angle in enumerate([0,45,90]):
  x=180+i*365;y=558;ratio=cos(angle*pi/180)
  s.text(x,512,f'Θ = {angle}°',20,INK,'middle')
  s.line((x-48,y),(x+48,y),BLUE,2.6, double=True)
  if ratio>1e-8:s.line((x,y-48*ratio),(x,y+48*ratio),BLUE,2.2,double=True)
  s.text(x-88,622,'Eₓ: 1',18,BLUE)
  s.text(x+8,622,f'E∥: {ratio:.2f}',18,BLUE)
 s.text(550,667,T('Eₓ ⟂ (y–z); E∥ lies in the scattering plane and is perpendicular to kₛ.','Eₓ 垂直 y–z 散射面；E∥ 位於散射面內，且垂直散射方向 kₛ。'),18,INK,'middle')
 s.save(f'scattering-directions-v2-{lang}.svg')

def patterns(lang):
 zh=lang=='zh';T=lambda en,cn:cn if zh else en
 s=SVG(1100,900,T('Dipole radiation and unpolarized Rayleigh phase function','偶極輻射與非偏振光的 Rayleigh 角分布'))
 cases=[((275,235),(0,1,0),'(a) '+T('Dipole along y','偶極沿 y'),'Iᵧ(n) ∝ 1 − nᵧ²'),((825,235),(1,0,0),'(b) '+T('Dipole along x','偶極沿 x'),'Iₓ(n) ∝ 1 − nₓ²'),((275,655),None,'(c) '+T('Equal incoherent average','等強度、不相干平均'),'I(Θ) ∝ (1 + cos²Θ) / 2')]
 for centre,d,title,formula in cases:
  cx,cy=centre;s.text(cx,cy-190,title,23,INK,'middle')
  def point(theta,phi):
   n=(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta))
   intensity=radiation(n,d)
   return mul(n,intensity)
  quads=[]
  nt,np=28,56
  for i in range(nt):
   for j in range(np):
    vs=[point(t*pi/nt,p*2*pi/np) for t,p in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]]
    quads.append((sum(dot(v,DEPTH) for v in vs)/4,vs))
  for depth,vs in sorted(quads,key=lambda p:p[0]):
   shade=max(0,min(1,(depth+1)/2));b=int(243-35*shade);r=int(236-57*shade);g=int(243-42*shade)
   s.poly([project(v,centre,125) for v in vs],f'#{r:02x}{g:02x}{b:02x}','#71869a',.45)
  for v,label in [((1.43,0,0),'x'),((0,1.43,0),'y'),((0,0,1.43),'z')]:
   p=project(v,centre,125);s.line(centre,p,'black',1.1,True);s.text(p[0]+8,p[1]-5,label,18,'black')
  if d:
   s.line(project(mul(d,-1.2),centre,125),project(mul(d,1.2),centre,125),BLUE,2,double=True)
   p=project(mul(d,1.25),centre,125);s.text(p[0]-10,p[1]-12,'Eᵢₙ',18,BLUE,'end')
  s.text(cx,cy+160,formula,21,BLUE,'middle')
  s.text(cx,cy+187,T('Null along the dipole axis' if d else 'Maximum along ±z; half as strong at 90°','沿偶極軸方向為零' if d else '沿 ±z 最強；90° 方向為其一半'),17,INK,'middle')
 s.text(825,465,T('(d) Scattering angle and polarization','(d) 散射角與偏振'),23,INK,'middle')
 x0,y0=625,735;w,h=410,220
 X=lambda a:x0+w*a/180;Y=lambda i:y0-h*i
 for v in [0,.5,1]:
  s.line((x0,Y(v)),(x0+w,Y(v)),'#dce3eb',.8);s.text(x0-12,Y(v)+5,str(v),17,INK,'end')
 for a in [0,45,90,135,180]:s.text(X(a),y0+28,str(a)+'°',17,INK,'middle')
 s.line((x0,y0-h),(x0,y0),'black',1.2);s.line((x0,y0),(x0+w,y0),'black',1.2)
 s.path([(X(a),Y(sin(a*pi/180)**2/(1+cos(a*pi/180)**2))) for a in range(181)],BLUE,2.8)
 s.path([(X(a),Y((1+cos(a*pi/180)**2)/2)) for a in range(181)],'#606974',2)
 s.circle((X(90),Y(1)),4,BLUE);s.circle((X(90),Y(.5)),4,'#606974')
 s.text(825,790,T('Scattering angle Θ (from +z)','散射角 Θ（由 +z 量起）'),19,INK,'middle')
 s.line((650,817),(690,817),BLUE,2.8);s.text(700,823,'DoLP = sin²Θ / (1 + cos²Θ)',18,BLUE)
 s.line((650,848),(690,848),'#606974',2);s.text(700,854,T('Intensity / forward intensity','光強度／前向光強度'),18,'#606974')
 s.text(550,890,T('Surface radius = relative intensity, not E amplitude; all three surfaces use the same radial scale.','曲面半徑表示相對光強度，不是電場振幅；三個立體圖使用相同徑向尺度。'),18,INK,'middle')
 s.save(f'rayleigh-dipoles-v2-{lang}.svg')

if __name__=='__main__':
 for lang in ('en','zh'):geometry(lang);patterns(lang)
 print('Built four original bilingual Rayleigh SVGs.')
