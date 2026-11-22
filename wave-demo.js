/* Vacuum plane wave: k = +z, E=(Ex,Ey,0), cB = k-hat × E. */
function waveComponents(state, theta) {
  const q=Math.SQRT1_2;
  const states={horizontal:[1,0,0],vertical:[0,1,0],diagonal:[q,q,0],circular:[q,q,Math.PI/2],elliptical:[1,.45,Math.PI/2]};
  const [ax,ay,delta]=states[state] || states.horizontal;
  const ex=ax*Math.cos(theta),ey=ay*Math.cos(theta+delta);
  return {e:[ex,ey,0],b:[-ey,ex,0]};
}
document.querySelectorAll('[data-wave-demo]').forEach(demo=>{
  const zh=demo.dataset.lang==='zh',T=(en,cn)=>zh?cn:en;
  const state=demo.querySelector('[data-wave-state]'),play=demo.querySelector('[data-wave-play]'),slider=demo.querySelector('[data-wave-phase]');
  const scene=demo.querySelector('[data-wave-scene]'),tip=demo.querySelector('[data-wave-tip]');
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let phase=0,running=!reduced,visible=false,last=0,frame=0;
  const K=2*Math.PI/1.6,zFixed=2.6;
  // One orthographic camera projects all positions and vectors.
  const view=[-7,-4,5].map(x=>x/Math.sqrt(90));
  const right=[view[2],0,-view[0]].map(x=>x/Math.hypot(view[2],view[0]));
  const up=[view[1]*right[2],view[2]*right[0]-view[0]*right[2],-view[1]*right[0]];
  const dot=(a,b)=>a.reduce((sum,x,i)=>sum+x*b[i],0);
  const project=p=>[90+130*dot(p,right),295-130*dot(p,up)];
  const pt=p=>project(p).map(x=>x.toFixed(2)).join(' ');
  const path=points=>points.map((p,i)=>(i?'L':'M')+pt(p)).join('');
  const arrow=(from,to,color,id,width=1)=>`<path d="M${pt(from)}L${pt(to)}" fill="none" stroke="${color}" stroke-width="${width}" marker-end="url(#${id})"/>`;
  const descriptions={
    horizontal:T('Linear x: E oscillates along x; cB oscillates along y.','水平線偏振：E 沿 x 軸往返振動，cB 沿 y 軸振動。'),
    vertical:T('Linear y: E oscillates along y; cB oscillates along the perpendicular x axis.','垂直線偏振：E 沿 y 軸往返振動，cB 沿垂直於它的 x 軸振動。'),
    diagonal:T('Linear 45°: the two E components have equal amplitude and the same phase.','45° 線偏振：兩個 E 分量等振幅、同相，電場末端沿固定斜軸往返。'),
    circular:T('Circular: equal E-component amplitudes with a 90° phase difference. E keeps a constant length while its direction rotates.','圓偏振：兩個 E 分量等振幅、相位差 90°；電場長度不變，方向隨時間旋轉。'),
    elliptical:T('Elliptical: unequal E-component amplitudes with a 90° phase difference in this example.','橢圓偏振：本例兩個 E 分量振幅不同、相位差 90°，電場末端描出橢圓。')
  };
  const updateControls=()=>{
    play.textContent=running?T('Pause','暫停'):T('Play','播放');play.setAttribute('aria-pressed',String(running));
    demo.querySelector('[data-wave-description]').textContent=descriptions[state.value];
  };
  const render=()=>{
    const eId=`wave-e-${demo.dataset.lang}`,bId=`wave-b-${demo.dataset.lang}`,kId=`wave-k-${demo.dataset.lang}`;
    const markers=[[eId,'#175da8'],[bId,'#c03941'],[kId,'#66788a']].map(([id,color])=>`<marker id="${id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="${color}"/></marker>`).join('');
    let art=`<defs>${markers}</defs><rect width="900" height="420" fill="white"/>`;
    const plane=[[-.75,-.75,zFixed],[.75,-.75,zFixed],[.75,.75,zFixed],[-.75,.75,zFixed]];
    art+=`<path d="${path(plane)}Z" fill="#eaf1f7" fill-opacity=".48" stroke="#b6c6d6" stroke-width="1"/>`;
    art+=arrow([0,0,-.2],[0,0,5.5],'#66788a',kId,1.2);
    for(const [to,label] of [[[1.05,0,0],'x'],[[0,1.05,0],'y'],[[0,0,5.5],'+z · k']]){
      if(label.length===1)art+=arrow([0,0,0],to,'#66788a',kId,.8);
      const [x,y]=project(to);art+=`<text x="${x+10}" y="${y-4}" fill="#536479">${label}</text>`;
    }
    const fields={e:[],b:[]};
    for(let j=0;j<=230;j++){
      const z=j/230*5.15,f=waveComponents(state.value,K*z-phase);
      for(const kind of ['e','b'])fields[kind].push([f[kind][0]*.52,f[kind][1]*.52,z]);
    }
    for(const [kind,color,id] of [['b','#c03941',bId],['e','#175da8',eId]]){
      art+=`<path d="${path(fields[kind])}" fill="none" stroke="${color}" stroke-width="1.7"/>`;
      for(let j=0;j<=42;j++){
        const z=j/42*5.1,f=waveComponents(state.value,K*z-phase)[kind];
        art+=arrow([0,0,z],[f[0]*.52,f[1]*.52,z],color,id,.8);
      }
    }
    const f=waveComponents(state.value,K*zFixed-phase),location=project([0,0,zFixed]);
    art+=`<circle cx="${location[0]}" cy="${location[1]}" r="3" fill="#536479"/><text x="${location[0]-10}" y="${location[1]+100}" text-anchor="middle">${T('Fixed position → panel (b)','固定位置 → (b)')}</text>`;
    art+=`<text x="690" y="40" fill="#175da8">E</text><text x="690" y="70" fill="#c03941">cB</text><text x="690" y="160">E ⊥ B</text><text x="690" y="190">E ⊥ z</text><text x="690" y="220">B ⊥ z</text>`;
    scene.innerHTML=art;
    const trajectory=kind=>Array.from({length:121},(_,j)=>{
      const vector=waveComponents(state.value,j/120*2*Math.PI)[kind];
      return `${j?'L':'M'}${150+85*vector[0]} ${160-85*vector[1]}`;
    }).join('');
    const ex=150+85*f.e[0],ey=160-85*f.e[1],bx=150+85*f.b[0],by=160-85*f.b[1];
    const tipMarkers=[['e','#175da8'],['b','#c03941']].map(([kind,color])=>`<marker id="wave-tip-${kind}-${demo.dataset.lang}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="${color}"/></marker>`).join('');
    tip.innerHTML=`<defs>${tipMarkers}</defs><rect width="300" height="320" fill="white"/><path d="M25 160H275M150 35V285" stroke="#acbac8" stroke-width="1"/><text x="279" y="153">x</text><text x="160" y="32">y</text>
      <path d="${trajectory('e')}" stroke="#175da8" stroke-opacity=".35" stroke-width="1.2" fill="none"/>
      <path d="${trajectory('b')}" stroke="#c03941" stroke-opacity=".45" stroke-dasharray="4 4" stroke-width="1.2" fill="none"/>
      <path data-tip-field="E" d="M150 160L${ex} ${ey}" stroke="#175da8" stroke-width="2" marker-end="url(#wave-tip-e-${demo.dataset.lang})"/>
      <path data-tip-field="cB" d="M150 160L${bx} ${by}" stroke="#c03941" stroke-width="2" marker-end="url(#wave-tip-b-${demo.dataset.lang})"/>
      <circle cx="${ex}" cy="${ey}" r="3.5" fill="#175da8"/><circle cx="${bx}" cy="${by}" r="3.5" fill="#c03941"/>
      <text x="${ex+8}" y="${ey-8}" fill="#175da8">E</text><text x="${bx+8}" y="${by+19}" fill="#c03941">cB</text>
      <text x="150" y="310" text-anchor="middle">${T('E and cB at the same instant','同一時刻的 E 與 cB')}</text>`;
    const degrees=Math.round(phase/(2*Math.PI)*360)%360;slider.value=degrees;
    demo.querySelector('[data-wave-phase-label]').textContent=degrees+'°';
  };
  const tick=time=>{
    frame=0;
    if(!running||!visible||document.hidden){last=0;return;}
    if(last)phase=(phase+Math.min((time-last)/1000,.05)*2*Math.PI/4)%(2*Math.PI);
    last=time;render();frame=requestAnimationFrame(tick);
  };
  const schedule=()=>{if(running&&visible&&!document.hidden&&!frame)frame=requestAnimationFrame(tick);};
  play.addEventListener('click',()=>{running=!running;last=0;updateControls();schedule();});
  state.addEventListener('change',()=>{phase=0;last=0;updateControls();render();schedule();});
  slider.addEventListener('input',()=>{running=false;last=0;phase=Number(slider.value)/360*2*Math.PI;updateControls();render();});
  demo.querySelector('[data-wave-reset]').addEventListener('click',()=>{phase=0;last=0;render();});
  document.addEventListener('visibilitychange',()=>{last=0;schedule();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;last=0;schedule();},{threshold:.05}).observe(demo);
  updateControls();render();
});
