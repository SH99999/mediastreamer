'use strict';

var libQ = require('kew');
var vConf = require('v-conf');
var express = require('express');
var cors = require('cors');
var fetch = require('node-fetch');
var path = require('path');
var fs = require('fs');
var childProcess = require('child_process');
var https = require('https');
var http = require('http');
var crypto = require('crypto');
var io = require('socket.io-client');

function ControllerRadioScaleOverlayBridge(context) {
  this.context = context;
  this.commandRouter = context.coreCommand;
  this.logger = context.logger;
  this.config = null;
  this.configFilePath = null;
  this.app = null;
  this.httpServer = null;
  this.httpsServer = null;
  this.listenerState = { httpRunning: false, httpsRunning: false, httpError: '', httpsError: '', certReady: false, certError: '' };
  this.volumioSocket = null;
  this.pollTimer = null;
  this.lyricsTimer = null;
  this.fetchInFlight = false;
  this.spotifyLookupInFlight = false;
  this.state = {
    volumioState: {},
    track: null,
    lyrics: null,
    lastUpdatedAt: 0,
    playback: { trackKey: null, positionMs: 0, anchorTs: 0, status: null },
    spotify: { connected: false, userId: null, match: null, error: null, rateLimitedUntil: 0, lookupTrackKey: null }
  };
  this.cache = { lyrics: new Map(), spotifyMatch: new Map() };
}

ControllerRadioScaleOverlayBridge.prototype.onVolumioStart = function() {
  var configFile = this.commandRouter.pluginManager.getConfigurationFile(this.context, 'config.json');
  this.configFilePath = configFile;
  this.config = new vConf();
  this.config.loadFile(configFile);
  this.ensureConfigWritable(configFile);
  this.ensureConfigDefaults();
  this.log('info', 'Using config file: ' + configFile);
  return libQ.resolve();
};

ControllerRadioScaleOverlayBridge.prototype.onStart = function() {
  return this.startBridge();
};

ControllerRadioScaleOverlayBridge.prototype.onStop = function() {
  return this.stopBridge();
};

ControllerRadioScaleOverlayBridge.prototype.getConfigurationFiles = function() { return ['config.json']; };

ControllerRadioScaleOverlayBridge.prototype.ensureConfigWritable = function(configFile) {
  try { fs.chmodSync(configFile, 0o664); } catch (e) {}
  try { childProcess.execFileSync('chown', ['volumio:volumio', configFile], { stdio: 'ignore' }); } catch (e) {}
  try {
    var dir = path.dirname(configFile);
    fs.chmodSync(dir, 0o755);
    childProcess.execFileSync('chown', ['volumio:volumio', dir], { stdio: 'ignore' });
  } catch (e) {}
};

ControllerRadioScaleOverlayBridge.prototype.ensureConfigDefaults = function() {
  var defaults = {
    enabled: true,
    port: 5511,
    httpsPort: 5443,
    publicHost: '',
    overlayWidthPercent: 36,
    lyricsEnabled: true,
    preferSyncedLyrics: true,
    lyricsCacheTtlSeconds: 21600,
    lyricsSyncOffsetMs: 0,
    scaleRadioEnabled: true,
    funModeEnabled: true,
    playNowEnabled: false,
    spotifyClientId: '',
    spotifyScopes: 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public',
    spotifyAccessToken: '',
    spotifyRefreshToken: '',
    spotifyTokenExpiresAt: 0,
    spotifyAuthorizedUserId: '',
    pkceVerifier: '',
    pkceState: '',
    playlistSlot1Enabled: true,
    playlistSlot1Name: 'Scale Radio 1',
    playlistSlot1Id: '',
    playlistSlot2Enabled: true,
    playlistSlot2Name: 'Scale Radio 2',
    playlistSlot2Id: '',
    playlistSlot3Enabled: false,
    playlistSlot3Name: 'Fun Mode 1',
    playlistSlot3Id: '',
    playlistSlot4Enabled: false,
    playlistSlot4Name: 'Fun Mode 2',
    playlistSlot4Id: '',
    debugLogging: false
  };
  var changed = false;
  for (var key in defaults) {
    var val = this.config.get(key);
    if (val === undefined || val === null) {
      this.config.set(key, defaults[key]);
      changed = true;
    }
  }
  if (changed) { this.saveConfig(); }
  this.updateSpotifyConnectedState();
};

