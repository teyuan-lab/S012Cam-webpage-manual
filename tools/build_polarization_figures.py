"""Original instructional SVG artwork and physical-model plots for the lesson."""
from pathlib import Path
import math,html,unicodedata
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
OUT=Path(__file__).resolve().parents[1]/'assets'/'polarization';OUT.mkdir(exist_ok=True)
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','font.size':13,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'path','svg.hashsalt':'s012cam-optics'})
BLUE='#175da8';GOLD='#b86a06';TEAL='#008679';RED='#c73c53';INK='#182238'
class S:
 def __init__(self,title):self.a=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" role="img"><title>'+html.escape(title)+'</title><defs><marker id="tip" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="context-stroke"/></marker></defs><rect width="800" height="420" rx="20" fill="#f1f6fc"/>']
 def text(self,x,y,t,size=25,color=INK):
  units=sum(1 if unicodedata.east_asian_width(c) in ('W','F') else .53 for c in t);size=min(size,(775-x)/max(1,units));self.a.append(f'<text x="{x}" y="{y}" font-family="Arial,Noto Sans TC,sans-serif" font-size="{size}" fill="{color}">{html.escape(t)}</text>')
 def line(self,x,y,u,v,c=BLUE,w=4,arrow=False,dash=False):self.a.append(f'<path d="M{x} {y}L{u} {v}" fill="none" stroke="{c}" stroke-width="{w}"'+(' marker-end="url(#tip)"' if arrow else '')+(' stroke-dasharray="8 7"' if dash else '')+'/>')
 def rect(self,x,y,w,h,c='#fff'):self.a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{c}" stroke="#b5c7dc" stroke-width="2"/>')
 def circle(self,x,y,r,c=BLUE,fill='none'):self.a.append(f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{c}" stroke-width="3" fill="{fill}"/>')
 def path(self,d,c=BLUE,w=4):self.a.append(f'<path d="{d}" stroke="{c}" stroke-width="{w}" fill="none"/>')
 def save(self,name,lang): (OUT/f'{name}-{lang}.svg').write_text(''.join(self.a)+'</svg>')
for lang in ('en','zh'):
 zh=lang=='zh';T=lambda e,z:z if zh else e
 s=S(T('Electric-field direction and polarization','電場方向與偏振'));s.text(32,43,T('(a) Light travels forward; E oscillates sideways','(a) 光向前傳播；電場 E 橫向振盪'),27)
 s.line(45,160,740,160,INK,3,True)
 points='M'+' L'.join(f'{x:.1f} {160-65*math.sin((x-60)*math.pi/105):.1f}' for x in range(60,700,3));s.path(points)
 for x in [110,215,320,425,530,635]:s.line(x,160,x,160-65*math.sin((x-60)*math.pi/105),BLUE,3,True)
 s.text(630,205,T('Travel k','傳播 k'));s.text(58,84,'E',29,BLUE)
 for x,label,shape in [(135,T('Linear','線偏振'),'line'),(400,T('Circular','圓偏振'),'circle'),(665,T('Elliptical','橢圓偏振'),'ellipse')]:
  s.circle(x,305,53,'#cfdae8')
  if shape=='line':s.line(x-34,339,x+34,271,BLUE,5,True)
  elif shape=='circle':s.circle(x,305,39,TEAL);s.line(x+39,305,x+39,290,TEAL,3,True)
  else:s.a.append(f'<ellipse cx="{x}" cy="305" rx="43" ry="22" transform="rotate(-25 {x} 305)" fill="none" stroke="{RED}" stroke-width="4"/>')
  s.text(x-65,395,{'line':'(b) ','circle':'(c) ','ellipse':'(d) '}[shape]+label,24)
 s.save('field',lang)
 s=S(T('Colour and polarization are independent','顏色與偏振是不同的性質'));s.text(30,44,T('Different wavelengths can have different E directions','不同波長的光，可以有不同的電場方向'),26)
 for y,c,period,angle,lbl in [(120,RED,65,0,T('Red: horizontal','紅光：水平')),(225,TEAL,48,45,T('Green: 45 degrees','綠光：45°')),(330,BLUE,35,90,T('Blue: vertical','藍光：垂直'))]:
  s.path('M'+' L'.join(f'{x} {y-23*math.sin(x*math.pi/period):.1f}' for x in range(35,350,3)),c)
  a=math.radians(angle);s.line(425-40*math.cos(a),y+40*math.sin(a),425+40*math.cos(a),y-40*math.sin(a),c,5,True);s.text(505,y+8,{120:'(a) ',225:'(b) ',330:'(c) '}[y]+lbl,26,c)
 s.text(30,404,T('Illustrative input; not a measurement','示意輸入，並非實際量測'),21);s.save('wavelength',lang)
 s=S(T('Unpolarized and partially polarized light','非偏振光與部分偏振光'));s.text(30,45,T('View along the beam; compare many time samples','沿光束方向看，比較許多時間樣本'),26)
 for x,label,kind in [(140,T('Unpolarized','非偏振'),'random'),(400,T('Partial','部分偏振'),'partial'),(660,T('Linear','線偏振'),'linear')]:
  s.circle(x,200,90,'#b4c8de')
  for i in range(12):
   a=math.radians(i*137.5 if kind=='random' else (i*137.5 if i<4 else 0) if kind=='partial' else 0);r=38+(i%4)*12
   s.line(x-r*math.cos(a),200+r*math.sin(a),x+r*math.cos(a),200-r*math.sin(a),BLUE if i%2 else TEAL,2)
  s.text(x-84,335,{140:'(a) ',400:'(b) ',660:'(c) '}[x]+label,26)
 s.text(32,392,T('Arrows are time samples, not simultaneous fixed axes','箭頭代表不同時間的樣本，不是同時存在的固定軸'),22);s.save('unpolarized',lang)
 s=S(T('Fresnel reflection at Brewster angle','Brewster 角的 Fresnel 反射'))
 n=1.5;a=math.atan(n);t=math.asin(math.sin(a)/n);c=math.cos(a);ct=math.cos(t)
 rs=((c-n*ct)/(c+n*ct))**2;rp=((n*c-ct)/(n*c+ct))**2
 x,y=370,215;r=210;tr=155;ray='#596779'
 s.rect(25,y,750,185,'#edf4f8');s.line(x,40,x,390,'#9aa8b7',1,False,True)
 dx,dy=r*math.sin(a),r*math.cos(a)
 s.line(x-dx,y-dy,x,y,ray,1.5,True);s.line(x,y,x+dx,y-dy,ray,1.5,True);s.line(x,y,x+tr*math.sin(t),y+tr*math.cos(t),ray,1.5,True)
 def field(cx,cy,amp,kind,normal,side):
  size=20*amp
  if kind=='TE':
   s.circle(cx,cy,size,BLUE,'#fff');d=size*.6;s.line(cx-d,cy-d,cx+d,cy+d,BLUE,1);s.line(cx-d,cy+d,cx+d,cy-d,BLUE,1)
  elif size>.001:
   nx,ny=normal;s.line(cx-nx*size,cy-ny*size,cx+nx*size,cy+ny*size,RED,1.4,True);s.line(cx+nx*size,cy+ny*size,cx-nx*size,cy-ny*size,RED,1.4,True)
  s.text(cx+side*(size+9)-(92 if side<0 else 0),cy+(-10 if kind=='TE' else 22),f'{kind} {amp:.2f}',16,BLUE if kind=='TE' else RED)
 field(x-.88*dx,y-.88*dy,1,'TE',(c,-math.sin(a)),-1);field(x-.50*dx,y-.50*dy,1,'TM',(c,-math.sin(a)),-1)
 field(x+.4*dx,y-.4*dy,math.sqrt(rs),'TE',(c,math.sin(a)),1);field(x+.82*dx,y-.82*dy,math.sqrt(rp),'TM',(c,math.sin(a)),1)
 field(x+.38*tr*math.sin(t),y+.38*tr*math.cos(t),2*c/(c+n*ct),'TE',(ct,-math.sin(t)),-1)
 field(x+.8*tr*math.sin(t),y+.8*tr*math.cos(t),2*c/(n*c+ct),'TM',(ct,-math.sin(t)),1)
 s.text(30,35,T('Incident light','入射光'),21);s.text(510,35,T('Reflected light','反射光'),21);s.text(480,380,T('Transmitted light','穿透光'),21)
 s.text(30,408,T('Relative E amplitude · equal incident components · angle 56.3°','相對電場振幅 · 入射兩分量皆為 1 · 入射角 56.3°'),19);s.save('reflection',lang)
 s=S(T('Polarization from Rayleigh scattering','Rayleigh 散射產生偏振'));s.text(30,44,T('At 90 degrees, only the transverse dipole radiates to you','在 90° 方向，只收到橫向偶極的散射光'),25)
 s.line(45,220,370,220,GOLD,6,True);s.circle(400,220,25,BLUE,'#dbeafa');s.line(400,190,400,85,BLUE,5,True)
 s.line(400,145,400,295,RED,4);s.circle(400,220,48,BLUE);s.circle(400,220,5,BLUE,BLUE)
 s.text(40,275,T('Incident sunlight','入射日光'));s.text(455,115,T('Observer at 90 degrees','90° 方向的觀察者'),23)
 s.text(38,345,T('E into/out of page radiates upward','垂直圖面的 E 可向上方輻射'),23,BLUE)
 s.text(38,385,T('E along the viewing direction cannot radiate toward you','沿觀察方向的 E 不向該方向輻射'),23,RED)
 s.line(650,205,650,285,RED,4,True);s.text(570,325,T('Induced E','感應電場'),22,RED)
 s.save('scattering',lang)
 s=S(T('Absorbing sheet polarizer','吸收式片狀偏振片'));s.text(28,42,T('Aligned absorbing chains select an E component','排列整齊的吸收分子，選擇電場分量'),26)
 s.rect(285,80,210,245,'#e3e9f0')
 for x in range(310,480,25):s.line(x,105,x,300,RED,5)
 
 for j in range(7):
  ang=j*math.pi/7;s.line(140-65*math.cos(ang),195-65*math.sin(ang),140+65*math.cos(ang),195+65*math.sin(ang),GOLD,3)
 s.text(60,100,T('Input E','入射 E'));s.circle(140,195,7,INK,'#fff');s.circle(140,195,2,INK,INK);s.circle(630,195,7,INK,'#fff');s.circle(630,195,2,INK,INK);s.text(255,77,T('View along beam: k out of page','沿光束看：k 朝圖面外'),20)
 s.line(525,195,735,195,BLUE,5,True);s.text(540,250,T('E transmitted','通過的 E'),23,BLUE)
 s.text(285,365,T('Absorption axis ↑','吸收軸 ↑'),24,RED);s.text(520,95,T('Transmission axis ↔','穿透軸 ↔'),24,BLUE)
 s.text(35,400,T('Ideal: Iout = Iin / 2 for unpolarized input','理想非偏振入射：Iout = Iin / 2'),21);s.save('sheet',lang)
 s=S(T('Sky polarization geometry','天空偏振的觀察幾何'));s.path('M70 310 A330 250 0 0 1 730 310','#acc6e5',4)
 s.line(400,310,155,140,GOLD,5,True);s.circle(155,140,28,GOLD,'#ffe7aa');s.text(62,95,T('Sun direction','太陽方向'),24)
 s.line(400,310,570,65,BLUE,5,True);s.text(490,45,T('View: 90° from Sun','看離太陽約 90° 的天空'),23)
 s.path('M344 271L385 230L441 271',TEAL,3);s.circle(400,310,16,INK,'#fff');s.line(70,333,730,333,TEAL,4)
 s.text(224,390,T('90 degrees from the Sun, not 90 degrees above the horizon','是離太陽 90°，不是離地平線 90°'),22);s.save('sky',lang)
 s=S(T('LCD and an external analyzer','LCD 與外加分析偏振片'));s.text(30,45,T('An LCD controls light using liquid crystals and polarizers','LCD 利用液晶與偏振片控制光線'),26)
 labels=[T('Backlight','背光'),T('Polarizer','偏振片'),T('Liquid crystal','液晶'),T('Analyzer','分析片')]
 for i,label in enumerate(labels):
  x=60+i*160;s.rect(x,110,110,170,['#fff3cc','#deebf9','#e3f3eb','#deebf9'][i]);s.text(x-6,325,label,21);s.line(x+118,190,x+145,190,GOLD,3,True)
  if i in (1,3):
   for k in range(4):s.line(x+20+k*23,130,x+20+k*23,260,BLUE,3)
  if i==2:
   for k in range(5):s.line(x+25,140+k*24,x+82,145+k*17,TEAL,3)
 s.text(60,385,T('The exiting light is often strongly linearly polarized','離開螢幕的光，通常具有很強的線偏振'),24);s.save('lcd',lang)
 # Scientific plots: explicitly ideal, reproducible formulae.
 th=np.linspace(0,89.8,600);rad=np.radians(th);t=np.arcsin(np.sin(rad)/1.5)
 rs=((np.cos(rad)-1.5*np.cos(t))/(np.cos(rad)+1.5*np.cos(t)))**2
 rp=((1.5*np.cos(rad)-np.cos(t))/(1.5*np.cos(rad)+np.cos(t)))**2
 fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained');ax.plot(th,rs,label='R_TE (TE)',color=BLUE,lw=2.5);ax.plot(th,rp,label='R_TM (TM)',color=RED,lw=2.5);ax.axvline(56.31,color=GOLD,ls='--',label=T('Brewster 56.3°','Brewster 角 56.3°'));ax.set(xlabel=T('Incidence angle from the normal (degrees)','由法線量起的入射角（度）'),ylabel=T('Power reflectance','光強度反射率'),ylim=(0,1),xlim=(0,90));ax.legend();ax.grid(alpha=.15);fig.savefig(OUT/f'fresnel-{lang}.svg');plt.close(fig)
 th=np.linspace(0,180,361);r=np.radians(th);P=np.sin(r)**2/(1+np.cos(r)**2)
 fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained');ax.plot(th,P,color=BLUE,lw=3);ax.set(xlabel=T('Scattering angle (degrees)','散射角（度）'),ylabel=T('Ideal linear polarization degree','理想線偏振度'),ylim=(0,1.05),xlim=(0,180));ax.set_xticks([0,45,90,135,180]);ax.grid(alpha=.2);fig.savefig(OUT/f'rayleigh-{lang}.svg');plt.close(fig)
 fig,ax=plt.subplots(figsize=(8,4.4),layout='constrained');a=np.linspace(0,180,361);ax.plot(a,np.cos(np.radians(a))**2,color=BLUE,lw=3);ax.set(xlabel=T('Angle between E and transmission axis (degrees)','電場與穿透軸的夾角（度）'),ylabel=T('Transmitted intensity / incident intensity','穿透光強度／入射光強度'),xlim=(0,180),ylim=(0,1.05));ax.set_xticks([0,45,90,135,180]);ax.grid(alpha=.2);fig.savefig(OUT/f'malus-{lang}.svg');plt.close(fig)
print('Created 22 bilingual diagrams and physical-model plots.')

for asset in OUT.glob("*.svg"):
 asset.write_text("\n".join(line.rstrip() for line in asset.read_text().splitlines())+"\n")
