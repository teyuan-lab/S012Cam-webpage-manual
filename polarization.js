function drawReflectionGeometry(scene, degrees, n, zh) {
  const a=degrees*Math.PI/180, t=Math.asin(Math.sin(a)/n), c=Math.cos(a), ct=Math.cos(t);
  const rs=((c-n*ct)/(c+n*ct))**2, rp=((n*c-ct)/(n*c+ct))**2;
      const r=245, x=320, y=300, dx=r*Math.sin(a), dy=r*Math.cos(a), tr=230;
      scene.querySelector('[data-incident]').setAttribute('d',`M${x-dx} ${y-dy}L${x} ${y}`);
      scene.querySelector('[data-reflected]').setAttribute('d',`M${x} ${y}L${x+dx} ${y-dy}`);
      scene.querySelector('[data-transmitted]').setAttribute('d',`M${x} ${y}L${x+tr*Math.sin(t)} ${y+tr*Math.cos(t)}`);
      scene.querySelector('[data-angle-arc]').setAttribute('d', degrees ? `M${x} ${y-70}A70 70 0 0 0 ${x-70*Math.sin(a)} ${y-70*Math.cos(a)}` : '');
      scene.querySelector('[data-ray-angle]').textContent = `${degrees}°`;
      // Common electric-field amplitude scale. n1=1, n2=n, no absorption.
      // T = n*cos(t)/cos(a) * |tE|²; transmission amplitude is not sqrt(1-R).
      const tTE=2*c/(c+n*ct), tTM=2*c/(n*c+ct);
      const fieldSymbol=(cx,cy,amplitude,kind,normal,labelSide=1)=>{
        const size=28*amplitude, label=`${kind} ${amplitude.toFixed(2)}`;
        if(kind==='TE') {
          const d=size*.60;
          return `<g data-field="TE" data-amplitude="${amplitude}"><circle cx="${cx}" cy="${cy}" r="${size}" fill="white" fill-opacity=".92" stroke="#175da8" stroke-width="1.8"/><path d="M${cx-d} ${cy-d}L${cx+d} ${cy+d}M${cx-d} ${cy+d}L${cx+d} ${cy-d}" stroke="#175da8" stroke-width="1.8"/><text x="${cx+labelSide*(size+8)}" y="${cy-8}" text-anchor="${labelSide<0?'end':'start'}" fill="#175da8">${label}</text></g>`;
        }
        const [nx,ny]=normal;
        return `<g data-field="TM" data-amplitude="${amplitude}">${size>.04?`<path d="M${cx-nx*size} ${cy-ny*size}L${cx+nx*size} ${cy+ny*size}" stroke="#0000ff" stroke-width="2.8" marker-start="url(#fieldtip-${scene.dataset.markers || (zh?'zh':'en')})" marker-end="url(#fieldtip-${scene.dataset.markers || (zh?'zh':'en')})"/>`:''}<text x="${cx+labelSide*(Math.abs(nx*size)+8)}" y="${cy+Math.abs(ny*size)+19}" text-anchor="${labelSide<0?'end':'start'}" fill="#0000ff">${label}</text></g>`;
      };
      let fields='';
      const add=(fraction,vx,vy,amp,kind,normal,side)=>{fields+=fieldSymbol(x+fraction*vx,y+fraction*vy,amp,kind,normal,side);};
      add(.88,-dx,-dy,1,'TE',[c,-Math.sin(a)],-1);
      add(.64,-dx,-dy,1,'TM',[c,-Math.sin(a)],-1);
      add(.40,dx,-dy,Math.sqrt(rs),'TE',[c,Math.sin(a)],1);
      add(.84,dx,-dy,Math.sqrt(rp),'TM',[c,Math.sin(a)],1);
      add(.35,tr*Math.sin(t),tr*Math.cos(t),tTE,'TE',[ct,-Math.sin(t)],-1);
      add(.78,tr*Math.sin(t),tr*Math.cos(t),tTM,'TM',[ct,-Math.sin(t)],1);
      const nearB=Math.abs(degrees-Math.atan(n)*180/Math.PI)<.6;
      if(nearB) {
        const u=[Math.sin(a)*19,-Math.cos(a)*19], v=[Math.sin(t)*19,Math.cos(t)*19];
        fields+=`<path d="M${x+u[0]} ${y+u[1]}L${x+u[0]+v[0]} ${y+u[1]+v[1]}L${x+v[0]} ${y+v[1]}" fill="none" stroke="#008679" stroke-width="1.8"/>`;
      }
      scene.querySelector('[data-electric-fields]').innerHTML=fields;
}
/* Teaching scenes use the stated ideal models. They are not measured camera data. */
document.querySelectorAll('.physics-demo').forEach(demo => {
  const slider = demo.querySelector('[data-angle-input]');
  const input = demo.querySelector('[data-input]');
  const zh = demo.dataset.lang === 'zh';
  const update = () => {
    const degrees = Number(slider.value), a = degrees * Math.PI / 180;
    demo.querySelector('[data-angle]').textContent = `${degrees}°`;
    if (demo.dataset.model === 'malus') {
      const intensity = Math.cos(a) ** 2;
      demo.querySelector('[data-result]').textContent = `${Math.round(intensity * 100)}%`;
      const beta=Number(demo.querySelector('[data-lcd-source-angle]').value);
      demo.querySelectorAll('.source-axis').forEach(axis=>{axis.style.transform=`rotate(${90-beta}deg)`;});
      demo.querySelector('[data-film]').style.transform = `translate(-50%, -50%) rotate(${90-beta-degrees}deg)`;
      demo.querySelector('[data-extinction]').style.opacity = String(1 - intensity);
      let message;
      if (intensity > .995) message = zh ? '兩軸平行：LCD 的電場沿穿透軸，透過偏振片看到的範圍最亮。' : 'Parallel axes: the LCD E follows the transmission axis, so the region viewed through the sheet is brightest.';
      else if (intensity < .005) message = zh ? '兩軸垂直：LCD 的電場被偏振片吸收，片內範圍最暗；片外仍是原來的白色螢幕。' : 'Crossed axes: the sheet absorbs the LCD E. The region inside the sheet is darkest; the uncovered screen stays white.';
      else message = zh ? `只有電場在穿透軸上的分量通過。現在片內的光強度約為最亮時的 ${Math.round(intensity*100)}%；片外不變。` : `Only the E component along the transmission axis passes. Inside the sheet, intensity is ${Math.round(intensity*100)}% of maximum; the uncovered screen is unchanged.`;
      demo.querySelector('[data-explanation]').textContent = message;
    } else {
      const n = Number(input.value), t = Math.asin(Math.sin(a) / n), c = Math.cos(a), ct = Math.cos(t);
      const rs = ((c - n * ct) / (c + n * ct)) ** 2;
      const rp = ((n * c - ct) / (n * c + ct)) ** 2;
      demo.querySelector('[data-rs]').textContent = rs.toFixed(3);
      demo.querySelector('[data-rp]').textContent = rp.toFixed(3);
      demo.querySelector('[data-result]').textContent = (Math.abs(rs-rp)/(rs+rp)).toFixed(3);
      // Both views of Fig. 5 follow the same physical model and selected angle.
      const reflectance = deg => {
        const a=deg*Math.PI/180, c=Math.cos(a), ct=Math.sqrt(1-(Math.sin(a)/n)**2);
        return [((c-n*ct)/(c+n*ct))**2,((n*c-ct)/(n*c+ct))**2];
      };
      const xp=deg=>60+deg/90*540, yp=r=>280-r*240;
      document.querySelectorAll('[data-reflectance-plot]').forEach(plot=>{
        let markup='<rect width="640" height="340" rx="12" fill="white"/>';
        for(let tick=0;tick<=1.001;tick+=.2) markup+=`<path d="M60 ${yp(tick)}H600" stroke="#dce3eb" stroke-width=".8"/><text x="49" y="${yp(tick)+4}" text-anchor="end">${tick.toFixed(1)}</text>`;
        for(let deg=0;deg<=90;deg+=15) markup+=`<text x="${xp(deg)}" y="302" text-anchor="middle">${deg}°</text>`;
        markup+='<path d="M60 40V280H600" fill="none" stroke="#000000" stroke-width="1"/>';
        for(const [i,color] of [[0,'#175da8'],[1,'#0000ff']]) {
          const points=Array.from({length:361},(_,j)=>{const d=j/4;return `${j?'L':'M'}${xp(d)} ${yp(reflectance(d)[i])}`;}).join('');
          markup+=`<path d="${points}" fill="none" stroke="${color}" stroke-width="${i===1?2.8:2.2}"/><circle cx="${xp(degrees)}" cy="${yp([rs,rp][i])}" r="4.5" fill="${color}" stroke="white" stroke-width="1"/>`;
        }
        const brewster=Math.atan(n)*180/Math.PI;
        markup+=`<path d="M${xp(brewster)} 44V280" stroke="#008679" stroke-width="1" stroke-dasharray="1 4"/><text x="${xp(brewster)}" y="55" text-anchor="end" fill="#008679">θB ${brewster.toFixed(1)}°</text>`;
        markup+=`<path d="M${xp(degrees)} 40V280" stroke="#697789" stroke-width="1" stroke-dasharray="4 4"/><text x="${Math.min(555,Math.max(95,xp(degrees)))}" y="24" text-anchor="middle">${degrees}°</text>`;
        markup+=`<text x="75" y="24" fill="#175da8">TE</text><text x="115" y="24" fill="#0000ff">TM</text><text x="330" y="330" text-anchor="middle">${zh?'由法線量起的入射角':'Incidence angle from the normal'}</text><text transform="translate(17 165) rotate(-90)" text-anchor="middle">${zh?'反射率 R':'Reflectance R'}</text>`;
        plot.innerHTML=markup;
      });
      document.querySelectorAll('.reflection-scene').forEach(scene => drawReflectionGeometry(scene,degrees,n,zh));
      const nearB=Math.abs(degrees-Math.atan(n)*180/Math.PI)<.6;
      demo.querySelector('[data-explanation]').textContent = degrees<.5 ? (zh?'正入射：TE 與 TM 反射率相同，沒有因反射而偏好某個線偏振方向。':'Normal incidence: TE and TM have equal reflectance. Reflection does not favour one linear axis.') : nearB ? (zh?'接近 Brewster 角：正藍色 TM 分量接近零，反射光幾乎只剩深藍色 TE 分量；水平表面的這種反光為水平偏振。':'Near Brewster’s angle: the bright-blue TM component is almost zero. Reflected light is nearly all TE, which is horizontal for this horizontal surface.') : (zh?'兩種電場的反射率不同。拖動角度，看正藍色 TM 分量如何先減弱、接近零，再增加。':'The two E components have different reflectances. Change the angle to see the bright-blue TM component decrease toward zero and then increase again.');
    }
  };
  slider.addEventListener('input', update); input?.addEventListener('change', update);
  demo.querySelector('[data-lcd-source-angle]')?.addEventListener('change',update);
  demo.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>{slider.value=b.dataset.preset;update();}));
  demo.querySelector('[data-brewster]')?.addEventListener('click',()=>{slider.value=(Math.atan(Number(input.value))*180/Math.PI).toFixed(1);update();});
  update();
});