ControllerRadioScaleOverlayBridge.prototype.getUIConfig = function() {
  var uiPath = path.join(__dirname, 'UIConfig.json');
  var uiconf = JSON.parse(fs.readFileSync(uiPath, 'utf8'));
  var self = this;
  function item(sectionId, contentId) {
    var section = uiconf.sections.find(function(s){ return s.id === sectionId; });
    return section && section.content ? section.content.find(function(c){ return c.id === contentId; }) : null;
  }
  function setValue(sectionId, contentId, value) { var it = item(sectionId, contentId); if (it) { it.value = value; } }
  setValue('s_service','publicHost', self.getPublicHost());
  setValue('s_service','port', self.getConf('port'));
  setValue('s_service','httpsPort', self.getConf('httpsPort'));
  setValue('s_service','overlayWidthPercent', self.getConf('overlayWidthPercent'));
  setValue('s_service','debugLogging', self.getConf('debugLogging'));
  setValue('s_service_status','overlayUrl', self.getOverlayUrl());
  setValue('s_service_status','secureUrl', self.getSecureBaseUrl());
  setValue('s_service_status','redirectUri', self.getRedirectUri());
  setValue('s_service_status','listenerStatus', self.getListenerStatusText());
  var preview = item('s_service_status','previewButton');
  if (preview && preview.onClick) { preview.onClick.url = self.getOverlayUrl(); }
  setValue('s_targets','scaleRadioEnabled', self.getConf('scaleRadioEnabled'));
  setValue('s_targets','funModeEnabled', self.getConf('funModeEnabled'));
  setValue('s_targets','playNowEnabled', self.getConf('playNowEnabled'));
  setValue('s_lyrics','lyricsEnabled', self.getConf('lyricsEnabled'));
  setValue('s_lyrics','preferSyncedLyrics', self.getConf('preferSyncedLyrics'));
  setValue('s_lyrics','lyricsCacheTtlSeconds', self.getConf('lyricsCacheTtlSeconds'));
  setValue('s_lyrics','lyricsSyncOffsetMs', self.getConf('lyricsSyncOffsetMs'));
  setValue('s_spotify','spotifyClientId', self.getConf('spotifyClientId'));
  setValue('s_spotify_status','redirectUri2', self.getRedirectUri());
  setValue('s_spotify_status','authStartUrl', self.getAuthStartUrl());
  setValue('s_spotify_status','authStatus', self.getSpotifyStatusText());
  var connect = item('s_spotify_status','connectSpotify');
  if (connect && connect.onClick) { connect.onClick.url = self.getAuthStartUrl(); }
  for (var i = 1; i <= 4; i++) {
    setValue('s_pl_' + i, 'playlistSlot' + i + 'Enabled', self.getConf('playlistSlot' + i + 'Enabled'));
    setValue('s_pl_' + i, 'playlistSlot' + i + 'Name', self.getConf('playlistSlot' + i + 'Name'));
    setValue('s_pl_' + i, 'playlistSlot' + i + 'Id', self.getConf('playlistSlot' + i + 'Id'));
  }
  return libQ.resolve(uiconf);
};

ControllerRadioScaleOverlayBridge.prototype.getConf = function(key) { return this.config.get(key); };
ControllerRadioScaleOverlayBridge.prototype.setConf = function(key, value) { this.config.set(key, value); };
ControllerRadioScaleOverlayBridge.prototype.saveConfig = function() {
  this.config.save();
  if (this.configFilePath) {
    this.ensureConfigWritable(this.configFilePath);
  }
};
ControllerRadioScaleOverlayBridge.prototype.getPublicHost = function() {
  return (this.getConf('publicHost') || '').trim();
};
ControllerRadioScaleOverlayBridge.prototype.getOverlayUrl = function() {
  var host = this.getPublicHost() || '127.0.0.1';
  return 'http://' + host + ':' + this.getConf('port') + '/';
};
ControllerRadioScaleOverlayBridge.prototype.getSecureBaseUrl = function() {
  var host = this.getPublicHost() || '127.0.0.1';
  return 'https://' + host + ':' + this.getConf('httpsPort') + '/';
};
ControllerRadioScaleOverlayBridge.prototype.getRedirectUri = function() {
  return this.getSecureBaseUrl() + 'callback';
};
ControllerRadioScaleOverlayBridge.prototype.getAuthStartUrl = function() {
  return this.getSecureBaseUrl() + 'auth/start';
};
ControllerRadioScaleOverlayBridge.prototype.getPluginVersion = function() {
  try { return require(path.join(__dirname, 'package.json')).version; } catch (e) { return '0.2.2-c2'; }
};
ControllerRadioScaleOverlayBridge.prototype.getListenerStatusText = function() {
  var parts = [];
  parts.push(this.listenerState.httpRunning ? 'HTTP running' : ('HTTP stopped' + (this.listenerState.httpError ? ': ' + this.listenerState.httpError : '')));
  parts.push(this.listenerState.httpsRunning ? 'HTTPS running' : ('HTTPS stopped' + (this.listenerState.httpsError ? ': ' + this.listenerState.httpsError : '')));
  parts.push(this.listenerState.certReady ? 'cert ready' : ('cert missing' + (this.listenerState.certError ? ': ' + this.listenerState.certError : '')));
  return parts.join(' | ');
};
ControllerRadioScaleOverlayBridge.prototype.getSpotifyStatusText = function() {
  if (!this.getConf('spotifyClientId')) return 'Client ID not configured';
  if (this.getConf('spotifyAuthorizedUserId')) return 'Connected as ' + this.getConf('spotifyAuthorizedUserId');
  if (this.state.spotify.error) return 'Not connected (' + this.state.spotify.error + ')';
  return 'Not connected';
};
ControllerRadioScaleOverlayBridge.prototype.log = function(level, msg) {
  var fn = this.logger && this.logger[level] ? this.logger[level] : console.log;
  fn.call(this.logger || console, '[radioscale_overlay_bridge] ' + msg);
};
ControllerRadioScaleOverlayBridge.prototype.toast = function(type, message) {
  try { this.commandRouter.pushToastMessage(type, 'RSOB ' + this.getPluginVersion(), message); } catch (e) {}
};

ControllerRadioScaleOverlayBridge.prototype.startBridge = function() {
  var self = this;
  return libQ.resolve().then(function() {
    return self.stopBridge();
  }).then(function() {
    self.createApp();
    self.startHttpServer();
    self.startHttpsServer();
    self.startVolumioConnector();
    self.pollOnce();
    self.pollTimer = setInterval(function() { self.pollOnce(); }, 5000);
    self.lyricsTimer = setInterval(function() { self.updateActiveLyricsIndex(); }, 1000);
    self.updateSpotifyConnectedState();
  });
};

