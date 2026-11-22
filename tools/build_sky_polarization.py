"""Original sky-dome field calculated from single-scattering Rayleigh geometry."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
out=Path(__file__).resolve().parents[1]/'assets/polarization'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','svg.fonttype':'path','font.size':13})
for lang in ('en','zh'):
 for panel,height in enumerate([15,45,75]):
  s=np.array([np.cos(np.radians(height)),0,np.sin(np.radians(height))])
  zh=lang=='zh';T=lambda en,cn:cn if zh else en
  fig=plt.figure(figsize=(7,6),facecolor='white');ax=fig.add_subplot(projection='3d',computed_zorder=False)
  az,el=np.meshgrid(np.linspace(0,2*np.pi,100),np.linspace(0,np.pi/2,45))
  x=np.cos(el)*np.cos(az);y=np.cos(el)*np.sin(az);z=np.sin(el)
  ax.plot_surface(x,y,z,color='#d8eafb',alpha=.2,linewidth=0,shade=True,zorder=0)
  for elev in [0,20,40,60,80]:
   a=np.linspace(0,2*np.pi,200);e=np.radians(elev);ax.plot(np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.full_like(a,np.sin(e)),color='#a9bacb',lw=.65,zorder=1)
  for azim in np.arange(0,360,30):
   e=np.linspace(0,np.pi/2,90);a=np.radians(azim);ax.plot(np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e),color='#bdc9d5',lw=.6,zorder=1)
  camera=np.array([np.cos(np.radians(24))*np.cos(np.radians(-45)),np.cos(np.radians(24))*np.sin(np.radians(-45)),np.sin(np.radians(24))])
  for ed in range(6,86,10):
   for ad in range(0,360,15):
    e,a=np.radians([ed,ad]);r=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    electric=np.cross(s,r);n=np.linalg.norm(electric)
    if n<1e-8:continue
    electric/=n;mu=np.dot(s,r);p=(1-mu*mu)/(1+mu*mu)
    if p<.035:continue
    d=.065*p;ends=[r*np.cos(d)+electric*np.sin(d),r*np.cos(d)-electric*np.sin(d)];v=np.array(ends)
    front=np.dot(r,camera)>0
    ax.plot(v[:,0],v[:,1],v[:,2],color='#175da8' if front else '#8eaed0',alpha=1 if front else .38,lw=2.3 if front else 1.1,zorder=4 if front else 1.5)
  u=np.array([0,1,0]);v=np.cross(s,u);a=np.linspace(0,np.pi,180);band=u[:,None]*np.cos(a)+v[:,None]*np.sin(a)
  # The upper half-disc is perpendicular to the observer-to-Sun vector s.
  # Its diameter passes through the observer and its rim is 90 degrees from the Sun.
  assert np.max(np.abs(s @ band)) < 1e-12
  assert np.min(band[2]) >= -1e-12
  vertices=np.vstack((np.zeros(3),band.T,np.zeros(3)))
  plane=Poly3DCollection([vertices],facecolor='#e4ac47',edgecolor='none',alpha=.26,zorder=2)
  ax.add_collection3d(plane)
  ax.plot(*band,color='#1675b6',lw=2,zorder=3)
  ax.plot([0,0],[-1,1],[0,0],color='#b3842c',lw=1,alpha=.7,zorder=3)
  ax.quiver(0,0,0,*(s*.94),color='black',linewidth=1.5,arrow_length_ratio=.12,zorder=9)
  ax.text(*(s*.53+np.array([.02,.06,.04])),T('normal n','法向量 n'),fontsize=12,color='black',zorder=10)

  ax.scatter(*s,s=140,color='#db4f36',edgecolors='white',linewidth=1,zorder=8)
  ax.text(*(s+np.array([.07,.02,.03])),T('Sun','太陽'),fontsize=17,color='#ba3926',zorder=10)
  # Observer centred at the origin: head, torso, arms and legs share world coordinates.
  uhead,vhead=np.meshgrid(np.linspace(0,2*np.pi,20),np.linspace(0,np.pi,14))
  ax.plot_surface(.035*np.cos(uhead)*np.sin(vhead),.035*np.sin(uhead)*np.sin(vhead),.035*np.cos(vhead)+.055,color='#243548',linewidth=0,zorder=12)
  for points in [([0,0,.02],[0,0,-.085]),([0,0,-.015],[0,-.075,-.06]),([0,0,-.015],[0,.075,-.06]),([0,0,-.085],[0,-.045,-.17]),([0,0,-.085],[0,.045,-.17])]:
   q=np.array(points);ax.plot(q[:,0],q[:,1],q[:,2],color='#243548',lw=3,solid_capstyle='round',zorder=12)
  ax.text(0,-.10,-.19,T('Observer','觀察者'),fontsize=13,color='#243548',zorder=15)
  ax.view_init(elev=24,azim=-45);ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),zlim=(-.24,1.12));ax.set_box_aspect((2,2,1.36),zoom=1.38);ax.set_axis_off();ax.dist=8
  fig.text(.06,.93,f'({chr(97+panel)}) '+T(f'Sun elevation {height}°',f'太陽高度 {height}°'),size=20,color='#182238')
  ax.set_position([.03,.04,.94,.83]);fig.savefig(out/f'sky-dome-sun{height}-{lang}.svg');fig.savefig(out/f'sky-dome-sun{height}-{lang}.png',dpi=170);plt.close(fig)
print("Rendered three solar elevations with E perpendicular to both Sun and view directions.")

for asset in out.glob("sky-dome-sun*.svg"):
 asset.write_text("\n".join(line.rstrip() for line in asset.read_text().splitlines())+"\n")
