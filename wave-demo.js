/* Vacuum plane wave: k = +z, E=(Ex,Ey,0), cB = k-hat × E. */
// Optical convention: receiver looks towards the source, along -z.
// chi > 0 is left-handed (counter-clockwise with time in the x-y view).
function waveParameters(state, psiDegrees=30, chiDegrees=20) {
  const presets={horizontal:[0,0],vertical:[90,0],diagonal:[45,0],'left-circular':[0,45],'right-circular':[0,-45]};
  const [psi,chi]=presets[state] || [psiDegrees,chiDegrees];
  return {psi:psi*Math.PI/180,chi:chi*Math.PI/180};
}
function waveComponents(state, theta, psiDegrees=30, chiDegrees=20) {
  const {psi,chi}=waveParameters(state,psiDegrees,chiDegrees);
  const u=Math.cos(chi)*Math.cos(theta),v=-Math.sin(chi)*Math.sin(theta);
  const ex=u*Math.cos(psi)-v*Math.sin(psi),ey=u*Math.sin(psi)+v*Math.cos(psi);
  return {e:[ex,ey,0],b:[-ey,ex,0]};
}
document.querySelectorAll('[data-wave-demo]').forEach(demo=>{
  const zh=demo.dataset.lang==='zh',T=(en,cn)=>zh?cn:en;
  const state=demo.querySelector('[data-wave-state]'),play=demo.querySelector('[data-wave-play]'),slider=demo.querySelector('[data-wave-phase]');
  const psiInput=demo.querySelector('[data-wave-psi]'),chiInput=demo.querySelector('[data-wave-chi]');
  const sample=theta=>waveComponents(state.value,theta,Number(psiInput.value),Number(chiInput.value));
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
    'left-circular':T('Left circular: E rotates counter-clockwise with time in panel (b), looking towards the source.','左圓偏振：從接收端朝光源看，圖 (b) 的 E 隨時間逆時針旋轉。'),
    'right-circular':T('Right circular: E rotates clockwise with time in panel (b), looking towards the source.','右圓偏振：從接收端朝光源看，圖 (b) 的 E 隨時間順時針旋轉。')
  };
  const updateControls=()=>{
    play.textContent=running?T('Pause','暫停'):T('Play','播放');play.setAttribute('aria-pressed',String(running));
    const psi=Number(psiInput.value),chi=Number(chiInput.value),circular=Math.abs(chi)===45;
    demo.querySelector('[data-wave-arbitrary]').hidden=state.value!=='arbitrary';
    psiInput.disabled=circular;
    demo.querySelector('[data-wave-psi-label]').textContent=circular?T('undefined for a circle','圓偏振時不定'):psi+'°';
    demo.querySelector('[data-wave-chi-label]').textContent=(chi>0?'+':'')+chi+'°';
    const rotation=chi===0?T('linear','線偏振'):chi>0?T('left-handed','左旋'):T('right-handed','右旋');
    demo.querySelector('[data-wave-ellipse-summary]').textContent=`v/u = ${Math.tan(Math.abs(chi)*Math.PI/180).toFixed(3)} · ${rotation}`;
    demo.querySelector('[data-wave-description]').textContent=state.value==='arbitrary'?T(`Arbitrary fully polarized state: ψ = ${circular?'undefined':psi+'°'}, χ = ${chi}°; ${rotation}. ${circular?'A circle has no unique major axis.':'The dashed axes in (b) show the ellipse semiaxes u and v.'}`,`任意完全偏振態：ψ = ${circular?'不定':psi+'°'}，χ = ${chi}°，${rotation}。${circular?'圓形沒有唯一的長軸方向。':'圖 (b) 的輔助線標示長、短半軸 u、v。'}`):descriptions[state.value];
  };
  const render=()=>{
    const eId=`wave-e-${demo.dataset.lang}`,bId=`wave-b-${demo.dataset.lang}`,kId=`wave-k-${demo.dataset.lang}`;
    const markers=[[eId,'#175da8'],[bId,'#c03941'],[kId,'#000000']].map(([id,color])=>`<marker id="${id}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="${color}"/></marker>`).join('');
    let art=`<defs>${markers}</defs><rect width="900" height="420" fill="white"/>`;
    const plane=[[-.75,-.75,zFixed],[.75,-.75,zFixed],[.75,.75,zFixed],[-.75,.75,zFixed]];
    art+=`<path d="${path(plane)}Z" fill="#eaf1f7" fill-opacity=".48" stroke="#b6c6d6" stroke-width="1"/>`;
    art+=arrow([0,0,-.2],[0,0,5.5],'#000000',kId,1.2);
    for(const [to,label] of [[[1.05,0,0],'x'],[[0,1.05,0],'y'],[[0,0,5.5],'+z · k']]){
      if(label.length===1)art+=arrow([0,0,0],to,'#000000',kId,.8);
      const [x,y]=project(to);art+=`<text x="${x+10}" y="${y-4}" fill="#000000">${label}</text>`;
    }
    const fields={e:[],b:[]};
    for(let j=0;j<=230;j++){
      const z=j/230*5.15,f=sample(K*z-phase);
      for(const kind of ['e','b'])fields[kind].push([f[kind][0]*.52,f[kind][1]*.52,z]);
    }
    for(const [kind,color,id] of [['b','#c03941',bId],['e','#175da8',eId]]){
      art+=`<path d="${path(fields[kind])}" fill="none" stroke="${color}" stroke-width="1.7"/>`;
      for(let j=0;j<=42;j++){
        const z=j/42*5.1,f=sample(K*z-phase)[kind];
        art+=arrow([0,0,z],[f[0]*.52,f[1]*.52,z],color,id,.8);
      }
    }
    const f=sample(K*zFixed-phase),location=project([0,0,zFixed]);
    art+=`<circle cx="${location[0]}" cy="${location[1]}" r="3" fill="#000000"/><text x="${location[0]-10}" y="${location[1]+100}" text-anchor="middle">${T('Fixed position → panel (b)','固定位置 → (b)')}</text>`;
    art+=`<text x="690" y="40" fill="#175da8">E</text><text x="690" y="70" fill="#c03941">cB</text><text x="690" y="160"><tspan fill="#175da8">E</tspan> ⊥ <tspan fill="#c03941">B</tspan></text><text x="690" y="190"><tspan fill="#175da8">E</tspan> ⊥ z</text><text x="690" y="220"><tspan fill="#c03941">B</tspan> ⊥ z</text>`;
    scene.innerHTML=art;
    const trajectory=kind=>Array.from({length:121},(_,j)=>{
      const vector=sample(j/120*2*Math.PI)[kind];
      return `${j?'L':'M'}${150+85*vector[0]} ${160-85*vector[1]}`;
    }).join('');
    const ex=150+85*f.e[0],ey=160-85*f.e[1],bx=150+85*f.b[0],by=160-85*f.b[1];
    const tipMarkers=[['e','#175da8'],['b','#c03941']].map(([kind,color])=>`<marker id="wave-tip-${kind}-${demo.dataset.lang}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="${color}"/></marker>`).join('');
    const parameters=waveParameters(state.value,Number(psiInput.value),Number(chiInput.value));
    let ellipseGuides='';
    if(state.value==='arbitrary' && Math.abs(parameters.chi)<Math.PI/4-1e-8) {
      const psi=parameters.psi,major=85*Math.cos(parameters.chi),minor=85*Math.abs(Math.sin(parameters.chi));
      const ux=Math.cos(psi),uy=-Math.sin(psi),vx=-Math.sin(psi),vy=-Math.cos(psi);
      ellipseGuides=`<path d="M${150-major*ux} ${160-major*uy}L${150+major*ux} ${160+major*uy}M${150-minor*vx} ${160-minor*vy}L${150+minor*vx} ${160+minor*vy}" stroke="#000000" stroke-width=".9" stroke-dasharray="3 4"/>
        <text x="${150+major*ux+6}" y="${160+major*uy-6}">u</text>${minor>5?`<text x="${150+minor*vx-14}" y="${160+minor*vy-6}">v</text>`:''}`;
      if(Math.abs(psi)>.01) ellipseGuides+=`<path d="M178 160A28 28 0 0 ${psi>0?0:1} ${150+28*ux} ${160+28*uy}" fill="none" stroke="#9b6c26" stroke-width="1"/><text x="${150+40*Math.cos(psi/2)}" y="${160-40*Math.sin(psi/2)}" fill="#9b6c26">ψ</text>`;
    }
    tip.innerHTML=`<defs>${tipMarkers}</defs><rect width="300" height="320" fill="white"/><path d="M25 160H275M150 35V285" stroke="#000000" stroke-width="1"/><text x="279" y="153">x</text><text x="160" y="32">y</text>
      <path d="${trajectory('e')}" stroke="#175da8" stroke-opacity=".35" stroke-width="1.2" fill="none"/>
      <path d="${trajectory('b')}" stroke="#c03941" stroke-opacity=".45" stroke-dasharray="4 4" stroke-width="1.2" fill="none"/>
      ${ellipseGuides}<path data-tip-field="E" d="M150 160L${ex} ${ey}" stroke="#175da8" stroke-width="2" marker-end="url(#wave-tip-e-${demo.dataset.lang})"/>
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
  [psiInput,chiInput].forEach(input=>input.addEventListener('input',()=>{last=0;updateControls();render();schedule();}));
  state.addEventListener('change',()=>{phase=0;last=0;updateControls();render();schedule();});
  slider.addEventListener('input',()=>{running=false;last=0;phase=Number(slider.value)/360*2*Math.PI;updateControls();render();});
  demo.querySelector('[data-wave-reset]').addEventListener('click',()=>{phase=0;last=0;render();});
  document.addEventListener('visibilitychange',()=>{last=0;schedule();});
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;last=0;schedule();},{threshold:.05}).observe(demo);
  updateControls();render();
});