ControllerRadioScaleOverlayBridge.prototype.stopBridge = function() {
  if (this.pollTimer) { clearInterval(this.pollTimer); this.pollTimer = null; }
  if (this.lyricsTimer) { clearInterval(this.lyricsTimer); this.lyricsTimer = null; }
  if (this.volumioSocket) {
    try { this.volumioSocket.removeAllListeners(); this.volumioSocket.close(); } catch (e) {}
    this.volumioSocket = null;
  }
  if (this.httpServer) {
    try { this.httpServer.close(); } catch (e) {}
    this.httpServer = null;
  }
  if (this.httpsServer) {
    try { this.httpsServer.close(); } catch (e) {}
    this.httpsServer = null;
  }
  this.listenerState.httpRunning = false;
  this.listenerState.httpsRunning = false;
  this.listenerState.httpError = '';
  this.listenerState.httpsError = '';
  return libQ.resolve();
};

ControllerRadioScaleOverlayBridge.prototype.createApp = function() {
  var self = this;
  var app = express();
  app.use(cors());
  app.use(express.json({ limit: '1mb' }));
  app.use(express.static(path.join(__dirname, 'public')));
  app.get('/api/state', function(req, res) {
    res.json(self.buildStatePayload());
  });
  app.get('/api/spotify/auth/status', function(req, res) {
    res.json({
      connected: !!self.getConf('spotifyAuthorizedUserId'),
      userId: self.getConf('spotifyAuthorizedUserId') || null,
      redirectUri: self.getRedirectUri(),
      authStartUrl: self.getAuthStartUrl(),
      clientIdConfigured: !!self.getConf('spotifyClientId'),
      error: self.state.spotify.error || null,
      rateLimitedUntil: self.state.spotify.rateLimitedUntil || 0
    });
  });
  app.get('/auth/start', function(req, res) {
    var authData = self.createSpotifyAuthorizeUrl();
    if (!authData.ok) return res.status(400).send(authData.error);
    res.redirect(authData.url);
  });
  app.get('/callback', async function(req, res) {
    try {
      await self.handleSpotifyCallback(req.query);
      res.setHeader('Content-Type', 'text/html; charset=utf-8');
      res.end('<html><body style="font-family:Arial;padding:24px;background:#111;color:#eee"><h2>Spotify connected (' + self.escapeHtml(self.getPluginVersion()) + ')</h2><p>You can close this window and return to Volumio.</p><p><a href="' + self.escapeHtml(self.getOverlayUrl()) + '">Open overlay</a></p></body></html>');
    }
    catch (error) {
      self.state.spotify.error = error.message;
      res.status(500).setHeader('Content-Type', 'text/html; charset=utf-8');
      res.end('<html><body style="font-family:Arial;padding:24px;background:#111;color:#eee"><h2>Spotify connection failed</h2><p>' + self.escapeHtml(error.message) + '</p></body></html>');
    }
  });
  app.get('/api/spotify/match', function(req, res) {
    res.json(self.state.spotify.match || { ok: false, reason: 'no-match' });
  });
  app.post('/api/spotify/add', async function(req, res) {
    try {
      var result = await self.addCurrentTrackToPlaylist(req.body || {});
      res.json(result);
    } catch (error) {
      res.status(500).json({ ok: false, error: error.message });
    }
  });
  app.get('*', function(req, res, next) {
    if (req.path.indexOf('/api/') === 0 || req.path === '/auth/start' || req.path === '/callback') {
      return next();
    }
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
  });
  this.app = app;
};

ControllerRadioScaleOverlayBridge.prototype.startHttpServer = function() {
  var self = this;
  this.httpServer = http.createServer(this.app);
  this.httpServer.listen(this.getConf('port'), '0.0.0.0', function() {
    self.listenerState.httpRunning = true;
    self.listenerState.httpError = '';
    self.log('info', 'HTTP listener started on port ' + self.getConf('port'));
  });
  this.httpServer.on('error', function(err) {
    self.listenerState.httpRunning = false;
    self.listenerState.httpError = err && err.message ? err.message : String(err);
    self.log('error', 'HTTP listener failed: ' + self.listenerState.httpError);
  });
};

ControllerRadioScaleOverlayBridge.prototype.ensureHttpsCertificate = function() {
  var cfgDir = path.dirname(this.configFilePath || path.join('/data/configuration/user_interface/radioscale_overlay_bridge', 'config.json'));
  var crt = path.join(cfgDir, 'spotify-auth.crt');
  var key = path.join(cfgDir, 'spotify-auth.key');
  if (fs.existsSync(crt) && fs.existsSync(key)) {
    this.listenerState.certReady = true;
    this.listenerState.certError = '';
    return { crt: crt, key: key };
  }
  try {
    fs.mkdirSync(cfgDir, { recursive: true });
    var subj = '/CN=' + (this.getPublicHost() || '127.0.0.1');
    childProcess.execFileSync('openssl', [
      'req', '-x509', '-newkey', 'rsa:2048', '-sha256', '-nodes',
      '-keyout', key, '-out', crt, '-days', '3650', '-subj', subj
    ], { stdio: 'ignore' });
    try { childProcess.execFileSync('chown', ['volumio:volumio', crt, key], { stdio: 'ignore' }); } catch (e) {}
    try { fs.chmodSync(crt, 0o644); fs.chmodSync(key, 0o600); } catch (e) {}
    this.listenerState.certReady = true;
    this.listenerState.certError = '';
    return { crt: crt, key: key };
  } catch (e) {
    this.listenerState.certReady = false;
    this.listenerState.certError = e && e.message ? e.message : String(e);
    this.log('warn', 'HTTPS certificate generation failed: ' + this.listenerState.certError);
    return null;
  }
};

