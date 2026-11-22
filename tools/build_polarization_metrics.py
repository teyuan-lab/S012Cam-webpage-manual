"""Original AoLP / DoLP teaching examples; intensity units are arbitrary."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Arc
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','svg.fonttype':'path','svg.hashsalt':'s012cam-metrics'})
out=Path(__file__).resolve().parents[1]/'assets/polarization'
for lang in ['en','zh']:
 T=lambda en,cn:cn if lang=='zh' else en
 fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
 for i,(ax,deg) in enumerate(zip(axes,[0,45,90])):
  a=np.radians(deg);ax.set(xlim=(-1.3,1.5),ylim=(-1.2,1.5),aspect='equal');ax.axis('off')
  ax.annotate('',xy=(1.2,0),xytext=(-1.15,0),arrowprops={'arrowstyle':'->','color':'#9aa8b7','lw':1})
  ax.annotate('',xy=(0,1.15),xytext=(0,-1.1),arrowprops={'arrowstyle':'->','color':'#9aa8b7','lw':1})
  ax.annotate('',xy=(np.cos(a),np.sin(a)),xytext=(-np.cos(a),-np.sin(a)),arrowprops={'arrowstyle':'<->','color':'#175da8','lw':2})
  if deg:ax.add_patch(Arc((0,0),.8,.8,theta1=0,theta2=deg,color='#b36b20',lw=1))
  ax.set_title(f'({chr(97+i)}) AoLP = {deg}°',fontsize=16,pad=12)
  ax.text(.4,-.3,T('0° reference','0° 基準'),fontsize=11,color='#637184')
 fig.savefig(out/f'aolp-examples-{lang}.svg');fig.savefig(out/f'aolp-examples-{lang}.png',dpi=150);plt.close(fig)
 fig,axes=plt.subplots(1,3,figsize=(12,3.7),layout='constrained');alpha=np.linspace(0,180,361)
 for i,(ax,dolp) in enumerate(zip(axes,[0,.5,1])):
  intensity=50*(1+dolp*np.cos(2*np.radians(alpha-30)))
  ax.plot(alpha,intensity,color='#175da8',lw=1.6);ax.set(xlim=(0,180),ylim=(-4,107),xticks=[0,45,90,135,180],yticks=[0,25,50,75,100],xlabel=T('Analyzer angle α (°)','分析片角度 α (°)'))
  ax.set_title(f'({chr(97+i)}) DoLP = {dolp:g}',fontsize=16);ax.grid(alpha=.2)
  ax.spines[['top','right']].set_visible(False)
  if i==0:ax.set_ylabel(T('Transmitted intensity (a.u.)','穿透光強度（任意單位）'))
  ax.text(.04,.93,T(f'Imax = {50*(1+dolp):g}\nImin = {50*(1-dolp):g}',f'Imax = {50*(1+dolp):g}\nImin = {50*(1-dolp):g}'),transform=ax.transAxes,fontsize=10,va='top',bbox={'facecolor':'white','edgecolor':'none','alpha':.85})
 fig.savefig(out/f'dolp-examples-{lang}.svg');fig.savefig(out/f'dolp-examples-{lang}.png',dpi=150);plt.close(fig)
for p in out.glob('*examples-*.svg'):p.write_text('\n'.join(l.rstrip() for l in p.read_text().splitlines())+'\n')
print('AoLP: axis examples; DoLP: I(alpha)=50[1+D cos 2(alpha−30°)].')
