(() => {
  const VERSION = '0.3.3-direct-now-playing-topmost-keeper';
  const STATE_API = '/api/state';
  const nowPlayingUrl = 'http://127.0.0.1:4004/';
  const volumioRootUrl = 'http://127.0.0.1:3000/';
  const minStartupMs = 9000;
  const settleAfterUiLoadMs = 1200;
  const fallbackToVolumioAfterMs = 22000;

  let state = { standby:false, startup_completed:false, startup_started_at:Date.now(), last_transition:null, version:VERSION };
  const qs = new URLSearchParams(window.location.search);
  let targetMode = qs.get('target') || 'nowplaying';
  let targetUrl = targetMode === 'volumio' ? volumioRootUrl : nowPlayingUrl;

  const frame = document.getElementById('target-frame');
  const artwork = document.getElementById('artwork-overlay');
  const standbyOverlay = document.getElementById('standby-overlay');
  const clockEl = standbyOverlay.querySelector('.ms-clock');
  let uiLoadedAt = null;
  let fadeDone = false;
  let fallbackTriggered = false;

  async function fetchState() {
    try {
      const res = await fetch(STATE_API, { cache:'no-store' });
      if (res.ok) state = await res.json();
    } catch (_) {}
  }

  async function pushState(update) {
    try {
      const res = await fetch(STATE_API, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(update),
        cache:'no-store'
      });
      if (res.ok) state = await res.json();
    } catch (_) {}
  }

  function updateClock() {
    const now = new Date();
    clockEl.textContent = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}`;
  }

  function setStandbyVisuals() {
    if (state.standby) standbyOverlay.classList.add('ms-visible');
    else standbyOverlay.classList.remove('ms-visible');
  }

  async function maybeFadeToTarget() {
    if (fadeDone || state.standby) return;
    const started = state.startup_started_at || Date.now();
    const elapsed = Date.now() - started;
    if (elapsed < minStartupMs) return;
    if (!uiLoadedAt) return;
    if ((Date.now() - uiLoadedAt) < settleAfterUiLoadMs) return;
    frame.classList.add('ms-visible');
    requestAnimationFrame(() => artwork.classList.add('ms-hidden'));
    fadeDone = true;
    await pushState({ startup_completed:true, last_transition:Date.now(), version:VERSION });
  }

  async function maybeFallback() {
    if (fallbackTriggered || targetMode !== 'nowplaying' || uiLoadedAt) return;
    const started = state.startup_started_at || Date.now();
    const elapsed = Date.now() - started;
    if (elapsed < fallbackToVolumioAfterMs) return;
    fallbackTriggered = true;
    targetMode = 'volumio';
    targetUrl = volumioRootUrl;
    frame.src = targetUrl;
  }

  frame.addEventListener('load', () => { uiLoadedAt = Date.now(); }, { once:false });

  async function wake() {
    if (!state.standby) return;
    await pushState({ standby:false, last_transition:Date.now(), version:VERSION });
    setStandbyVisuals();
  }

  standbyOverlay.addEventListener('pointerdown', wake, { passive:true });
  document.addEventListener('keydown', wake);

  async function tick() {
    await fetchState();
    updateClock();
    setStandbyVisuals();
    await maybeFallback();
    await maybeFadeToTarget();
    setTimeout(tick, 750);
  }

  async function init() {
    await fetchState();
    if (!state.startup_started_at) {
      await pushState({ startup_started_at:Date.now(), startup_completed:false, version:VERSION });
    }
    frame.src = targetUrl;
    updateClock();
    setStandbyVisuals();
    tick();
  }

  init();
})();