ControllerRadioScaleOverlayBridge.prototype.startHttpsServer = function() {
  var self = this;
  var cert = this.ensureHttpsCertificate();
  if (!cert) {
    self.listenerState.httpsRunning = false;
    self.listenerState.httpsError = self.listenerState.certError || 'certificate missing';
    return;
  }
  try {
    var options = {
      cert: fs.readFileSync(cert.crt),
      key: fs.readFileSync(cert.key)
    };
    this.httpsServer = https.createServer(options, this.app);
    this.httpsServer.listen(this.getConf('httpsPort'), '0.0.0.0', function() {
      self.listenerState.httpsRunning = true;
      self.listenerState.httpsError = '';
      self.log('info', 'HTTPS listener started on port ' + self.getConf('httpsPort'));
    });
    this.httpsServer.on('error', function(err) {
      self.listenerState.httpsRunning = false;
      self.listenerState.httpsError = err && err.message ? err.message : String(err);
      self.log('warn', 'HTTPS listener failed: ' + self.listenerState.httpsError);
    });
  } catch (e) {
    this.listenerState.httpsRunning = false;
    this.listenerState.httpsError = e && e.message ? e.message : String(e);
  }
};

ControllerRadioScaleOverlayBridge.prototype.startVolumioConnector = function() {
  var self = this;
  if (this.volumioSocket) {
    try { this.volumioSocket.removeAllListeners(); this.volumioSocket.close(); } catch (e) {}
  }
  var socket = io('http://127.0.0.1:3000', {
    transports: ['websocket'],
    reconnection: true,
    reconnectionAttempts: Infinity,
    reconnectionDelay: 1500,
    timeout: 5000
  });
  this.volumioSocket = socket;
  socket.on('connect', function() {
    self.log('info', 'Volumio socket connected');
    self.pollOnce();
  });
  socket.on('disconnect', function(reason) {
    self.log('warn', 'Volumio socket disconnected: ' + reason);
  });
  socket.on('pushState', function(state) {
    self.handleVolumioState(state);
  });
  socket.on('connect_error', function(err) {
    self.log('warn', 'Volumio socket connect error: ' + (err && err.message ? err.message : String(err)));
  });
};

ControllerRadioScaleOverlayBridge.prototype.pollOnce = function() {
  var self = this;
  if (this.fetchInFlight) { return; }
  this.fetchInFlight = true;
  fetch('http://127.0.0.1:3000/api/v1/getState', { timeout: 5000 }).then(function(res) {
    return res.json();
  }).then(function(state) {
    self.handleVolumioState(state);
  }).catch(function(err) {
    self.log('warn', 'State poll failed: ' + (err && err.message ? err.message : String(err)));
  }).finally(function() {
    self.fetchInFlight = false;
  });
};

ControllerRadioScaleOverlayBridge.prototype.normalizeTrack = function(state) {
  if (!state || typeof state !== 'object') { return null; }
  var rawTitle = (state.title || '').trim();
  var rawArtist = (state.artist || '').trim();
  var service = (state.service || state.stream || '').toString();
  var station = rawArtist || '';
  var artist = rawArtist;
  var title = rawTitle;
  if (state.trackType === 'webradio' || service === 'webradio' || state.stream === true) {
    var parts = this.parseRadioTitle(rawTitle);
    if (parts) {
      artist = parts.artist;
      title = parts.title;
    }
  }
  if (!title) { return null; }
  return {
    key: ((artist || '') + '|' + title).toLowerCase(),
    title: title,
    artist: artist || station || '',
    station: station || '',
    service: service || '',
    albumart: state.albumart || '',
    status: state.status || '',
    trackType: state.trackType || ''
  };
};

ControllerRadioScaleOverlayBridge.prototype.parseRadioTitle = function(rawTitle) {
  if (!rawTitle) { return null; }
  var separators = [' - ', ' – ', ' — ', ' | ', ' ~ '];
  for (var i = 0; i < separators.length; i++) {
    var sep = separators[i];
    if (rawTitle.indexOf(sep) > 0) {
      var parts = rawTitle.split(sep);
      if (parts.length >= 2) {
        return { artist: parts.shift().trim(), title: parts.join(sep).trim() };
      }
    }
  }
  return null;
};

ControllerRadioScaleOverlayBridge.prototype.handleVolumioState = function(state) {
  this.state.volumioState = state || {};
  this.state.lastUpdatedAt = Date.now();
  var normalized = this.normalizeTrack(state || {});
  var previousKey = this.state.track && this.state.track.key;
  this.state.track = normalized;
  if (normalized) {
    this.state.playback.trackKey = normalized.key;
    this.state.playback.anchorTs = Date.now();
    this.state.playback.positionMs = state.seek || 0;
    this.state.playback.status = state.status || '';
    if (normalized.key !== previousKey) {
      this.fetchLyrics(normalized);
      this.scheduleSpotifyLookup(normalized, true);
    } else {
      this.updateActiveLyricsIndex();
    }
  } else {
    this.state.spotify.match = null;
  }
};

