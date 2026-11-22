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
      demo.querySelector('[data-film]').style.transform = `translate(-50%, -50%) rotate(${-degrees}deg)`;
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
      demo.querySelector('[data-s-bar]').style.width = `${rs*100}%`;
      demo.querySelector('[data-p-bar]').style.width = `${rp*100}%`;
      const r=220, x=320, y=280, dx=r*Math.sin(a), dy=r*Math.cos(a);
      demo.querySelector('[data-incident]').setAttribute('d',`M${x-dx} ${y-dy}L${x} ${y}`);
      demo.querySelector('[data-reflected]').setAttribute('d',`M${x} ${y}L${x+dx} ${y-dy}`);
      demo.querySelector('[data-transmitted]').setAttribute('d',`M${x} ${y}L${x+100*Math.sin(t)} ${y+100*Math.cos(t)}`);
      demo.querySelector('[data-angle-arc]').setAttribute('d', degrees ? `M${x} ${y-70}A70 70 0 0 0 ${x-70*Math.sin(a)} ${y-70*Math.cos(a)}` : '');
      demo.querySelector('[data-ray-angle]').textContent = `${degrees}°`;
      const nearB=Math.abs(degrees-Math.atan(n)*180/Math.PI)<.6;
      demo.querySelector('[data-explanation]').textContent = degrees<.5 ? (zh?'正入射：s 與 p 反射率相同，沒有因反射而偏好某個線偏振方向。':'Normal incidence: s and p have equal reflectance. Reflection does not favour one linear axis.') : nearB ? (zh?'接近 Brewster 角：紅色 p 分量接近零，反射光幾乎只剩藍色 s 分量；水平表面的這種反光為水平偏振。':'Near Brewster’s angle: the red p component is almost zero. Reflected light is nearly all s, which is horizontal for this horizontal surface.') : (zh?'兩種電場的反射率不同。拖動角度，看紅色 p 分量如何先減弱、接近零，再增加。':'The two E components have different reflectances. Change the angle to see the red p component decrease toward zero and then increase again.');
    }
  };
  slider.addEventListener('input', update); input?.addEventListener('change', update);
  demo.querySelectorAll('[data-preset]').forEach(b=>b.addEventListener('click',()=>{slider.value=b.dataset.preset;update();}));
  demo.querySelector('[data-brewster]')?.addEventListener('click',()=>{slider.value=(Math.atan(Number(input.value))*180/Math.PI).toFixed(1);update();});
  update();
});
