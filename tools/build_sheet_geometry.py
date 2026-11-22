"""Project a fixed, checked 3D scene through one camera; labels never define geometry."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,FancyArrowPatch
from matplotlib import font_manager
out=Path(__file__).resolve().parents[1]/'assets/polarization'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','svg.fonttype':'path'})
k=np.array([0.,0,1.]);trans=np.array([1.,0,0]);absorb=np.array([0.,1.,0])
def W(points):
 return np.asarray(points,dtype=float)[...,[1,2,0]]
assert np.dot(k,trans)==np.dot(k,absorb)==np.dot(trans,absorb)==0
assert np.allclose(np.cross(trans,absorb),k)
# Camera basis; W maps local (beam, horizontal, vertical) to world (x,y,z).
view=np.array([-7.,4.,5.]);view/=np.linalg.norm(view)
right=np.cross(absorb,view);right/=np.linalg.norm(right);up=np.cross(view,right)
def project(points):
 p=np.atleast_2d(points);scale=12/(12-p@view)
 return np.column_stack([p@right,p@up])*scale[:,None]
def line(ax,points,c,lw=2,z=1,alpha=1):
 p=project(points);ax.plot(p[:,0],p[:,1],color=c,lw=lw,zorder=z,alpha=alpha,solid_capstyle='round')
def arrow(ax,start,end,c,lw=2,z=7):
 a,b=project([start,end]);ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=11,color=c,lw=lw,zorder=z))
BLUE='#145eae';RED='#c03941';GOLD='#a77817'
for lang in ('en','zh'):
 zh=lang=='zh';T=lambda en,cn:cn if zh else en
 fig=plt.figure(figsize=(12,7.5),facecolor='white');ax=fig.add_axes([.035,.17,.93,.62])
 w=1.22;h=1.4;d=.035
 for x,c,a in [(-d,'#e4e8ee',.7),(d,'#a9b4c1',.27)]:
  pts=project(W([(x,-w,-h),(x,w,-h),(x,w,h),(x,-w,h)]));ax.add_patch(Polygon(pts,facecolor=c,edgecolor='#75869a',lw=.8,alpha=a,zorder=3))
 # Render incident field ribbons in their exact x-z and x-y planes.
 def wave(xs,unit,c,phase,z):
  amplitude=.78*np.sin(5.2*xs+phase);pts=xs[:,None]*k+amplitude[:,None]*unit
  for i in range(0,len(xs)-1,3):
   j=min(i+3,len(xs)-1);verts=project([xs[i]*k,pts[i],pts[j],xs[j]*k]);ax.add_patch(Polygon(verts,facecolor=c,edgecolor='none',alpha=.065,zorder=z-.1))
  line(ax,pts,c,1.5,z)
  for x in np.linspace(xs[0],xs[-1],13):arrow(ax,x*k,x*k+.78*np.sin(5.2*x+phase)*unit,c,.6,z+.1)
 wave(np.linspace(-3.7,-.09,230),absorb,RED,.6,2)
 wave(np.linspace(-3.7,-.09,230),trans,BLUE,0,2.3)
 # Chains run along world y at every position of the x-y film.
 for y in np.linspace(-1.10,1.10,14):line(ax,W([(d,y,-1.3),(d,y,1.3)]),RED,1.1,4,.46)
 # Film edge highlights show physical depth without changing the projection.
 for y in [-w,w]:line(ax,W([(d,y,-h),(d,y,h)]),'#a5b4c5',1.1,4)
 line(ax,W([(d,-w,h),(d,w,h)]),'#657b95',1.1,4)
 wave(np.linspace(.09,3.7,230),trans,BLUE,0,5)
 arrow(ax,-4*k,4.15*k,GOLD,.9,6)
 origin=W([d+.02,-.83,-.98]);arrow(ax,origin,origin+1.7*trans,BLUE,1.5);arrow(ax,origin,origin+1.85*absorb,RED,1.5)
 q=[origin+.23*trans,origin+.23*trans+.23*absorb,origin+.23*absorb];line(ax,q,'#182238',.8,8)
 for point,label,c in [(origin+1.8*trans,'x',BLUE),(origin+1.98*absorb,'y',RED),(4.2*k,'k = z',GOLD)]:
  x,y=project(point)[0];ax.text(x+.03,y,label,color=c,fontsize=12,zorder=10)
 # Axis limits from the entire projected scene; preserve metric scaling and avoid clipping.
 bounds=project(W([[-4.5,0,0],[4.7,0,0],[0,-w,-h],[0,w,h],[0,-w,h],[0,w,-h]]))
 xmin,ymin=bounds.min(axis=0);xmax,ymax=bounds.max(axis=0)
 ax.set(xlim=(xmin-.1,xmax+.35),ylim=(ymin-.32,ymax+.28));ax.set_aspect('equal');ax.axis('off')
 fig.text(.045,.94,T('Linear polarizer · oblique 3D view','線性偏振片・斜向三維觀察'),fontsize=19,color='#182238')
 fig.text(.045,.115,T('Propagation: k ∥ z   |   Film: x–y plane','光行進方向：k ∥ z　｜　偏振片平面：x–y'),fontsize=14,color='#182238')
 fig.text(.045,.075,T('Red: Ey ∥ absorption axis y','紅色：Ey ∥ 吸收軸 y'),fontsize=13,color=RED)
 fig.text(.5,.075,T('Blue: Ex ∥ transmission axis x','藍色：Ex ∥ 穿透軸 x'),fontsize=13,color=BLUE)
 fig.text(.045,.035,'Ex · k = 0     Ey · k = 0     Ex · Ey = 0',fontsize=13,color='#536479')
 fig.savefig(out/f'sheet-orthogonal-3d-v2-{lang}.png',dpi=180);fig.savefig(out/f'sheet-orthogonal-3d-v2-{lang}.svg');plt.close(fig)
print('Verified all pairwise dot products = 0; every object uses one perspective camera.')