ControllerRadioScaleOverlayBridge.prototype.fetchLyrics = function(track) {
  var self = this;
  if (!this.getConf('lyricsEnabled')) {
    this.state.lyrics = null;
    return;
  }
  var cacheKey = track.key;
  var cached = this.cache.lyrics.get(cacheKey);
  var ttlMs = Math.max(60, parseInt(this.getConf('lyricsCacheTtlSeconds'), 10) || 21600) * 1000;
  if (cached && (Date.now() - cached.ts) < ttlMs) {
    this.state.lyrics = JSON.parse(JSON.stringify(cached.value));
    this.updateActiveLyricsIndex();
    return;
  }
  var url = 'https://lrclib.net/api/search?track_name=' + encodeURIComponent(track.title) + '&artist_name=' + encodeURIComponent(track.artist || '');
  fetch(url, { timeout: 6000, headers: { 'User-Agent': 'RSOB/0.2.2-c2' } }).then(function(res) {
    return res.json();
  }).then(function(items) {
    var lyrics = self.pickLyrics(items || []);
    self.state.lyrics = lyrics;
    self.cache.lyrics.set(cacheKey, { ts: Date.now(), value: JSON.parse(JSON.stringify(lyrics)) });
    self.updateActiveLyricsIndex();
  }).catch(function(err) {
    self.log('warn', 'Lyrics fetch failed: ' + (err && err.message ? err.message : String(err)));
    self.state.lyrics = null;
  });
};

ControllerRadioScaleOverlayBridge.prototype.pickLyrics = function(items) {
  if (!items.length) { return null; }
  var preferSynced = !!this.getConf('preferSyncedLyrics');
  var chosen = preferSynced ? (items.find(function(it){ return !!it.syncedLyrics; }) || items[0]) : items[0];
  var synced = chosen.syncedLyrics || '';
  if (preferSynced && synced) {
    return { mode: 'synced', text: chosen.plainLyrics || '', lines: this.parseSyncedLyrics(synced), activeIndex: -1 };
  }
  return { mode: 'plain', text: chosen.plainLyrics || synced || '', lines: [], activeIndex: -1 };
};

ControllerRadioScaleOverlayBridge.prototype.parseSyncedLyrics = function(text) {
  return String(text || '').split(/\r?\n/).map(function(line) {
    var m = line.match(/^\[(\d+):(\d+(?:\.\d+)?)\](.*)$/);
    if (!m) { return null; }
    var sec = parseInt(m[1], 10) * 60 + parseFloat(m[2]);
    return { timeMs: Math.round(sec * 1000), text: (m[3] || '').trim() };
  }).filter(Boolean);
};

ControllerRadioScaleOverlayBridge.prototype.updateActiveLyricsIndex = function() {
  var lyrics = this.state.lyrics;
  if (!lyrics || lyrics.mode !== 'synced' || !lyrics.lines || !lyrics.lines.length) { return; }
  var status = this.state.playback.status;
  var pos = this.state.playback.positionMs || 0;
  if (status === 'play') {
    pos += Date.now() - (this.state.playback.anchorTs || Date.now());
  }
  pos += parseInt(this.getConf('lyricsSyncOffsetMs'), 10) || 0;
  var active = -1;
  for (var i = 0; i < lyrics.lines.length; i++) {
    if (pos >= lyrics.lines[i].timeMs) { active = i; } else { break; }
  }
  lyrics.activeIndex = active;
};

