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
    playlistFeedback: document.getElementById('playlistFeedback')
  };
  let busy = false;
  function showFeedback(text, ok){
    els.playlistFeedback.className='feedback ' + (ok ? 'ok':'bad');
    els.playlistFeedback.textContent=text;
    els.playlistFeedback.classList.remove('hidden');
  }
  function setArt(url){
    els.artBox.innerHTML='';
    if(url){
      const img=document.createElement('img');
      img.src=url;
      img.alt='Track art';
      img.onerror=function(){els.artBox.innerHTML='<div class="art-fallback">No image</div>';};
      els.artBox.appendChild(img);
    } else {
      els.artBox.innerHTML='<div class="art-fallback">No image</div>';
    }
  }
  function renderLyrics(data){
    const lyrics = data && data.lyrics;
    if(!lyrics){
      els.lyrics.className='lyrics-empty';
      els.lyrics.innerHTML='The overlay is running. As soon as Volumio publishes artist and title metadata, lyrics will appear here.';
      return;
    }
    const lines = lyrics.lines || [];
    if(!lines.length){
      els.lyrics.className='lyrics-empty';
      els.lyrics.textContent = lyrics.text || 'No lyrics found for the current metadata.';
      return;
    }
    els.lyrics.className='';
    els.lyrics.innerHTML='';
    const activeIndex = typeof lyrics.activeIndex === 'number' ? lyrics.activeIndex : -1;
    lines.forEach((line, idx)=>{
      const div=document.createElement('div');
      div.className='lyrics-line'+(idx===activeIndex?' active':'');
      div.textContent=line.text || '';
      els.lyrics.appendChild(div);
      if(idx===activeIndex){ requestAnimationFrame(()=>{ div.scrollIntoView({block:'center',behavior:'smooth'}); }); }
    });
  }
  function renderPlaylists(state){
    els.playlists.innerHTML='';
    (state.playlists || []).forEach(pl=>{
      const btn=document.createElement('button');
      btn.className='pl-btn';
      btn.disabled = busy || !pl.enabled || !pl.configured;
      btn.innerHTML = `${pl.name}<small>${pl.enabled ? (pl.configured ? 'Add current match' : 'Configure in plugin settings') : 'Disabled'}</small>`;
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
    const t = state.track || {};
    els.trackTitle.textContent = t.title || 'Waiting for metadata...';
    els.trackArtist.textContent = t.artist || 'No active track detected yet.';
    els.metaTrack.textContent = t.title || 'Waiting for metadata...';
    els.metaArtist.textContent = t.artist || '—';
    els.metaStation.textContent = t.station || '—';
    els.metaService.textContent = t.service || '—';
    els.metaState.textContent = t.status || '—';
    els.svcPill.textContent = 'Service: ' + (t.service || '—');
    els.stationPill.textContent = 'Station: ' + (t.station || '—');
    const sp = state.spotify || {};
    els.spotifyPill.textContent = sp.connected ? 'Spotify connected' : 'Spotify not connected';
    els.spotifyPill.className = 'pill ' + (sp.connected ? 'ok' : '');
    els.lyricsPill.textContent = state.lyrics && state.lyrics.mode === 'synced' ? 'Synced lyrics' : 'Lyrics';
    setArt(t.albumart || '');
    if(sp.match){
      els.spotifyMatchWrap.classList.remove('hidden');
      els.spotifyMatchText.textContent = `${sp.match.artist} · ${sp.match.title} · confidence ${sp.match.confidence}`;
    } else {
      els.spotifyMatchWrap.classList.add('hidden');
    }
    renderLyrics(state);
    renderPlaylists(state);
  }
  async function refresh(){
    try{
      const res = await fetch('/api/state',{cache:'no-store'});
      if(!res.ok) throw new Error('HTTP '+res.status);
      const data = await res.json();
      render(data);
    }catch(e){
      console.error('Overlay refresh failed:', e.message || e);
    }
  }
  refresh();
  setInterval(refresh, 2500);
})();
