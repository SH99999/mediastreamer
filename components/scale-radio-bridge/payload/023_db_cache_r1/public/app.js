(function(){
  const els = {
    trackTitle: document.getElementById('trackTitle'),
    trackArtist: document.getElementById('trackArtist'),
    artBox: document.getElementById('artBox'),
    metaTrack: document.getElementById('metaTrack'),
    metaArtist: document.getElementById('metaArtist'),
    metaStation: document.getElementById('metaStation'),
    metaService: document.getElementById('metaService'),
    metaState: document.getElementById('metaState'),
    lyrics: document.getElementById('lyrics'),
    svcPill: document.getElementById('svcPill'),
    stationPill: document.getElementById('stationPill'),
    spotifyPill: document.getElementById('spotifyPill'),
    lyricsPill: document.getElementById('lyricsPill'),
    spotifyMatchWrap: document.getElementById('spotifyMatchWrap'),
    spotifyMatchText: document.getElementById('spotifyMatchText'),
    playlists: document.getElementById('playlists'),
    playlistFeedback: document.getElementById('playlistFeedback'),
    offsetMinus: document.getElementById('offsetMinus'),
    offsetPlus: document.getElementById('offsetPlus'),
    singAlongBtn: document.getElementById('singAlongBtn'),
    singAlongModal: document.getElementById('singAlongModal'),
    singAlongClose: document.getElementById('singAlongClose'),
    singAlongLyrics: document.getElementById('singAlongLyrics')
  };

  let busy = false;
  let requestSeq = 0;
  let lastMainActiveIndex = -2;
  let lastSingActiveIndex = -2;

  function showFeedback(text, ok){
    if (!els.playlistFeedback) return;
    els.playlistFeedback.className='feedback ' + (ok ? 'ok':'bad');
    els.playlistFeedback.textContent=text;
    els.playlistFeedback.classList.remove('hidden');
  }

  function setArt(url){
    if (!els.artBox) return;
    els.artBox.innerHTML='';
    if(url){
      const img=document.createElement('img');
      img.src=url;
      img.alt='Track art';
      img.onerror=function(){ els.artBox.innerHTML='<div class="art-fallback">No image</div>'; };
      els.artBox.appendChild(img);
    } else {
      els.artBox.innerHTML='<div class="art-fallback">No image</div>';
    }
  }

  function buildLyricsNodes(container, lyrics){
    container.innerHTML='';
    const lines = Array.isArray(lyrics && lyrics.lines) ? lyrics.lines : [];
    const activeIndex = typeof (lyrics && lyrics.activeIndex) === 'number' ? lyrics.activeIndex : -1;
    if(!lines.length){
      const raw = String((lyrics && lyrics.text) || '').trim();
      const pseudo = raw ? raw.split(/\r?\n+/).map(s=>s.trim()).filter(Boolean) : [];
      if(pseudo.length > 1){
        container.className = container.id === 'singAlongLyrics' ? 'singalong-lyrics' : '';
        pseudo.forEach((line)=>{
          const div=document.createElement('div');
          div.className='lyrics-line near';
          div.textContent=line;
          container.appendChild(div);
        });
      } else {
        container.className = (container.id === 'singAlongLyrics' ? 'singalong-lyrics ' : '') + 'lyrics-empty';
        container.textContent = raw || 'No lyrics found for the current metadata.';
      }
      return { activeIndex: -1 };
    }
    container.className = container.id === 'singAlongLyrics' ? 'singalong-lyrics' : '';
    lines.forEach((line, idx)=>{
      const div=document.createElement('div');
      let cls='lyrics-line';
      if(idx===activeIndex) cls+=' active';
      else if(activeIndex >= 0 && Math.abs(idx-activeIndex) <= 2) cls+=' near';
      else cls+=' far';
      div.className=cls;
      div.textContent=(line && line.text) ? line.text : '';
      container.appendChild(div);
    });
    return { activeIndex };
  }

  function positionActiveLine(container, activeIndex, previousIndex, ratio){
    if(activeIndex < 0) return activeIndex;
    const target = container.children[activeIndex];
    if(!target) return activeIndex;
    const doPosition = ()=>{
      const containerHeight = container.clientHeight || 0;
      const targetTop = target.offsetTop || 0;
      const targetHeight = target.offsetHeight || 0;
      const desiredTop = Math.max(0, Math.round(targetTop - (containerHeight * ratio) + (targetHeight / 2)));
      const currentTop = container.scrollTop || 0;
      const delta = Math.abs(currentTop - desiredTop);
      if(delta > 1){
        container.scrollTop = desiredTop;
      }
    };
    requestAnimationFrame(()=>requestAnimationFrame(doPosition));
    return activeIndex;
  }

  function renderLyrics(data){
    const lyrics = data && data.lyrics;
    if(!els.lyrics) return;
    if(!lyrics){
      els.lyrics.className='lyrics-empty';
      els.lyrics.textContent='The overlay is running. As soon as Volumio publishes artist and title metadata, lyrics will appear here.';
      if(els.singAlongLyrics){
        els.singAlongLyrics.className='singalong-lyrics lyrics-empty';
        els.singAlongLyrics.textContent='Lyrics will appear here.';
      }
      lastMainActiveIndex = -2;
      lastSingActiveIndex = -2;
      return;
    }
    const main = buildLyricsNodes(els.lyrics, lyrics);
    lastMainActiveIndex = positionActiveLine(els.lyrics, main.activeIndex, lastMainActiveIndex, 0.33);
    if(els.singAlongLyrics){
      const sing = buildLyricsNodes(els.singAlongLyrics, lyrics);
      lastSingActiveIndex = positionActiveLine(els.singAlongLyrics, sing.activeIndex, lastSingActiveIndex, 0.28);
    }
  }

  function renderPlaylists(state){
    if (!els.playlists) return;
    els.playlists.innerHTML='';
    (state.playlists || []).forEach(pl=>{
      const btn=document.createElement('button');
      btn.className='pl-btn';
      btn.disabled = busy || !pl.enabled || !pl.configured;
      btn.innerHTML = `${pl.name}<small>${pl.enabled ? (pl.configured ? '' : 'Configure in plugin settings') : 'Disabled'}</small>`;
      btn.addEventListener('click', async ()=>{
        if(btn.disabled) return;
        busy = true;
        try{
          const res = await fetch('/api/spotify/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({slot:pl.slot})});
          const json = await res.json();
          showFeedback(json.message || json.error || 'Request finished.', !!json.ok);
        }catch(e){
          showFeedback('Spotify add failed: ' + (e.message || e), false);
        }finally{ busy = false; refresh(); }
      });
      els.playlists.appendChild(btn);
    });
  }

  function render(state){
    const t = (state && state.track) || null;
    const hasTrack = !!(t && t.title);
    els.trackTitle.textContent = hasTrack ? t.title : 'Waiting for metadata...';
    els.trackArtist.textContent = hasTrack ? (t.artist || t.station || '—') : 'No active track detected yet.';
    els.metaTrack.textContent = hasTrack ? t.title : 'Waiting for metadata...';
    els.metaArtist.textContent = hasTrack ? (t.artist || '—') : '—';
    els.metaStation.textContent = hasTrack ? (t.station || '—') : '—';
    els.metaService.textContent = hasTrack ? (t.service || '—') : '—';
    els.metaState.textContent = hasTrack ? (t.status || '—') : '—';
    els.svcPill.textContent = 'Service: ' + (hasTrack ? (t.service || '—') : '—');
    els.stationPill.textContent = 'Station: ' + (hasTrack ? (t.station || '—') : '—');

    const sp = (state && state.spotify) || {};
    if (sp.connected) {
      if (sp.match) {
        els.spotifyPill.textContent = 'Spotify ' + Math.round(sp.match.confidence || 0) + '%';
        els.spotifyPill.className = 'pill ok';
      } else if (sp.error) {
        els.spotifyPill.textContent = sp.error;
        els.spotifyPill.className = 'pill warn';
      } else {
        els.spotifyPill.textContent = 'Spotify connected';
        els.spotifyPill.className = 'pill ok';
      }
    } else {
      els.spotifyPill.textContent = 'Spotify not connected';
      els.spotifyPill.className = 'pill';
    }

    const lyrMode = state && state.lyrics && state.lyrics.mode;
    if (lyrMode === 'synced') {
      els.lyricsPill.textContent = 'Lyrics synced';
      els.lyricsPill.className = 'pill ok';
    } else if (lyrMode === 'plain') {
      els.lyricsPill.textContent = 'Lyrics plain';
      els.lyricsPill.className = 'pill';
    } else {
      els.lyricsPill.textContent = 'Lyrics';
      els.lyricsPill.className = 'pill';
    }

    setArt(hasTrack ? (t.albumart || '') : '');
    if(sp.match){
      els.spotifyMatchWrap.classList.remove('hidden');
      els.spotifyMatchText.textContent = `${sp.match.artist} · ${sp.match.title} · confidence ${sp.match.confidence}`;
    } else {
      els.spotifyMatchWrap.classList.add('hidden');
    }
    renderLyrics(state || {});
    renderPlaylists(state || {});
  }

  async function refresh(){
    const seq = ++requestSeq;
    try{
      const res = await fetch('/api/state', {cache:'no-store'});
      if(!res.ok) throw new Error('HTTP ' + res.status);
      const data = await res.json();
      if(seq === requestSeq) render(data);
    }catch(e){
      console.error('Overlay refresh failed:', e.message || e);
    }
  }

  async function adjustOffset(delta){
    try{
      await fetch('/api/lyrics/offset',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({delta:delta})
      });
      refresh();
    }catch(e){
      console.error('Offset update failed:', e.message || e);
    }
  }

  if (els.offsetMinus) els.offsetMinus.addEventListener('click', ()=>adjustOffset(-100));
  if (els.offsetPlus) els.offsetPlus.addEventListener('click', ()=>adjustOffset(100));
  if (els.singAlongBtn && els.singAlongModal) els.singAlongBtn.addEventListener('click', ()=>{
    els.singAlongModal.classList.remove('hidden');
    document.body.style.overflow='hidden';
  });
  if (els.singAlongClose && els.singAlongModal) els.singAlongClose.addEventListener('click', ()=>{
    els.singAlongModal.classList.add('hidden');
    document.body.style.overflow='';
  });
  if (els.singAlongModal) els.singAlongModal.addEventListener('click', (ev)=>{
    if(ev.target === els.singAlongModal){
      els.singAlongModal.classList.add('hidden');
      document.body.style.overflow='';
    }
  });
  document.addEventListener('keydown', (ev)=>{
    if(ev.key === 'Escape' && els.singAlongModal && !els.singAlongModal.classList.contains('hidden')){
      els.singAlongModal.classList.add('hidden');
      document.body.style.overflow='';
    }
  });

  refresh();
  setInterval(refresh, 1000);
})();