ControllerRadioScaleOverlayBridge.prototype.normalizeString = function(s) {
  return String(s || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '').replace(/[’'`]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
};
ControllerRadioScaleOverlayBridge.prototype.stripTitleDecorations = function(title) {
  return String(title || '')
    .replace(/\((?:19|20)\d{2}\)$/i, '')
    .replace(/\((?:live|remaster(?:ed)?|radio edit|album version|mono|stereo)\)/ig, '')
    .replace(/\[[^\]]+\]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
};
ControllerRadioScaleOverlayBridge.prototype.updateSpotifyConnectedState = function() {
  this.state.spotify.connected = !!(this.getConf('spotifyAccessToken') && this.getConf('spotifyAuthorizedUserId'));
  this.state.spotify.userId = this.getConf('spotifyAuthorizedUserId') || null;
};
ControllerRadioScaleOverlayBridge.prototype.createSpotifyAuthorizeUrl = function() {
  var clientId = (this.getConf('spotifyClientId') || '').trim();
  if (!clientId) return { ok: false, error: 'Spotify Client ID is not configured.' };
  if (!this.listenerState.httpsRunning) return { ok: false, error: 'Spotify HTTPS listener is not running.' };
  var verifier = this.randomString(64);
  var challenge = this.base64Url(crypto.createHash('sha256').update(verifier).digest());
  var state = this.randomString(24);
  this.setConf('pkceVerifier', verifier);
  this.setConf('pkceState', state);
  this.saveConfig();
  var params = new URLSearchParams({
    client_id: clientId,
    response_type: 'code',
    redirect_uri: this.getRedirectUri(),
    code_challenge_method: 'S256',
    code_challenge: challenge,
    state: state,
    scope: this.getConf('spotifyScopes') || ''
  });
  return { ok: true, url: 'https://accounts.spotify.com/authorize?' + params.toString() };
};
ControllerRadioScaleOverlayBridge.prototype.handleSpotifyCallback = async function(query) {
  if (!query || query.error) throw new Error(query && query.error ? String(query.error) : 'Missing callback query');
  if ((query.state || '') !== (this.getConf('pkceState') || '')) throw new Error('Spotify PKCE state mismatch.');
  var code = query.code || '';
  if (!code) throw new Error('Missing Spotify authorization code.');
  var verifier = this.getConf('pkceVerifier') || '';
  if (!verifier) throw new Error('Missing Spotify PKCE verifier.');
  var body = new URLSearchParams({
    client_id: this.getConf('spotifyClientId') || '',
    grant_type: 'authorization_code',
    code: code,
    redirect_uri: this.getRedirectUri(),
    code_verifier: verifier
  });
  var res = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
    timeout: 10000
  });
  var json = await res.json();
  if (!res.ok || !json.access_token) throw new Error((json && json.error_description) || (json && json.error) || ('Spotify token error HTTP ' + res.status));
  this.setConf('spotifyAccessToken', json.access_token || '');
  this.setConf('spotifyRefreshToken', json.refresh_token || this.getConf('spotifyRefreshToken') || '');
  this.setConf('spotifyTokenExpiresAt', Date.now() + ((json.expires_in || 3600) * 1000));
  this.setConf('pkceVerifier', '');
  this.setConf('pkceState', '');
  this.saveConfig();
  var me = await this.spotifyFetchJson('https://api.spotify.com/v1/me');
  this.setConf('spotifyAuthorizedUserId', me && me.id ? me.id : '');
  this.saveConfig();
  this.state.spotify.error = null;
  this.updateSpotifyConnectedState();
  if (this.state.track) this.scheduleSpotifyLookup(this.state.track, true);
};
ControllerRadioScaleOverlayBridge.prototype.spotifyDisconnectAction = function() {
  this.setConf('spotifyAccessToken', '');
  this.setConf('spotifyRefreshToken', '');
  this.setConf('spotifyTokenExpiresAt', 0);
  this.setConf('spotifyAuthorizedUserId', '');
  this.setConf('pkceVerifier', '');
  this.setConf('pkceState', '');
  this.saveConfig();
  this.state.spotify.match = null;
  this.state.spotify.error = null;
  this.state.spotify.rateLimitedUntil = 0;
  this.updateSpotifyConnectedState();
  this.toast('success', 'Spotify authorization removed.');
  return libQ.resolve({ success: true });
};
ControllerRadioScaleOverlayBridge.prototype.ensureSpotifyToken = async function() {
  var access = this.getConf('spotifyAccessToken') || '';
  var exp = parseInt(this.getConf('spotifyTokenExpiresAt'), 10) || 0;
  if (access && Date.now() < (exp - 60000)) return access;
  var refresh = this.getConf('spotifyRefreshToken') || '';
  if (!refresh) return access;
  var body = new URLSearchParams({ client_id: this.getConf('spotifyClientId') || '', grant_type: 'refresh_token', refresh_token: refresh });
  var res = await fetch('https://accounts.spotify.com/api/token', {
    method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body.toString(), timeout: 10000
  });
  var json = await res.json();
  if (!res.ok || !json.access_token) throw new Error((json && json.error_description) || (json && json.error) || ('Spotify refresh HTTP ' + res.status));
  this.setConf('spotifyAccessToken', json.access_token || '');
  if (json.refresh_token) this.setConf('spotifyRefreshToken', json.refresh_token);
  this.setConf('spotifyTokenExpiresAt', Date.now() + ((json.expires_in || 3600) * 1000));
  this.saveConfig();
  this.updateSpotifyConnectedState();
  return this.getConf('spotifyAccessToken') || '';
};
ControllerRadioScaleOverlayBridge.prototype.spotifyFetchJson = async function(url, options) {
  options = options || {};
  if (this.state.spotify.rateLimitedUntil && Date.now() < this.state.spotify.rateLimitedUntil) {
    throw new Error('Spotify backoff active');
  }
  var token = await this.ensureSpotifyToken();
  if (!token) throw new Error('Spotify not connected');
  var headers = Object.assign({}, options.headers || {}, { Authorization: 'Bearer ' + token });
  var res = await fetch(url, Object.assign({}, options, { headers: headers, timeout: options.timeout || 10000 }));
  if (res.status === 429) {
    var retryAfter = parseInt(res.headers.get('retry-after') || '30', 10);
    this.state.spotify.rateLimitedUntil = Date.now() + Math.max(5, retryAfter) * 1000;
    this.state.spotify.error = 'Spotify rate limited';
    throw new Error('Spotify rate limited');
  }
  var json = await res.json();
  if (!res.ok) {
    var msg = (json && json.error && json.error.message) || ('Spotify HTTP ' + res.status);
    throw new Error(msg);
  }
  return json;
};
ControllerRadioScaleOverlayBridge.prototype.scheduleSpotifyLookup = function(track, force) {
  if (!track || !this.getConf('spotifyClientId') || !this.getConf('spotifyAuthorizedUserId')) {
    this.state.spotify.match = null;
    this.updateSpotifyConnectedState();
    return;
  }
  this.updateSpotifyConnectedState();
  if (this.spotifyLookupInFlight) return;
  if (!force && this.state.spotify.lookupTrackKey === track.key) return;
  var self = this;
  this.state.spotify.lookupTrackKey = track.key;
  setTimeout(function() { self.performSpotifyLookup(track).catch(function(){}); }, 10);
};
ControllerRadioScaleOverlayBridge.prototype.performSpotifyLookup = async function(track) {
  if (!track || this.spotifyLookupInFlight) return;
  if (this.state.spotify.rateLimitedUntil && Date.now() < this.state.spotify.rateLimitedUntil) return;
  var cached = this.cache.spotifyMatch.get(track.key);
  if (cached && (Date.now() - cached.ts) < 10 * 60 * 1000) {
    this.state.spotify.match = JSON.parse(JSON.stringify(cached.value));
    return;
  }
  this.spotifyLookupInFlight = true;
  try {
    var variants = this.buildSpotifyQueries(track);
    var best = null;
    for (var i = 0; i < variants.length; i++) {
      var url = 'https://api.spotify.com/v1/search?type=track&limit=5&q=' + encodeURIComponent(variants[i]);
      var json = await this.spotifyFetchJson(url);
      var items = (json && json.tracks && json.tracks.items) || [];
      for (var j = 0; j < items.length; j++) {
        var cand = this.scoreSpotifyItem(track, items[j]);
        if (!best || cand.confidence > best.confidence) best = cand;
      }
      if (best && best.confidence >= 88) break;
    }
    if (best && best.confidence >= 72) {
      this.state.spotify.match = best;
      this.cache.spotifyMatch.set(track.key, { ts: Date.now(), value: JSON.parse(JSON.stringify(best)) });
      this.state.spotify.error = null;
    } else {
      this.state.spotify.match = null;
      this.state.spotify.error = null;
    }
  } catch (e) {
    this.state.spotify.error = e && e.message ? e.message : String(e);
    this.log('warn', 'Spotify lookup failed: ' + this.state.spotify.error);
  } finally {
    this.spotifyLookupInFlight = false;
  }
};
ControllerRadioScaleOverlayBridge.prototype.buildSpotifyQueries = function(track) {
  var title = this.stripTitleDecorations(track.title || '');
  var artist = track.artist || '';
  var list = [];
  function add(q) { if (q && list.indexOf(q) === -1) list.push(q); }
  add('track:"' + title + '" artist:"' + artist + '"');
  add(title + ' ' + artist);
  add('track:"' + title.replace(/\((?:19|20)\d{2}\)$/,'').trim() + '" artist:"' + artist + '"');
  return list.filter(Boolean);
};
ControllerRadioScaleOverlayBridge.prototype.scoreSpotifyItem = function(track, item) {
  var candArtist = ((item.artists && item.artists[0] && item.artists[0].name) || '');
  var candTitle = item.name || '';
  var normTrackArtist = this.normalizeString(track.artist);
  var normTrackTitle = this.normalizeString(this.stripTitleDecorations(track.title));
  var normCandArtist = this.normalizeString(candArtist);
  var normCandTitle = this.normalizeString(this.stripTitleDecorations(candTitle));
  var confidence = 0;
  if (normTrackArtist === normCandArtist) confidence += 45;
  else if (normCandArtist.indexOf(normTrackArtist) >= 0 || normTrackArtist.indexOf(normCandArtist) >= 0) confidence += 30;
  if (normTrackTitle === normCandTitle) confidence += 45;
  else if (normCandTitle.indexOf(normTrackTitle) >= 0 || normTrackTitle.indexOf(normCandTitle) >= 0) confidence += 30;
  return {
    ok: confidence >= 72,
    confidence: confidence,
    id: item.id,
    uri: item.uri,
    title: candTitle,
    artist: candArtist,
    album: item.album && item.album.name ? item.album.name : '',
    albumart: item.album && item.album.images && item.album.images[0] ? item.album.images[0].url : '',
    externalUrl: item.external_urls && item.external_urls.spotify ? item.external_urls.spotify : '',
    releaseDate: item.album && item.album.release_date ? item.album.release_date : ''
  };
};
ControllerRadioScaleOverlayBridge.prototype.parsePlaylistId = function(input) {
  var raw = String(input || '').trim();
  if (!raw) return '';
  var m = raw.match(/playlist[/:]([A-Za-z0-9]+)(?:\?|$)/);
  if (m) return m[1];
  if (raw.indexOf('spotify:playlist:') === 0) return raw.split(':').pop();
  return raw;
};
ControllerRadioScaleOverlayBridge.prototype.isTrackAlreadyInPlaylist = async function(playlistId, trackId) {
  var offset = 0;
  while (offset < 1000) {
    var url = 'https://api.spotify.com/v1/playlists/' + encodeURIComponent(playlistId) + '/tracks?fields=items(track(id)),next&limit=100&offset=' + offset;
    var json = await this.spotifyFetchJson(url);
    var items = json.items || [];
    for (var i = 0; i < items.length; i++) {
      if (items[i] && items[i].track && items[i].track.id === trackId) return true;
    }
    if (!json.next) break;
    offset += 100;
  }
  return false;
};
ControllerRadioScaleOverlayBridge.prototype.addCurrentTrackToPlaylist = async function(body) {
  var slot = parseInt(body.slot || body.playlistSlot || 1, 10);
  if (slot < 1 || slot > 4) slot = 1;
  var enabled = !!this.getConf('playlistSlot' + slot + 'Enabled');
  var name = this.getConf('playlistSlot' + slot + 'Name') || ('Playlist ' + slot);
  var playlistId = this.parsePlaylistId(this.getConf('playlistSlot' + slot + 'Id') || '');
  if (!enabled) return { ok: false, error: 'Playlist slot disabled.' };
  if (!playlistId) return { ok: false, error: 'Playlist slot not configured.' };
  if (!this.state.track) return { ok: false, error: 'No active track.' };
  if (!this.state.spotify.match || this.state.spotify.match.confidence < 72 || this.state.spotify.lookupTrackKey !== this.state.track.key) {
    await this.performSpotifyLookup(this.state.track);
  }
  var match = this.state.spotify.match;
  if (!match || !match.id) return { ok: false, error: 'The bridge did not find a strong enough match for the current radio metadata.' };
  var exists = await this.isTrackAlreadyInPlaylist(playlistId, match.id);
  if (exists) return { ok: true, duplicate: true, added: false, playlist: name, track: match.title, artist: match.artist, message: 'Track already exists in ' + name + '.' };
  var url = 'https://api.spotify.com/v1/playlists/' + encodeURIComponent(playlistId) + '/tracks';
  await this.spotifyFetchJson(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ uris: [match.uri] }) });
  return { ok: true, duplicate: false, added: true, playlist: name, track: match.title, artist: match.artist, message: 'Added to ' + name + '.' };
};

