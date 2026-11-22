"""Normally-white TN LCD: a single checked 3D camera and Cartesian scene."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,FancyArrowPatch
from matplotlib import font_manager
OUT=Path(__file__).resolve().parents[1]/'assets/polarization'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','svg.fonttype':'path'})
k=np.array([0.,0,1.]);X=np.array([1.,0,0]);Y=np.array([0.,1.,0])
assert np.dot(X,k)==np.dot(Y,k)==np.dot(X,Y)==0
view=np.array([-7.,4.,5.]);view/=np.linalg.norm(view);right=np.cross(Y,view);right/=np.linalg.norm(right);up=np.cross(view,right)
def P(q):
 q=np.atleast_2d(q);return np.column_stack((q@right,q@up))*14/(14-q@view)[:,None]
def line(ax,q,c,lw=1,z=1,alpha=1):
 p=P(q);ax.plot(*p.T,c=c,lw=lw,zorder=z,alpha=alpha,solid_capstyle='round')
def arrow(ax,a,b,c,lw=1,z=10):
 a,b=P([a,b]);ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=10,color=c,lw=lw,zorder=z))
def plane(ax,z,colour,alpha=.6,width=.82,height=.92,depth=3):
 for dz in [-.025,.025]:
  q=P([[-width,-height,z+dz],[width,-height,z+dz],[width,height,z+dz],[-width,height,z+dz]])
  ax.add_patch(Polygon(q,facecolor=colour,edgecolor='#8b9eaf',lw=.8,alpha=alpha,zorder=depth))
def rod(ax,centre,direction,length=.24):
 assert np.isclose(np.linalg.norm(direction),1)
 line(ax,[centre-direction*length/2,centre+direction*length/2],'#177c86',3,6)
 # thin highlight gives volume without moving the centreline
 line(ax,[centre-direction*length/2+X*.015,centre+direction*length/2+X*.015],'#94cdd1',.65,6.1)
def draw(ax,on):
 # Backlight, rear analyzer and front analyzer are ALL parallel x-y planes.
 plane(ax,-4.1,'#fff4cc',.95,depth=1);plane(ax,-2.7,'#a5afbe',.45,depth=2)
 # Crossed transmission axes, drawn on the actual surfaces: rear y, front x.
 rear=np.array([-.5,-.62,-2.66]);arrow(ax,rear,rear+Y*1.18,'#000000',1.8,4)
 px,py=P(rear+Y*1.35)[0];ax.text(px,py,'y',color='#000000',fontsize=11,zorder=8)
 # The LC cell is a rectangular transparent volume; directors vary THROUGH z.
 low=-1.55;high=1.55;w=.74;h=.83
 faces=[[[x,-h,low],[x,h,low],[x,h,high],[x,-h,high]] for x in [-w,w]]+[[[-w,y,low],[w,y,low],[w,y,high],[-w,y,high]] for y in [-h,h]]
 for q in faces:ax.add_patch(Polygon(P(q),facecolor='#d7eef1',edgecolor='#a4c4cc',lw=.7,alpha=.16,zorder=3))
 for z in np.linspace(-1.35,1.35,9):
  theta=(z+1.35)/2.7*np.pi/2;d=k if on else np.cos(theta)*Y+np.sin(theta)*X
  for x,y in [(-.3,-.36),(.3,.28)]:rod(ax,np.array([x,y,z]),d)
 plane(ax,2.7,'#a5afbe',.52,depth=7)
 front=np.array([-.6,-.52,2.74]);arrow(ax,front,front+X*1.25,'#000000',1.8,8)
 px,py=P(front+X*1.38)[0];ax.text(px,py,'x',color='#000000',fontsize=11,zorder=8)
 # Blue optical E has no z component, even when the molecular director is along z.
 zz=np.linspace(-2.6,2.61,430);t=np.clip((zz-low)/(high-low),0,1)*np.pi/2
 dirs=np.tile(Y,(len(zz),1)) if on else np.cos(t)[:,None]*Y+np.sin(t)[:,None]*X
 assert np.allclose(dirs@k,0)
 pts=zz[:,None]*k+.49*np.sin(5.8*zz)[:,None]*dirs
 line(ax,pts,'#145eae',1.35,6.5)
 for z in np.linspace(-2.5,2.5,15):
  theta=np.clip((z-low)/(high-low),0,1)*np.pi/2;d=Y if on else np.cos(theta)*Y+np.sin(theta)*X
  arrow(ax,z*k,z*k+.49*np.sin(5.8*z)*d,'#145eae',.55,6.6)
 if not on:
  zz=np.linspace(2.81,4.1,100);line(ax,zz[:,None]*k+.49*np.sin(5.8*zz)[:,None]*X,'#145eae',1.35,9)
 else:
  hit=P([0,0,2.74])[0];ax.plot(*hit,marker='x',color='#b62d3c',ms=9,mew=1.8,zorder=10)
 # An output viewing swatch, separated from the optics (not a fifth polarizer).
 # No extra optical plate: a transmitted wave or the red stop marks the output.
 arrow(ax,-4.65*k,(2.62 if on else 4.0)*k,'#000000',.85,11)
 for i,z in enumerate([-4.1,-2.7,0,2.7]):
  p=P([0,-1.04,z])[0];ax.text(*p,str(i+1),ha='center',va='top',fontsize=12,color='#182238',zorder=12,bbox={'facecolor':'white','edgecolor':'none','pad':1})
 bounds=P([[x,y,z] for x in [-1.1,1.1] for y in [-1.2,1.25] for z in [-4.9,4.9]])
 ax.set(xlim=(bounds[:,0].min()-.12,bounds[:,0].max()+.18),ylim=(bounds[:,1].min()-.25,bounds[:,1].max()+.15));ax.set_aspect('equal');ax.axis('off')
for lang in ['en','zh']:
 T=lambda en,cn:cn if lang=='zh' else en
 fig=plt.figure(figsize=(13,9.5),facecolor='white')
 fig.text(.04,.955,T('Normally-white TN LCD · consistent 3D projection','常白型 TN LCD・一致的三維投影'),fontsize=21,color='#182238')
 for i,on in enumerate([False,True]):
  ax=fig.add_axes([.025,.535-i*.40,.95,.345]);draw(ax,on)
  fig.text(.04,.90-i*.40,T('(b) Voltage ON: E remains along y; crossed front analyzer blocks it.' if on else '(a) Voltage OFF: E rotates from y to x; front analyzer passes it.','(b) 加電壓：電場維持 y 方向，被前分析片擋住，呈暗。' if on else '(a) 未加電壓：電場由 y 轉至 x，通過前分析片，呈亮。'),fontsize=14,color='#182238')
 labels=[T('1  LED backlight','1  LED 背光'),T('2  Rear: transmission y','2  後偏振片：穿透軸 y'),T('3  TN liquid crystal','3  TN 液晶層'),T('4  Front: transmission x','4  前分析片：穿透軸 x')]
 for x,label in zip([.04,.25,.52,.73],labels):fig.text(x,.065,label,fontsize=12,color='#182238')
 fig.text(.04,.025,T('k ∥ z · all film faces lie in x–y · optical E ⊥ k · OFF: director twists by 90°; ON: director ∥ z','k ∥ z・各膜面位於 x–y・光電場 E ⊥ k・未加電壓時分子扭轉 90°；加電壓時分子沿 z'),fontsize=11,color='#536479')
 fig.savefig(OUT/f'tn-lcd-geometry-v2-{lang}.png',dpi=170);fig.savefig(OUT/f'tn-lcd-geometry-v2-{lang}.svg');plt.close(fig)
print('TN checks passed: k=z, rear axis=y, front axis=x; all optical E dot k = 0.')
