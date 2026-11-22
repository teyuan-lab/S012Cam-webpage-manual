"""Original sky-dome field calculated from single-scattering Rayleigh geometry."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
out=Path(__file__).resolve().parents[1]/'assets/polarization'
font_manager.fontManager.addfont('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
plt.rcParams.update({'font.family':'Arial Unicode MS','svg.fonttype':'path','font.size':13})
s=np.array([np.cos(np.radians(15)),0,np.sin(np.radians(15))])
for lang in ('en','zh'):
 zh=lang=='zh';T=lambda en,cn:cn if zh else en
 fig=plt.figure(figsize=(10,7.2),facecolor='white');ax=fig.add_subplot(projection='3d',computed_zorder=False)
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
   ax.plot(v[:,0],v[:,1],v[:,2],color='#132b43' if front else '#8295a8',alpha=1 if front else .38,lw=2.3 if front else 1.1,zorder=4 if front else 1.5)
 u=np.array([0,1,0]);v=np.cross(s,u);a=np.linspace(0,np.pi,180);band=u[:,None]*np.cos(a)+v[:,None]*np.sin(a)
 ax.plot(*band,color='#1675b6',lw=2,zorder=3)
 ax.scatter(*s,s=140,color='#db4f36',edgecolors='white',linewidth=1,zorder=8)
 ax.text(*(s+np.array([.07,.02,.03])),T('Sun','太陽'),fontsize=17,color='#ba3926',zorder=10)
 # Observer centred at the origin: head, torso, arms and legs share world coordinates.
 uhead,vhead=np.meshgrid(np.linspace(0,2*np.pi,20),np.linspace(0,np.pi,14))
 ax.plot_surface(.035*np.cos(uhead)*np.sin(vhead),.035*np.sin(uhead)*np.sin(vhead),.035*np.cos(vhead)+.055,color='#243548',linewidth=0,zorder=12)
 for points in [([0,0,.02],[0,0,-.085]),([0,0,-.015],[0,-.075,-.06]),([0,0,-.015],[0,.075,-.06]),([0,0,-.085],[0,-.045,-.17]),([0,0,-.085],[0,.045,-.17])]:
  q=np.array(points);ax.plot(q[:,0],q[:,1],q[:,2],color='#243548',lw=3,solid_capstyle='round',zorder=12)
 ax.text(0,-.10,-.19,T('Observer','觀察者'),fontsize=13,color='#243548',zorder=15)
 ax.view_init(elev=24,azim=-45);ax.set(xlim=(-1.1,1.1),ylim=(-1.1,1.1),zlim=(-.24,1.12));ax.set_box_aspect((2,2,1.36),zoom=1.48);ax.set_axis_off();ax.dist=8
 fig.text(.055,.94,T('Polarization directions across the sky','天空穹頂上的偏振方向'),size=23,weight='bold',color='#182238')
 fig.text(.055,.875,T('Short black strokes = local electric-field axis','黑色短線＝該方向天空光的電場軸向'),size=15,color='#182238')
 fig.text(.055,.83,T('Blue arc = 90° from the Sun, strongest ideal linear polarization','藍色弧線＝距太陽 90°，理想線偏振最強'),size=14,color='#1675b6')
 fig.text(.055,.075,T('Single-scattering model · stroke length scales with DoLP','單次散射模型 · 短線長度隨 DoLP 改變'),size=13,color='#536479')
 fig.text(.055,.035,T('Each stroke is tangent to the dome and perpendicular to the local scattering plane.','每條短線沿穹頂切向，且垂直於該處的散射面。'),size=12,color='#536479')
 ax.set_position([.03,.09,.94,.76]);fig.savefig(out/f'sky-dome-{lang}.svg');fig.savefig(out/f'sky-dome-{lang}.png',dpi=170);plt.close(fig)
print('Sky dome: E ∝ Sun × view; stroke length ∝ (1 − cos²Θ)/(1 + cos²Θ).')