ControllerRadioScaleOverlayBridge.prototype.buildStatePayload = function() {
  this.updateActiveLyricsIndex();
  this.updateSpotifyConnectedState();
  return {
    ok: true,
    plugin: 'radioscale_overlay_bridge',
    version: this.getPluginVersion(),
    release: 'RSOB 0.2.2-c2',
    track: this.state.track,
    lyrics: this.state.lyrics,
    spotify: {
      connected: this.state.spotify.connected,
      userId: this.state.spotify.userId,
      match: this.state.spotify.match,
      error: this.state.spotify.error,
      rateLimitedUntil: this.state.spotify.rateLimitedUntil || 0
    },
    playlists: [1,2,3,4].map(function(i){
      return {
        slot: i,
        enabled: !!this.getConf('playlistSlot'+i+'Enabled'),
        name: this.getConf('playlistSlot'+i+'Name') || ('Playlist '+i),
        configured: !!this.parsePlaylistId(this.getConf('playlistSlot'+i+'Id') || '')
      };
    }, this),
    runtime: {
      httpRunning: this.listenerState.httpRunning,
      httpsRunning: this.listenerState.httpsRunning,
      httpError: this.listenerState.httpError,
      httpsError: this.listenerState.httpsError,
      certReady: this.listenerState.certReady,
      certError: this.listenerState.certError
    },
    lastUpdatedAt: this.state.lastUpdatedAt
  };
};

