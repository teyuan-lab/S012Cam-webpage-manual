(() => {
  document.querySelectorAll('[data-video]').forEach(button => button.addEventListener('click', () => {
    const video = document.getElementById(button.dataset.video);
    if (!video) return;
    const seek = () => { video.currentTime = Number(button.dataset.time); video.play().catch(() => {}); };
    if (video.readyState) seek(); else { video.addEventListener('loadedmetadata', seek, { once: true }); video.load(); }
  }));
  document.querySelectorAll('.capture-demo').forEach(demo => {
    if (demo.dataset.ready) return;
    demo.dataset.ready = 'true';
    const buttons = [...demo.querySelectorAll('[data-step]')];
    const labels = [...demo.querySelectorAll('.sequence-labels p')];
    const focus = demo.querySelector('.sequence-focus');
    const play = demo.querySelector('.sequence-play');
    let active = 0, timer = null;
    const select = index => {
      active = index;
      buttons.forEach((b, i) => b.setAttribute('aria-pressed', String(i === index)));
      labels.forEach((p, i) => p.hidden = i !== index);
      focus.style.transform = `translate(${index % 2 * 100}%, ${Math.floor(index / 2) * 100}%)`;
    };
    const stop = () => { clearInterval(timer); timer = null; play.textContent = play.dataset.playLabel; };
    buttons.forEach((b, i) => b.addEventListener('click', () => { stop(); select(i); }));
    play.addEventListener('click', () => {
      if (timer) return stop();
      select(0); play.textContent = play.dataset.pauseLabel;
      timer = setInterval(() => { if (active === 3) stop(); else select(active + 1); }, 3000);
    });
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
  });
})();
