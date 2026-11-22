/* Original teaching models: ideal RGB analyzer, statistical field samples, linear projection. */
function lessonProjection(p) {
  // Orthonormal camera basis: view=(-7,-4,5)/sqrt(90).
  const rx=5/Math.sqrt(74),rz=7/Math.sqrt(74),vy=-4/Math.sqrt(90);
  const ux=vy*rz,uy=Math.sqrt(74/90),uz=-vy*rx;
  return [90+130*(p[0]*rx+p[2]*rz),300-130*(p[0]*ux+p[1]*uy+p[2]*uz)];
}
function sheetProjection(alpha) {
  const a=alpha*Math.PI/180,t=[Math.cos(a),Math.sin(a),0],gain=Math.sin(a);
  return {axis:t,e:[gain*t[0],gain*t[1],0],amplitude:Math.abs(gain),intensity:gain*gain};
}
function statisticalFieldSample(kind,random,frame) {
  const x=Math.cos(2*Math.PI*random()),y=Math.cos(2*Math.PI*random());
  return kind===0?[x,y]:kind===1?[Math.sqrt(1.6)*x,Math.sqrt(.4)*y]:[Math.SQRT2*Math.cos(frame*.65),0];
}
document.querySelectorAll('[data-projector-demo]').forEach(demo=>{
  const zh=demo.dataset.lang==='zh',T=(en,cn)=>zh?cn:en,slider=demo.querySelector('[data-projector-slider]');
  const update=()=>{
    const angle=Number(slider.value),a=angle*Math.PI/180,rb=Math.sin(a)**2,g=Math.cos(a)**2;
    const srgb=v=>Math.round(255*(v<=.0031308?12.92*v:1.055*v**(1/2.4)-.055));
    let art='<defs><marker id="projector-e" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#175da8"/></marker></defs><rect width="900" height="420" fill="white"/><rect x="20" y="70" width="135" height="280" rx="18" fill="#edf1f6" stroke="#000" stroke-width="1"/><text x="88" y="190" text-anchor="middle" font-size="24">LCD</text><text x="88" y="222" text-anchor="middle">'+T('projector','投影機')+'</text>';
    for(const [i,color,label,vertical] of [[0,'#c83e45','R',true],[1,'#18803a','G',false],[2,'#3355db','B',true]]) {
      const y=105+i*100;art+=`<path d="M155 ${y}H540" stroke="${color}" stroke-opacity=".2" stroke-width="40"/><text x="180" y="${y-27}" fill="${color}" font-size="23">${label}</text><path d="M${vertical?325:290} ${vertical?y-30:y}L${vertical?325:360} ${vertical?y+30:y}" stroke="#175da8" stroke-width="3" marker-start="url(#projector-e)" marker-end="url(#projector-e)"/><text x="380" y="${y+7}" fill="#175da8">E ∥ ${vertical?'y':'x'}</text>`;
    }
    art+='<rect x="540" y="58" width="22" height="305" fill="#c8d2de" fill-opacity=".6" stroke="#000"/>';
    const tx=45*Math.cos(a),ty=-45*Math.sin(a);art+=`<path d="M${600-tx} ${210-ty}L${600+tx} ${210+ty}" stroke="black" stroke-width="2"/><text x="600" y="105" text-anchor="middle">${T('Analyzer T','分析片 T')}</text><text x="600" y="325" text-anchor="middle">α ${angle}°</text><rect x="690" y="100" width="175" height="220" rx="12" fill="rgb(${srgb(rb)},${srgb(g)},${srgb(rb)})" stroke="black"/><text x="778" y="360" text-anchor="middle">${T('Transmitted RGB','穿透 RGB 混色')}</text><path d="M70 388H150M70 388V365" stroke="black"/><text x="158" y="393">x</text><text x="63" y="356">y</text>`;
    demo.querySelector('[data-projector-scene]').innerHTML=art;
    demo.querySelector('[data-projector-angle]').textContent=angle+'°';
    demo.querySelector('[data-projector-reading]').textContent=T(`Relative transmission: R ${(rb*100).toFixed(0)}%, G ${(g*100).toFixed(0)}%, B ${(rb*100).toFixed(0)}%. Rotate by 90° to swap green and magenta.`,`相對穿透強度：R ${(rb*100).toFixed(0)}%、G ${(g*100).toFixed(0)}%、B ${(rb*100).toFixed(0)}%。旋轉 90°，可比較偏綠與偏洋紅的混色。`);
  };
  slider.addEventListener('input',update);update();
});
document.querySelectorAll('[data-statistical-demo]').forEach(demo=>{
  const zh=demo.dataset.lang==='zh',T=(en,cn)=>zh?cn:en,play=demo.querySelector('[data-stat-play]');
  let seed=123456789,count=0,visible=false,running=!window.matchMedia('(prefers-reduced-motion: reduce)').matches,last=0,frame=0;
  const random=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)/4294967296;};
  const samples=[[],[],[]],targets=[0,.6,1];
  const advance=()=>{for(let i=0;i<3;i++){samples[i].push(statisticalFieldSample(i,random,count));if(samples[i].length>32)samples[i].shift();}count++;};
  const render=()=>{
    demo.querySelectorAll('[data-stat-panel]').forEach((svg,i)=>{
      const marker='stat-e-'+i+'-'+demo.dataset.lang;
      let art=`<defs><marker id="${marker}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#175da8"/></marker></defs><rect width="280" height="310" fill="white"/><path d="M35 145H245M140 40V250" stroke="black" stroke-width="1"/><text x="250" y="140">x</text><text x="147" y="35">y</text>`;
      for(const [j,e] of samples[i].entries()){
        const current=j===samples[i].length-1;art+=`<path d="M140 145L${140+62*e[0]} ${145-62*e[1]}" stroke="#175da8" stroke-opacity="${current?1:.13}" stroke-width="${current?2.5:1}" ${current?`marker-end="url(#${marker})"`:''}/>`;
      }
      art+=`<text x="140" y="284" text-anchor="middle">${T('Model target','模型目標')} DoLP ${targets[i]}</text>`;svg.innerHTML=art;
    });
    demo.querySelector('[data-stat-time]').textContent=count;
    play.textContent=running?T('Pause','暫停'):T('Play','播放');play.setAttribute('aria-pressed',String(running));
  };
  const tick=time=>{frame=0;if(!running||!visible||document.hidden){last=0;return;}if(!last||time-last>200){advance();render();last=time;}frame=requestAnimationFrame(tick);};
  const schedule=()=>{if(running&&visible&&!document.hidden&&!frame)frame=requestAnimationFrame(tick);};
  play.addEventListener('click',()=>{running=!running;last=0;render();schedule();});
  demo.querySelector('[data-stat-step]').addEventListener('click',()=>{running=false;advance();render();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;last=0;schedule();},{threshold:.05}).observe(demo);
  document.addEventListener('visibilitychange',()=>{last=0;schedule();});
  for(let i=0;i<32;i++)advance();render();
});
document.querySelectorAll('[data-sheet-demo]').forEach(demo=>{
  const zh=demo.dataset.lang==='zh',T=(en,cn)=>zh?cn:en,slider=demo.querySelector('[data-sheet-slider]');
  const pp=p=>lessonProjection(p).map(x=>x.toFixed(2)).join(' '),path=points=>points.map((p,i)=>(i?'L':'M')+pp(p)).join('');
  const update=()=>{
    const alpha=Number(slider.value),m=sheetProjection(alpha),t=m.axis,a=[-t[1],t[0],0],z0=2.55;
    const eid='sheet-e-'+demo.dataset.lang,kid='sheet-k-'+demo.dataset.lang;
    let art=`<defs><marker id="${eid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#175da8"/></marker><marker id="${kid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="black"/></marker></defs><rect width="900" height="430" fill="white"/>`;
    const add=(s,v,n)=>s.map((x,i)=>x+n*v[i]);
    const centre=[0,0,z0],corners=[[-1,-1],[1,-1],[1,1],[-1,1]].map(([u,v])=>add(add(centre,t,.8*u),a,.8*v));
    art+=`<path d="${path(corners)}Z" fill="#d1dbe5" fill-opacity=".5" stroke="#000" stroke-width="1"/>`;
    for(let j=-3;j<=3;j++){const base=add(centre,t,j*.2);art+=`<path d="M${pp(add(base,a,-.72))}L${pp(add(base,a,.72))}" stroke="#657282" stroke-opacity=".3" stroke-width="1"/>`;}
    art+=`<path d="M${pp([0,0,-.15])}L${pp([0,0,5.4])}" stroke="black" stroke-width="1.2" marker-end="url(#${kid})"/>`;
    for(const [end,label] of [[[1.05,0,z0],'x'],[[0,1.05,z0],'y'],[[0,0,5.4],'+z · k']]){const p=lessonProjection(end);if(label.length===1)art+=`<path d="M${pp(centre)}L${pp(end)}" stroke="black" stroke-width=".9" marker-end="url(#${kid})"/>`;art+=`<text x="${p[0]+8}" y="${p[1]-5}">${label}</text>`;}
    art+=`<path d="M${pp(add(centre,t,-1))}L${pp(add(centre,t,1))}" stroke="black" stroke-width="2" stroke-dasharray="4 3"/><text x="${lessonProjection(add(centre,t,1))[0]+8}" y="${lessonProjection(add(centre,t,1))[1]+10}">T</text>`;
    for(const [start,end,e] of [[0,2.4,[0,1,0]],[2.7,5.1,m.e]]){
      if(Math.hypot(...e)<1e-8)continue;
      const points=Array.from({length:161},(_,j)=>{const z=start+j/160*(end-start),phase=5.4*(z-z0);return [e[0]*.55*Math.cos(phase),e[1]*.55*Math.cos(phase),z];});
      art+=`<path d="${path(points)}" fill="none" stroke="#175da8" stroke-width="2"/>`;
      for(let j=0;j<=35;j++){const z=start+j/35*(end-start),g=.55*Math.cos(5.4*(z-z0));art+=`<path d="M${pp([0,0,z])}L${pp([e[0]*g,e[1]*g,z])}" stroke="#175da8" stroke-width=".9" marker-end="url(#${eid})"/>`;}
    }
    art+=`<text x="100" y="65" fill="#175da8">${T('Vertical input E','垂直入射 E')} · 1.00</text><text x="530" y="65" fill="#175da8">${T('Output E','出射 E')} · ${m.amplitude.toFixed(2)}</text><text x="90" y="400">${T('One fixed-time field snapshot; T is the transmission axis.','固定時刻的場快照；T 為穿透軸。')}</text>`;
    demo.querySelector('[data-sheet-scene]').innerHTML=art;
    const x=150,y=165,r=80,tx=r*t[0],ty=-r*t[1],ex=x+r*m.e[0],ey=y-r*m.e[1],id='sheet-end-'+demo.dataset.lang;
    demo.querySelector('[data-sheet-end]').innerHTML=`<defs><marker id="${id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#175da8"/></marker><marker id="${id}-out" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#0000ff"/></marker></defs><rect width="300" height="320" fill="white"/><path d="M25 165H275M150 35V280" stroke="black" stroke-width="1"/><text x="278" y="160">x</text><text x="160" y="33">y</text><circle cx="150" cy="165" r="100" fill="none" stroke="#a8b7c7"/><path d="M${x-tx*1.2} ${y-ty*1.2}L${x+tx*1.2} ${y+ty*1.2}" stroke="black" stroke-width="1.6" stroke-dasharray="4 4"/><text x="${x+tx*1.2+7}" y="${y+ty*1.2-5}">T</text><path d="M150 165V85" stroke="#175da8" stroke-width="2" marker-end="url(#${id})"/><text x="155" y="75" fill="#175da8">Ein</text><path d="M150 85L${ex} ${ey}" stroke="black" stroke-width=".8" stroke-dasharray="3 4"/>${m.amplitude>1e-8?`<path d="M150 165L${ex} ${ey}" stroke="#0000ff" stroke-width="3" marker-end="url(#${id}-out)"/>`:''}<text x="${ex+8}" y="${ey+18}" fill="#0000ff">Eout</text><text x="150" y="310" text-anchor="middle">${T('Look along the beam','沿光束方向看')}</text>`;
    demo.querySelector('[data-sheet-angle]').textContent=alpha+'°';
    demo.querySelector('[data-sheet-reading]').textContent=T(`Output field amplitude ${m.amplitude.toFixed(3)}; relative intensity ${(100*m.intensity).toFixed(1)}%.`,`出射場振幅 ${m.amplitude.toFixed(3)}；相對光強度 ${(100*m.intensity).toFixed(1)}%。`);
  };
  slider.addEventListener('input',update);demo.querySelectorAll('[data-sheet-preset]').forEach(b=>b.addEventListener('click',()=>{slider.value=b.dataset.sheetPreset;update();}));update();
});