ControllerRadioScaleOverlayBridge.prototype.randomString = function(len) {
  return this.base64Url(crypto.randomBytes(len)).slice(0, len);
};
ControllerRadioScaleOverlayBridge.prototype.base64Url = function(buf) {
  return Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
};
ControllerRadioScaleOverlayBridge.prototype.escapeHtml = function(s) {
  return String(s || '').replace(/[&<>"']/g, function(ch){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]); });
};
ControllerRadioScaleOverlayBridge.prototype.coerceBoolean = function(v) { return v === true || v === 'true' || v === 1 || v === '1' || v === 'on'; };
ControllerRadioScaleOverlayBridge.prototype.configSaveService = function(data) {
  this.setConf('publicHost', (data.publicHost || '').trim());
  this.setConf('port', parseInt(data.port, 10) || 5511);
  this.setConf('httpsPort', parseInt(data.httpsPort, 10) || 5443);
  this.setConf('overlayWidthPercent', parseInt(data.overlayWidthPercent, 10) || 36);
  this.setConf('debugLogging', this.coerceBoolean(data.debugLogging));
  this.saveConfig();
  return this.restartBridgeAfterConfigChange();
};
ControllerRadioScaleOverlayBridge.prototype.configSaveTargets = function(data) {
  this.setConf('scaleRadioEnabled', this.coerceBoolean(data.scaleRadioEnabled));
  this.setConf('funModeEnabled', this.coerceBoolean(data.funModeEnabled));
  this.setConf('playNowEnabled', this.coerceBoolean(data.playNowEnabled));
  this.saveConfig();
  return libQ.resolve({ success: true });
};
ControllerRadioScaleOverlayBridge.prototype.configSaveLyrics = function(data) {
  this.setConf('lyricsEnabled', this.coerceBoolean(data.lyricsEnabled));
  this.setConf('preferSyncedLyrics', this.coerceBoolean(data.preferSyncedLyrics));
  this.setConf('lyricsCacheTtlSeconds', parseInt(data.lyricsCacheTtlSeconds, 10) || 21600);
  this.setConf('lyricsSyncOffsetMs', parseInt(data.lyricsSyncOffsetMs, 10) || 0);
  this.saveConfig();
  return libQ.resolve({ success: true });
};
ControllerRadioScaleOverlayBridge.prototype.configSaveSpotify = function(data) {
  this.setConf('spotifyClientId', String(data.spotifyClientId || '').trim());
  this.saveConfig();
  this.state.spotify.error = null;
  return libQ.resolve({ success: true });
};
ControllerRadioScaleOverlayBridge.prototype.configSavePlaylists = function(data) {
  for (var i = 1; i <= 4; i++) {
    if (Object.prototype.hasOwnProperty.call(data, 'playlistSlot' + i + 'Enabled')) this.setConf('playlistSlot' + i + 'Enabled', this.coerceBoolean(data['playlistSlot' + i + 'Enabled']));
    if (Object.prototype.hasOwnProperty.call(data, 'playlistSlot' + i + 'Name')) this.setConf('playlistSlot' + i + 'Name', String(data['playlistSlot' + i + 'Name'] || '').trim());
    if (Object.prototype.hasOwnProperty.call(data, 'playlistSlot' + i + 'Id')) this.setConf('playlistSlot' + i + 'Id', String(data['playlistSlot' + i + 'Id'] || '').trim());
  }
  this.saveConfig();
  return libQ.resolve({ success: true });
};
ControllerRadioScaleOverlayBridge.prototype.restartBridgeAfterConfigChange = function() {
  var self = this;
  return self.stopBridge().then(function() { return self.startBridge(); }).then(function() { return { success: true }; });
};

module.exports = ControllerRadioScaleOverlayBridge;
