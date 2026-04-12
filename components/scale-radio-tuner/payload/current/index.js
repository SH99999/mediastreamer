"use strict";

const libQ = require('kew');
const fs = require('fs');
const path = require('path');
const http = require('http');
const { spawn, execSync } = require('child_process');
const vConf = require('v-conf');
const io = require('socket.io-client');

/** Public labels shown to the user. Internal plugin ids stay unchanged for compatibility. */
const PUBLIC_OVERLAY_NAME = 'Scale FM Overlay';
const PUBLIC_SOURCE_LABEL = 'Scale FM';

module.exports = ControllerRadioScalePeppy;

/**
 * Main user_interface plugin for the Scale FM overlay.
 *
 * The internal plugin id remains `radio_scale_peppy` because other plugins,
 * rotary mappings and user configs already reference that id directly.
 * User-facing names were cleaned up for 1.9.0 without breaking those links.
 */
function ControllerRadioScalePeppy(context) {
  this.context = context;
  this.commandRouter = context.coreCommand;
  this.logger = context.logger;
  this.configManager = context.configManager;
  this.config = new vConf();
  this.rendererProcess = null;
  this.pollTimer = null;
  this.lastStateDigest = '';
  this.pluginDir = __dirname;
  this.runtimeDir = path.join(this.pluginDir, 'runtime');
  this.statePath = path.join(this.runtimeDir, 'state.json');
  this.settingsPath = path.join(this.runtimeDir, 'settings.json');
  this.stationCachePath = path.join(this.runtimeDir, 'station_cache.json');
  this.rendererReadyPath = path.join(this.runtimeDir, 'renderer_ready.json');
  this.rendererPidPath = path.join(this.runtimeDir, 'renderer.pid');
  this.sharedOverlayOwnerPath = '/tmp/mediastreamer_active_overlay.json';
  this.rendererOwnedByPlugin = false;
  this.stationCache = {};
  this.stationWarmPromises = {};
  this.preparedStationPayloads = {};
  this.lastWarmFocusKey = null;
  this.stationSourceWatchTimer = null;
  this.stationSourceWatchPaths = [];
  this.stationSourceChangeHandler = null;
  this.hissProcess = null;
  this.hissVariant = null;
  this.hissLoopWanted = false;
  this.hissSyncTimer = null;
  this.overlayOpenedAt = 0;
  this.myWebRadioPath = '/data/favourites/my-web-radio';
  this.externalStationSources = [
    this.myWebRadioPath
  ];
  this.externalStationIndex = [];
  this.seedPlaylistName = 'radioscale_base';
  this.seedPlaylistPath = path.join('/data/playlist', this.seedPlaylistName);
  this.browseSourceUri = 'scalefm';
  this.browseSourceName = PUBLIC_SOURCE_LABEL;
  this.browseSourceRegistered = false;
  this.seedStations = [
    {
      name: 'Hitradio OE3',
      title: 'Hitradio OE3',
      freq: 99.9,
      uri: 'https://orf-live.ors-shoutcast.at/oe3-q2a',
      service: 'webradio',
      type: 'webradio',
      match: ['oe3', 'oe 3', 'hitradio oe3']
    },
    {
      name: 'FM4',
      title: 'FM4',
      freq: 103.8,
      uri: 'https://orf-live.ors-shoutcast.at/fm4-q2a',
      service: 'webradio',
      type: 'webradio',
      match: ['fm4', 'orf fm4']
    },
    {
      name: 'RADIO WIEN',
      title: 'RADIO WIEN',
      freq: 89.9,
      uri: 'https://orf-live.ors-shoutcast.at/wie-q2a',
      service: 'webradio',
      type: 'webradio',
      match: ['radio wien', 'wien', 'orf radio wien']
    },
    {
      name: 'Deep House Radio',
      title: 'Deep House Radio',
      freq: null,
      uri: 'https://streaming.shoutcast.com/dhr',
      service: 'webradio',
      type: 'webradio',
      match: ['deep house radio', 'deep house', 'dhr']
    },
    {
      name: 'CHILLOUT ANTENNE',
      title: 'CHILLOUT ANTENNE',
      freq: null,
      uri: 'https://stream.antenne.de/chillout/stream/mp3',
      service: 'webradio',
      type: 'webradio',
      match: ['chillout antenne', 'antenne bayern chillout', 'chillout']
    },
    {
      name: 'OLDIE ANTENNE',
      title: 'OLDIE ANTENNE',
      freq: null,
      uri: 'https://stream.antenne.de/oldie-antenne/stream/mp3',
      service: 'webradio',
      type: 'webradio',
      match: ['oldie antenne', 'antenne bayern oldies but goldies', 'oldies but goldies']
    },
    {
      name: 'Antenne Kärnten',
      title: 'Antenne Kärnten',
      freq: null,
      uri: 'https://live.antenne.at/ak',
      service: 'webradio',
      type: 'webradio',
      match: ['antenne kärnten', 'antenne karnten']
    },
    {
      name: 'Kronehit',
      title: 'Kronehit',
      freq: 105.8,
      uri: 'https://secureonair.krone.at/kronehit1058.mp3',
      service: 'webradio',
      type: 'webradio',
      match: ['kronehit', 'krone hit']
    }
  ];
  this.tuning = {
    position: null,
    lockedStationKey: null,
    nearestStationKey: null,
    nearestDistance: null,
    noiseLevel: 1,
    autoPlayOnLock: true,
    tuningMode: 'auto',
    controlMode: 'normal',
    lastInteractionTs: 0,
    lastActivatedStationKey: null,
    tuneUnlockPauseApplied: false,
    lastToastKey: '',
    pendingActivation: null,
    lastTuneDirection: 0,
    recentUnlockStationKey: null,
    recentUnlockAt: 0,
    lastLockedStationKey: null,
    lastLockedFreq: null,
    lastStablePosition: null
  };
  this.pendingActivationTimer = null;
  this.activationInFlight = null;
  this.activationInFlightPromise = null;
  this.lastActivationIssuedKey = null;
  this.lastActivationIssuedAt = 0;
  this.lastVolumioState = this.buildIdleState();
  this.modeSwitchLockUntil = 0;
  this.activationSerial = Promise.resolve();
  this.rendererShutdownRequested = false;
  this.rendererRetryTimer = null;
}



ControllerRadioScalePeppy.prototype.onVolumioStart = function () {
  const configFile = this.commandRouter.pluginManager.getConfigurationFile(this.context, 'config.json');
  this.config = new vConf();
  this.config.loadFile(configFile);
  return libQ.resolve();
};

ControllerRadioScalePeppy.prototype.onStart = function () {
  const self = this;
  const defer = libQ.defer();

  Promise.resolve()
    .then(() => {
      self.logger.info('[radio_scale_peppy] onStart');
      self.ensureRuntimeDir();
      if (!fs.existsSync(self.sharedOverlayOwnerPath)) {
        self.writeSharedOverlayOwner('none', 'radio_scale_peppy');
      }
      self.ensureSeedPlaylistExists();
      self.removeDeprecatedSeedEntries();
      self.ensureMyWebRadiosSeeded();
      self.stationCache = self.loadStationCache();
      self.refreshExternalStationIndex();
      self.startStationSourceWatchers();
      self.syncTuningConfig();
      self.hydrateTuningFromStateFile();
      self.writeSettingsFile();
      if (!fs.existsSync(self.statePath)) {
        self.writeStateFile(self.buildIdleState());
      }
      self.stopHiss();
      self.clearRendererReadyFlag();
      self.startPolling();
      self.logger.info('[radio_scale_peppy] renderer enabled = ' + JSON.stringify(self.isRendererEnabled()));
      if (self.isResidentRendererServiceEnabled()) {
        self.logger.info('[radio_scale_peppy] resident renderer service mode active - expecting systemd-managed preload');
      } else if (self.shouldPreloadResidentRenderer()) {
        self.scheduleResidentRendererStart(1000);
      } else if (self.isRendererEnabled() && self.getBooleanConfig('autoStartRendererOnPluginStart', false) === true) {
        self.startRenderer();
      } else {
        self.logger.info('[radio_scale_peppy] renderer waiting for browse source or button trigger');
      }
      defer.resolve();
    })
    .catch((err) => {
      self.logger.error('[radio_scale_peppy] onStart failed: ' + err.stack);
      defer.reject(err);
    });

  return defer.promise;
};

ControllerRadioScalePeppy.prototype.onStop = function () {
  const self = this;
  const defer = libQ.defer();

  try {
    self.stopPolling();
    self.stopStationSourceWatchers();
    self.clearHissSyncTimer();
    self.stopHiss();
    self.clearPendingActivation();
    self.clearRendererRetryTimer();
    self.stopRenderer();
    defer.resolve();
  } catch (err) {
    self.logger.error('[radio_scale_peppy] onStop failed: ' + err.stack);
    defer.reject(err);
  }

  return defer.promise;
};


/**
 * Read the last renderer/runtime state from disk.
 *
 * The renderer continuously consumes this JSON, so it is the cheapest place to
 * restore the last tuned pointer position when the overlay is opened again.
 */
ControllerRadioScalePeppy.prototype.readPersistedScaleState = function () {
  try {
    if (!fs.existsSync(this.statePath)) {
      return null;
    }
    const raw = fs.readFileSync(this.statePath, 'utf8');
    if (!raw || !raw.trim()) {
      return null;
    }
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] readPersistedScaleState failed: ' + err.message);
    return null;
  }
};

/**
 * Restore in-memory tuning anchors from the last runtime state file.
 *
 * This keeps the pointer and lock target stable across overlay close/open
 * cycles, and also helps after a plugin restart.
 */
ControllerRadioScalePeppy.prototype.hydrateTuningFromStateFile = function () {
  const persisted = this.readPersistedScaleState();
  if (!persisted) {
    return false;
  }

  const persistedPosition = Number(persisted.tuning_position);
  const persistedLockedStation = persisted.tuning_station || persisted.matched_station || null;
  const persistedLockedFreq = Number(
    persistedLockedStation && typeof persistedLockedStation.freq !== 'undefined'
      ? persistedLockedStation.freq
      : persisted.active_frequency
  );

  if (Number.isFinite(persistedPosition)) {
    this.tuning.position = persistedPosition;
    this.tuning.lastStablePosition = persistedPosition;
  }

  if (persistedLockedStation && persistedLockedStation.key) {
    this.tuning.lastLockedStationKey = String(persistedLockedStation.key);
    this.tuning.lockedStationKey = String(persistedLockedStation.key);
    this.tuning.nearestStationKey = String(persistedLockedStation.key);
  }

  if (Number.isFinite(persistedLockedFreq)) {
    this.tuning.lastLockedFreq = persistedLockedFreq;
    if (!Number.isFinite(Number(this.tuning.position))) {
      this.tuning.position = persistedLockedFreq;
    }
  }

  if (persisted.tuning_locked && Number.isFinite(persistedLockedFreq)) {
    this.tuning.noiseLevel = 0;
  }

  return true;
};

/**
 * Re-seed the pointer right before entering the overlay.
 *
 * When the user reopens the scale, we want to land on the last locked station
 * rather than drift into hiss on the left side of the band.
 */
ControllerRadioScalePeppy.prototype.restoreOpenScaleSeed = function (baseState) {
  if (Number.isFinite(Number(this.tuning.lastLockedFreq))) {
    this.tuning.position = Number(this.tuning.lastLockedFreq);
    this.tuning.lastStablePosition = Number(this.tuning.lastLockedFreq);
    if (this.tuning.lastLockedStationKey) {
      this.tuning.lockedStationKey = this.tuning.lastLockedStationKey;
      this.tuning.nearestStationKey = this.tuning.lastLockedStationKey;
    }
    this.tuning.noiseLevel = 0;
    return true;
  }

  const persisted = this.readPersistedScaleState();
  if (persisted) {
    const restored = this.hydrateTuningFromStateFile();
    if (restored) {
      return true;
    }
  }

  if (baseState && baseState.matched_station && Number.isFinite(Number(baseState.matched_station.freq))) {
    this.tuning.position = Number(baseState.matched_station.freq);
    this.tuning.lockedStationKey = baseState.matched_station.key || null;
    this.tuning.lastLockedStationKey = baseState.matched_station.key || null;
    this.tuning.lastLockedFreq = Number(baseState.matched_station.freq);
    this.tuning.lastStablePosition = Number(baseState.matched_station.freq);
    this.tuning.noiseLevel = 0;
    return true;
  }

  return false;
};

/**
 * Stop the currently playing radio stream once when the pointer leaves a locked
 * station. This restores hiss behaviour without spamming stop commands on every
 * tiny encoder step.
 */
ControllerRadioScalePeppy.prototype.stopPlaybackOnUnlock = function (previousLockedKey) {
  if (!previousLockedKey || this.tuning.tuneUnlockPauseApplied) {
    return Promise.resolve({ success: true, skipped: true, reason: 'already-unlocked' });
  }

  const stations = this.getStations();
  const previousStation = stations.find((station) => station.key === previousLockedKey) || null;
  const currentUri = String((this.lastVolumioState && this.lastVolumioState.uri) || '');
  const currentStatus = String((this.lastVolumioState && this.lastVolumioState.status) || '');

  if (!currentUri || currentStatus !== 'play') {
    this.tuning.tuneUnlockPauseApplied = true;
    return Promise.resolve({ success: true, skipped: true, reason: 'nothing-playing' });
  }

  if (previousStation && previousStation.uri && currentUri !== String(previousStation.uri)) {
    this.tuning.tuneUnlockPauseApplied = true;
    return Promise.resolve({ success: true, skipped: true, reason: 'different-stream' });
  }

  this.tuning.tuneUnlockPauseApplied = true;
  return this.restCommand('stop')
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] stopPlaybackOnUnlock failed: ' + err.message);
      return { success: false, warning: err.message };
    })
    .then(() => this.pollState())
    .then(() => ({ success: true, stopped: true, previousLockedKey }));
};

/**
 * Remove deprecated seed entries from all relevant favourites / playlist files.
 *
 * Earlier field builds could seed OE1 into several JSON-backed Volumio lists.
 * 1.9.7-safe cleans the known Scale-FM-related locations plus every JSON playlist
 * under /data/playlist so old seed data does not keep reappearing after plugin
 * upgrades.
 */
ControllerRadioScalePeppy.prototype.removeDeprecatedSeedEntries = function () {
  const playlistDir = '/data/playlist';
  const cleanupPaths = new Set([this.getPlaylistPath(), this.myWebRadioPath]);

  try {
    if (fs.existsSync(playlistDir)) {
      fs.readdirSync(playlistDir)
        .filter((name) => /\.(json|m3u|m3u8)?$/i.test(name) || name.indexOf('.') === -1)
        .forEach((name) => cleanupPaths.add(path.join(playlistDir, name)));
    }
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] playlist directory scan failed: ' + err.message);
  }

  const oe1Pattern = /(\boe\s*1\b|\bö\s*1\b|orf\s*oe1|oe1-q2a|oe1)/i;

  const filterJsonEntries = (entries) => entries.filter((entry) => {
    const haystack = [
      entry && entry.title,
      entry && entry.name,
      entry && entry.artist,
      entry && entry.uri,
      entry && entry.service
    ].map((value) => String(value || '')).join(' | ');
    return !oe1Pattern.test(haystack);
  });

  const filterM3u = (raw) => {
    const lines = String(raw || '').split(/\r?\n/);
    const kept = [];
    for (let index = 0; index < lines.length; index += 1) {
      const line = lines[index];
      const nextLine = index + 1 < lines.length ? lines[index + 1] : '';
      const pair = [line, nextLine].join('\n');
      if (/^#EXTINF/i.test(line) && oe1Pattern.test(pair)) {
        index += 1;
        continue;
      }
      if (!/^#/.test(line) && oe1Pattern.test(line)) {
        continue;
      }
      kept.push(line);
    }
    return kept.join('\n').replace(/\n{3,}/g, '\n\n');
  };

  cleanupPaths.forEach((targetPath) => {
    try {
      if (!fs.existsSync(targetPath)) {
        return;
      }
      const raw = fs.readFileSync(targetPath, 'utf8');
      const trimmed = String(raw || '').trim();
      if (!trimmed) {
        return;
      }

      if (trimmed.startsWith('[') || trimmed.startsWith('{')) {
        const parsed = JSON.parse(trimmed);
        if (!Array.isArray(parsed)) {
          return;
        }
        const filtered = filterJsonEntries(parsed);
        if (filtered.length !== parsed.length) {
          fs.writeFileSync(targetPath, JSON.stringify(filtered, null, 2));
          this.logger.info('[radio_scale_peppy] removed deprecated OE1 entries from ' + targetPath);
        }
        return;
      }

      const filteredText = filterM3u(raw);
      if (filteredText !== raw) {
        fs.writeFileSync(targetPath, filteredText);
        this.logger.info('[radio_scale_peppy] removed deprecated OE1 lines from ' + targetPath);
      }
    } catch (err) {
      this.logger.warn('[radio_scale_peppy] removeDeprecatedSeedEntries failed for ' + targetPath + ': ' + err.message);
    }
  });
};

/** Clear any pending delayed hiss start. */
ControllerRadioScalePeppy.prototype.clearHissSyncTimer = function () {
  if (this.hissSyncTimer) {
    clearTimeout(this.hissSyncTimer);
    this.hissSyncTimer = null;
  }
};

ControllerRadioScalePeppy.prototype.getConfigurationFiles = function () {
  return ['config.json'];
};

ControllerRadioScalePeppy.prototype.getBrowseSourceAlbumart = function () {
  return '/albumart?sourceicon=user_interface/radio_scale_peppy/icon.png';
};

ControllerRadioScalePeppy.prototype.addToBrowseSources = function () {
  this.logger.info('[radio_scale_peppy] browse source registration is handled by separate radio_scale_source plugin');
  this.browseSourceRegistered = false;
};

ControllerRadioScalePeppy.prototype.removeFromBrowseSources = function () {
  this.browseSourceRegistered = false;
};

ControllerRadioScalePeppy.prototype.handleBrowseUri = function (curUri) {
  const defer = libQ.defer();
  const uri = String(curUri || '').replace(/^\//, '');

  Promise.resolve()
    .then(() => {
      this.logger.info('[radio_scale_peppy] handleBrowseUri ' + uri);
      if (uri === this.browseSourceUri || uri === this.browseSourceUri + '/open') {
        return this.openScale(false).then(() => this.getBrowseRoot(true));
      }

      if (uri === this.browseSourceUri + '/close') {
        return this.exitScaleToBrowse(false).then(() => this.getBrowseRoot(false));
      }

      throw new Error('Unknown browse URI: ' + curUri);
    })
    .then((response) => defer.resolve(response))
    .catch((err) => {
      this.logger.error('[radio_scale_peppy] handleBrowseUri failed: ' + err.message);
      defer.reject(err);
    });

  return defer.promise;
};

ControllerRadioScalePeppy.prototype.getBrowseRoot = function (scaleActive) {
  const active = typeof scaleActive === 'boolean' ? scaleActive : Boolean(this.rendererProcess);
  return {
    navigation: {
      prev: { uri: '/' },
      lists: [
        {
          title: this.browseSourceName,
          availableListViews: ['list', 'grid'],
          items: [
            {
              service: 'radio_scale_peppy',
              type: 'folder',
              title: active ? 'Scale FM Overlay läuft' : 'Scale FM Overlay starten',
              artist: '',
              album: '',
              albumart: this.getBrowseSourceAlbumart(),
              icon: 'fa fa-radio',
              uri: this.browseSourceUri + '/open'
            },
            {
              service: 'radio_scale_peppy',
              type: 'folder',
              title: 'Zurück zu Quellen',
              artist: '',
              album: '',
              icon: 'fa fa-home',
              uri: this.browseSourceUri + '/close'
            },
            {
              service: 'radio_scale_peppy',
              type: 'item-no-menu',
              title: 'Encoder 1 Long Press = Quellen',
              artist: '',
              album: '',
              icon: 'fa fa-arrow-left',
              uri: this.browseSourceUri
            }
          ]
        }
      ]
    }
  };
};

/**
 * Ask the active Volumio client to show the browse root.
 *
 * We try both `/` and an empty URI because different clients / screensavers
 * can behave slightly differently when the overlay exits.
 */
ControllerRadioScalePeppy.prototype.navigateToBrowseRoot = function () {
  return this.emitSocketEvent('browseLibrary', { uri: '/' })
    .catch(() => this.emitSocketEvent('browseLibrary', { uri: '' }))
    .catch(() => ({ success: true }));
};

/**
 * Ask Volumio to paint the regular UI *before* the resident overlay hides.
 *
 * 1.10.2 uses this as an exit pre-roll to reduce the white flash gap between
 * the fullscreen overlay and Chromium's normal page repaint.
 */
ControllerRadioScalePeppy.prototype.prepareUnderlyingUiForOverlayHide = function () {
  return this.navigateToBrowseRoot()
    .catch(() => ({ success: true }));
};


/** Simple promise-based sleep helper used to soften UI hand-off timing. */
ControllerRadioScalePeppy.prototype.delay = function (ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/** Remove the renderer-ready marker so fresh opens wait for a new first paint. */
ControllerRadioScalePeppy.prototype.clearRendererReadyFlag = function () {
  try {
    if (fs.existsSync(this.rendererReadyPath)) {
      fs.unlinkSync(this.rendererReadyPath);
    }
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] clearRendererReadyFlag failed: ' + err.message);
  }
};

/** Read the renderer-ready marker that is written after the first visible frame. */
ControllerRadioScalePeppy.prototype.isRendererReady = function () {
  try {
    if (!fs.existsSync(this.rendererReadyPath)) {
      return false;
    }
    const raw = fs.readFileSync(this.rendererReadyPath, 'utf8');
    const parsed = raw && raw.trim() ? JSON.parse(raw) : null;
    return Boolean(parsed && parsed.ready);
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] isRendererReady failed: ' + err.message);
    return false;
  }
};

/**
 * Wait briefly for the renderer to present its first visible frame.
 *
 * The source plugin uses this to keep the local touch UI on the current page a
 * little longer, which reduces how often the user sees the empty white
 * intermediate browse page before the fullscreen overlay takes over.
 */
ControllerRadioScalePeppy.prototype.waitForRendererReadyBriefly = function (timeoutMs) {
  const deadline = Date.now() + Math.max(0, Number(timeoutMs) || 0);
  const poll = () => {
    if (this.isRendererReady()) {
      return Promise.resolve({ success: true, ready: true });
    }
    if (Date.now() >= deadline) {
      return Promise.resolve({ success: true, ready: false, timeout: true });
    }
    return this.delay(40).then(poll);
  };
  return poll();
};

/**
 * Leave the overlay and return control to standard Volumio browsing.
 *
 * Runtime cleanup that happens here:
 * - pending station activation is cancelled
 * - encoder mode is reset to `normal`
 * - hiss playback stops
 * - fullscreen renderer is terminated
 * - fresh runtime state/settings are written for the next entry
 */
ControllerRadioScalePeppy.prototype.goToSourceSelect = function () {
  this.logger.info('[radio_scale_peppy] goToSourceSelect');
  this.clearPendingActivation();
  this.activationInFlight = null;
  this.activationInFlightPromise = null;
  this.overlayOpenedAt = 0;
  this.modeSwitchLockUntil = Date.now() + 500;
  this.stopHiss();

  return Promise.resolve()
    .then(() => this.refreshBaseQueueAfterExit())
    .then(() => this.pollState())
    .then(() => this.prepareUnderlyingUiForOverlayHide())
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] prepareUnderlyingUiForOverlayHide failed: ' + err.message);
      return { success: false, warning: err.message };
    })
    .then(() => this.delay(220))
    .then(() => {
      this.setControlMode('normal', false);
      this.releaseSharedOverlayOwnershipIfOwned();
      this.clearHissSyncTimer();
      this.stopHiss();
      if (this.isResidentRendererEnabled()) {
        this.clearRendererReadyFlag();
      } else {
        this.stopRenderer();
      }
      this.writeSettingsFile();
      return this.pollState();
    })
    .then(() => ({ success: true, controlMode: this.getControlMode(), rendererRunning: Boolean(this.rendererProcess) }));
};

/**
 * Enter the Scale FM overlay.
 *
 * This is the main entry point used by the browse tile, GPIO button and manual
 * plugin calls. It switches encoder 2 into scale mode, starts the renderer if
 * needed, refreshes runtime JSON files and optionally auto-activates the
 * station currently locked by the pointer.
 */
ControllerRadioScalePeppy.prototype.openScale = function (notify) {
  this.logger.info('[radio_scale_peppy] openScale');
  if (!this.isRendererEnabled()) {
    return Promise.resolve({ success: false, reason: 'Renderer disabled in config' });
  }

  if (this.getControlMode() === 'scale' && this.isRendererRunning()) {
    this.logger.info('[radio_scale_peppy] openScale ignored because overlay is already active');
    return Promise.resolve()
      .then(() => this.pollState())
      .then(() => ({ success: true, ignored: true, reason: 'already-active', controlMode: this.getControlMode(), rendererRunning: true }));
  }

  const rendererAlreadyRunning = this.isRendererRunning();
  const baseState = this.lastVolumioState || this.buildIdleState();

  this.overlayOpenedAt = Date.now();
  this.claimSharedOverlayOwnership();
  this.clearHissSyncTimer();
  this.clearRendererReadyFlag();
  this.restoreOpenScaleSeed(baseState);
  this.setControlMode('scale', notify !== false);

  // 1.10.2 keeps the same pre-seeding approach, but the resident renderer now
  // also forces a state reload on the visible transition. Together this avoids
  // the first-open pointer sweep that could still happen right after boot.
  this.ensureTuningSeed(baseState);
  const tuningEval = this.evaluateTuning();
  const effective = this.applyTuningOverlay(baseState);
  this.writeSettingsFile();
  this.writeStateIfChanged(effective);
  this.stopHiss();

  if (!rendererAlreadyRunning) {
    this.startRenderer();
  } else {
    this.logger.info('[radio_scale_peppy] renderer already running');
  }

  const shouldActivateLockedStation = Boolean(
    tuningEval.lockedStation &&
    this.tuning.autoPlayOnLock && (
      !this.lastVolumioState ||
      this.lastVolumioState.status !== 'play' ||
      String(this.lastVolumioState.uri || '') !== String((tuningEval.lockedStation && tuningEval.lockedStation.uri) || '')
    )
  );

  Promise.resolve()
    .then(() => this.waitForRendererReadyBriefly(this.getNumberConfig('rendererReadyWaitMs', 2200)))
    .then(() => shouldActivateLockedStation ? this.scheduleLockedStationActivation(tuningEval.lockedStation) : { success: true, skipped: true })
    .then(() => this.pollState())
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] openScale background work failed: ' + err.message);
    });

  return Promise.resolve({ success: true, controlMode: this.getControlMode(), rendererRunning: this.isRendererRunning(), alreadyRunning: rendererAlreadyRunning });
};

/**
 * Lightweight overlay shutdown helper.
 *
 * `navigate === false` only closes renderer-related pieces and leaves final UI
 * navigation to the caller. `navigate !== false` uses the full source-select
 * hand-off implemented by `goToSourceSelect()`.
 */
ControllerRadioScalePeppy.prototype.exitScaleToBrowse = function (navigate) {
  this.logger.info('[radio_scale_peppy] exitScaleToBrowse navigate=' + JSON.stringify(navigate));
  if (navigate === false) {
    this.clearPendingActivation();
    this.activationInFlight = null;
    this.activationInFlightPromise = null;
    this.overlayOpenedAt = 0;
    this.setControlMode('normal', false);
    this.releaseSharedOverlayOwnershipIfOwned();
    this.clearHissSyncTimer();
    this.stopHiss();
    if (this.isResidentRendererEnabled()) {
      this.clearRendererReadyFlag();
    } else {
      this.stopRenderer();
    }
    this.writeSettingsFile();

    return Promise.resolve()
      .then(() => this.pollState())
      .then(() => ({ success: true, controlMode: this.getControlMode(), rendererRunning: this.isRendererRunning() }));
  }
  return this.goToSourceSelect();
};


/**
 * Build one queue item payload for Volumio's addToQueue endpoint.
 *
 * We intentionally re-use the same metadata shape as replaceAndPlay, just
 * without the implicit playback side effect.
 */
ControllerRadioScalePeppy.prototype.buildQueuePayload = function (playable) {
  if (!playable || !playable.uri) {
    return null;
  }
  return {
    uri: playable.uri,
    service: playable.service || 'webradio',
    title: playable.title || playable.name,
    artist: playable.artist || '',
    album: playable.album || '',
    albumart: playable.albumart || '',
    type: playable.type || 'webradio'
  };
};

/**
 * Queue a single item without starting playback.
 */
ControllerRadioScalePeppy.prototype.addItemToQueue = function (payload) {
  if (!payload || !payload.uri) {
    return Promise.resolve({ success: false, skipped: true, reason: 'missing-uri' });
  }
  return this.httpRequest({
    method: 'POST',
    path: '/api/v1/addToQueue',
    json: payload
  });
};

/**
 * Rebuild the neutral base queue from the radioscale_base playlist file.
 *
 * This is used on overlay exit so the user lands back in a predictable Volumio
 * state instead of keeping the last tuned station as the active queue.
 */
ControllerRadioScalePeppy.prototype.restoreBaseQueueFromPlaylist = function () {
  const playlistStations = this.loadPlaylistStations();
  const queuePayloads = playlistStations
    .map((station) => this.enrichStationPlayableInfo(station))
    .map((station) => this.buildQueuePayload(station))
    .filter(Boolean);

  if (!queuePayloads.length) {
    this.logger.warn('[radio_scale_peppy] restoreBaseQueueFromPlaylist skipped: no playlist stations found');
    return Promise.resolve({ success: false, skipped: true, reason: 'empty-playlist' });
  }

  return this.restCommand('clearQueue')
    .then(() => queuePayloads.reduce(
      (chain, payload) => chain.then(() => this.addItemToQueue(payload)),
      Promise.resolve()
    ))
    .then(() => ({ success: true, queued: queuePayloads.length }));
};

/**
 * Stop active playback and restore the neutral radioscale_base queue.
 *
 * Primary path:
 * - stop playback
 * - rebuild the queue item-by-item via addToQueue
 *
 * Fallback path:
 * - ask Volumio to play the named playlist and immediately stop again
 *
 * The fallback is only used if the queue rebuild API path fails.
 */
ControllerRadioScalePeppy.prototype.stopPlaybackAndRestoreBaseQueue = function () {
  const playlistName = this.getPlaylistName();

  return this.restCommand('stop')
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] stop before queue restore failed: ' + err.message);
      return { success: false, warning: err.message };
    })
    .then(() => this.delay(120))
    .then(() => this.restoreBaseQueueFromPlaylist())
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] restoreBaseQueueFromPlaylist failed, fallback to playplaylist+stop: ' + err.message);
      return this.restCommand('playplaylist', { name: playlistName })
        .then(() => this.delay(180))
        .then(() => this.restCommand('stop'))
        .then(() => ({ success: true, fallback: true, playlist: playlistName }));
    });
};

/**
 * Append the neutral radioscale_base queue *without* interrupting current playback.
 *
 * This is the safe queue-hand-off used by 1.9.5-safe. The active station keeps
 * playing so Volumio can fall back to its normal Now Playing screen cleanly,
 * while the base queue is rebuilt behind the scenes for later browsing.
 */
ControllerRadioScalePeppy.prototype.appendBaseQueueWithoutInterruptingPlayback = function () {
  const playlistStations = this.loadPlaylistStations();
  const currentUri = String((this.lastVolumioState && this.lastVolumioState.uri) || '').trim();
  const seen = new Set(currentUri ? [currentUri] : []);
  const queuePayloads = playlistStations
    .map((station) => this.enrichStationPlayableInfo(station))
    .map((station) => this.buildQueuePayload(station))
    .filter((payload) => {
      if (!payload || !payload.uri) {
        return false;
      }
      const uri = String(payload.uri).trim();
      if (!uri || seen.has(uri)) {
        return false;
      }
      seen.add(uri);
      return true;
    });

  if (!queuePayloads.length) {
    this.logger.info('[radio_scale_peppy] appendBaseQueueWithoutInterruptingPlayback skipped: nothing new to queue');
    return Promise.resolve({ success: true, skipped: true, reason: 'nothing-to-queue' });
  }

  return queuePayloads.reduce(
    (chain, payload) => chain.then(() => this.addItemToQueue(payload)),
    Promise.resolve()
  ).then(() => ({ success: true, queued: queuePayloads.length, preservedPlayback: Boolean(currentUri) }));
};

/**
 * Refresh the neutral radioscale_base queue on overlay exit.
 *
 * Behaviour:
 * - if a station is still playing, keep it alive and append the base queue
 * - if nothing is playing, fall back to the older stop-and-restore path
 */
ControllerRadioScalePeppy.prototype.refreshBaseQueueAfterExit = function () {
  const state = this.lastVolumioState || {};
  const isPlaying = String(state.status || '') === 'play' && String(state.uri || '').trim() !== '';
  if (isPlaying) {
    return this.appendBaseQueueWithoutInterruptingPlayback();
  }
  return this.stopPlaybackAndRestoreBaseQueue();
};

ControllerRadioScalePeppy.prototype.getConfigValue = function (key, fallback) {
  const raw = this.config.get(key);
  if (raw && typeof raw === 'object' && Object.prototype.hasOwnProperty.call(raw, 'value')) {
    return raw.value;
  }
  return typeof raw === 'undefined' ? fallback : raw;
};

ControllerRadioScalePeppy.prototype.getBooleanConfig = function (key, fallback) {
  const value = this.getConfigValue(key, fallback);
  if (typeof value === 'boolean') {
    return value;
  }
  if (typeof value === 'number') {
    return value !== 0;
  }
  if (typeof value === 'string') {
    const lower = value.trim().toLowerCase();
    if (['true', '1', 'yes', 'on'].includes(lower)) {
      return true;
    }
    if (['false', '0', 'no', 'off', ''].includes(lower)) {
      return false;
    }
  }
  return Boolean(value);
};

ControllerRadioScalePeppy.prototype.getNumberConfig = function (key, fallback) {
  const value = Number(this.getConfigValue(key, fallback));
  return Number.isFinite(value) ? value : Number(fallback);
};

ControllerRadioScalePeppy.prototype.getStringConfig = function (key, fallback) {
  const value = this.getConfigValue(key, fallback);
  if (value === null || typeof value === 'undefined') {
    return typeof fallback === 'undefined' ? '' : String(fallback);
  }
  return String(value);
};

ControllerRadioScalePeppy.prototype.isRendererEnabled = function () {
  return this.getBooleanConfig('enabled', true);
};

/**
 * Resident renderer mode keeps the Python process alive in hidden standby.
 *
 * Why this exists:
 * - removes repeated Python/Pygame startup cost on every overlay open
 * - keeps PNG themes, fonts and cached surfaces warm in memory
 * - allows the source tile / GPIO button to switch the overlay visible instead
 *   of spawning a fresh process every time
 */
ControllerRadioScalePeppy.prototype.isResidentRendererEnabled = function () {
  return this.getBooleanConfig('residentRendererEnabled', true);
};

/**
 * Service mode means the resident renderer is expected to be managed by systemd
 * (`scale_fm_renderer.service`) instead of being spawned by the plugin itself.
 * The plugin still keeps the classic spawn path as a fallback when the service
 * is not running.
 */
ControllerRadioScalePeppy.prototype.isResidentRendererServiceEnabled = function () {
  return this.isResidentRendererEnabled() && this.getBooleanConfig('residentRendererServiceEnabled', true);
};

/** Read the resident renderer PID file written by the Python process. */
ControllerRadioScalePeppy.prototype.getExternalRendererPid = function () {
  try {
    if (!fs.existsSync(this.rendererPidPath)) {
      return null;
    }
    const raw = String(fs.readFileSync(this.rendererPidPath, 'utf8') || '').trim();
    const pid = Number(raw);
    return Number.isInteger(pid) && pid > 1 ? pid : null;
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] getExternalRendererPid failed: ' + err.message);
    return null;
  }
};

/** Check whether a PID currently exists. */
ControllerRadioScalePeppy.prototype.isPidAlive = function (pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (err) {
    return false;
  }
};


/**
 * Read the shared overlay owner marker used by multiple resident overlays.
 *
 * Contract:
 * - owner=scale_fm  -> Scale FM may render actively
 * - owner=fun_linea -> Scale FM must switch to deep idle
 * - owner=none      -> Scale FM stays in normal hidden standby
 */
ControllerRadioScalePeppy.prototype.readSharedOverlayOwner = function () {
  try {
    if (!fs.existsSync(this.sharedOverlayOwnerPath)) {
      return { owner: 'none' };
    }
    const payload = JSON.parse(String(fs.readFileSync(this.sharedOverlayOwnerPath, 'utf8') || '{}'));
    const owner = String(payload.owner || 'none').trim().toLowerCase();
    return {
      owner: owner || 'none',
      updated_at: payload.updated_at || null,
      source: payload.source || 'unknown'
    };
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] readSharedOverlayOwner failed: ' + err.message);
    return { owner: 'none' };
  }
};

/** Write one shared overlay owner marker JSON atomically. */
ControllerRadioScalePeppy.prototype.writeSharedOverlayOwner = function (owner, source) {
  const marker = {
    owner: String(owner || 'none').trim().toLowerCase() || 'none',
    updated_at: Date.now(),
    source: source || 'radio_scale_peppy'
  };
  try {
    fs.writeFileSync(this.sharedOverlayOwnerPath, JSON.stringify(marker, null, 2));
    return marker;
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] writeSharedOverlayOwner failed: ' + err.message);
    return null;
  }
};

/** Claim the shared overlay owner slot for Scale FM before showing the overlay. */
ControllerRadioScalePeppy.prototype.claimSharedOverlayOwnership = function () {
  return this.writeSharedOverlayOwner('scale_fm', 'radio_scale_peppy');
};

/**
 * Release the shared overlay owner marker only when Scale FM currently owns it.
 * This avoids trampling over future overlays such as fun_linea.
 */
ControllerRadioScalePeppy.prototype.releaseSharedOverlayOwnershipIfOwned = function () {
  const current = this.readSharedOverlayOwner();
  if (String(current.owner || 'none').toLowerCase() !== 'scale_fm') {
    return current;
  }
  return this.writeSharedOverlayOwner('none', 'radio_scale_peppy');
};

/**
 * Unified renderer-running probe used by status endpoints and duplicate-open
 * protection. This covers plugin-owned child processes and service-managed
 * resident renderer instances.
 */
ControllerRadioScalePeppy.prototype.isRendererRunning = function () {
  if (this.rendererProcess) {
    return true;
  }
  const pid = this.getExternalRendererPid();
  return Boolean(pid && this.isPidAlive(pid));
};

/**
 * Decide whether the hidden standby renderer should be preloaded right after
 * the plugin starts. This is the default for 1.10.2-resident.
 */
ControllerRadioScalePeppy.prototype.shouldPreloadResidentRenderer = function () {
  return this.isRendererEnabled() && this.isResidentRendererEnabled() && !this.isResidentRendererServiceEnabled() && this.getBooleanConfig('preloadRendererOnPluginStart', true);
};

/** Clear a pending resident-renderer retry timer. */
ControllerRadioScalePeppy.prototype.clearRendererRetryTimer = function () {
  if (this.rendererRetryTimer) {
    clearTimeout(this.rendererRetryTimer);
    this.rendererRetryTimer = null;
  }
};

/**
 * Spawn the hidden standby renderer a little later.
 *
 * Volumio can start plugins before the X11 touch-display session is fully
 * ready. The retry helper prevents a one-shot cold boot failure from leaving
 * the resident service permanently absent.
 */
ControllerRadioScalePeppy.prototype.scheduleResidentRendererStart = function (delayMs) {
  if (!this.shouldPreloadResidentRenderer()) {
    return;
  }
  this.clearRendererRetryTimer();
  this.rendererRetryTimer = setTimeout(() => {
    this.rendererRetryTimer = null;
    if (this.rendererProcess || !this.shouldPreloadResidentRenderer()) {
      return;
    }
    this.logger.info('[radio_scale_peppy] resident renderer preload attempt');
    this.startRenderer();
  }, Math.max(0, Number(delayMs) || 0));
};


/** Read the effective encoder mode exposed to the renderer and GPIO hooks. */
ControllerRadioScalePeppy.prototype.getControlMode = function () {
  if (!this.tuning || this.tuning.controlMode !== 'scale') {
    return 'normal';
  }
  return 'scale';
};

/**
 * Force one encoder mode.
 *
 * `scale` = encoder 2 tunes stations on the scale.
 * `normal` = encoder 2 returns to regular Volumio previous/next behaviour.
 */
ControllerRadioScalePeppy.prototype.setControlMode = function (mode, notify) {
  const nextMode = mode === 'scale' ? 'scale' : 'normal';
  if (nextMode !== 'scale') {
    this.overlayOpenedAt = 0;
  }
  this.tuning.controlMode = nextMode;
  this.tuning.tuningMode = nextMode === 'scale'
    ? (this.tuning.autoPlayOnLock ? 'auto' : 'manual')
    : 'normal';

  if (notify !== false) {
    this.commandRouter.pushToastMessage(
      'success',
      PUBLIC_OVERLAY_NAME,
      nextMode === 'scale' ? 'Scale tuning mode active' : 'Normal encoder mode active'
    );
  }

  const effective = this.applyTuningOverlay(this.lastVolumioState || this.buildIdleState());
  this.writeStateIfChanged(effective);
  this.syncHissWithState(effective);
  return { success: true, mode: nextMode };
};

/**
 * Toggle encoder 2 between scale mode and normal Volumio track stepping.
 *
 * A short guard window prevents the same double-press from also being consumed
 * as a left/right rotation event immediately afterwards.
 */
ControllerRadioScalePeppy.prototype.toggleControlMode = function () {
  const nextMode = this.getControlMode() === 'scale' ? 'normal' : 'scale';
  this.logger.info('[radio_scale_peppy] toggleControlMode -> ' + nextMode);
  this.modeSwitchLockUntil = Date.now() + Math.max(300, this.getNumberConfig('controlModeSwitchGuardMs', 450));
  this.setControlMode(nextMode, true);
  const effective = this.applyTuningOverlay(this.lastVolumioState || this.buildIdleState());
  this.writeStateIfChanged(effective);
  this.syncHissWithState(effective);
  return Promise.resolve()
    .then(() => this.pollState())
    .then(() => ({ success: true, mode: nextMode, rendererRunning: Boolean(this.rendererProcess), guardUntil: this.modeSwitchLockUntil }));
};


ControllerRadioScalePeppy.prototype.getUIConfig = function () {
  const defer = libQ.defer();

  try {
    this.logger.info('[radio_scale_peppy] getUIConfig');
    defer.resolve({
      page: {
        label: PUBLIC_OVERLAY_NAME
      },
      sections: [
        {
          id: 'info',
          element: 'section',
          label: 'Information',
          icon: 'fa-info-circle',
          content: [
            {
              id: 'pluginInfo',
              element: 'input',
              type: 'text',
              label: 'Status',
              value: 'Stable runtime build with auto-resync from My Web Radios, playlist-backed station seeds and Braun HD layered PNG theme support.'
            },
            {
              id: 'configPath',
              element: 'input',
              type: 'text',
              label: 'Config file',
              value: '/data/configuration/user_interface/radio_scale_peppy/config.json'
            },
            {
              id: 'stationSources',
              element: 'input',
              type: 'text',
              label: 'Station sources',
              value: '/data/favourites/my-web-radio and /data/playlist/radioscale_base'
            }
          ]
        }
      ]
    });
  } catch (err) {
    this.logger.error('[radio_scale_peppy] getUIConfig failed: ' + err.stack);
    defer.resolve({ page: { label: PUBLIC_OVERLAY_NAME }, sections: [] });
  }

  return defer.promise;
};


ControllerRadioScalePeppy.prototype.saveSettings = function () {
  this.logger.info('[radio_scale_peppy] saveSettings ignored in stable runtime build');
  return libQ.resolve({ success: true });
};

ControllerRadioScalePeppy.prototype.ensureRuntimeDir = function () {
  if (!fs.existsSync(this.runtimeDir)) {
    fs.mkdirSync(this.runtimeDir, { recursive: true });
  }
};


ControllerRadioScalePeppy.prototype.getPlaylistName = function () {
  const candidate = this.getStringConfig('playlistName', this.seedPlaylistName).trim();
  return candidate || this.seedPlaylistName;
};

ControllerRadioScalePeppy.prototype.getPlaylistPath = function () {
  return path.join('/data/playlist', this.getPlaylistName());
};

ControllerRadioScalePeppy.prototype.getSeedStations = function () {
  return this.seedStations.map((station) => Object.assign({}, station, {
    match: Array.isArray(station.match) ? station.match.slice() : []
  }));
};

ControllerRadioScalePeppy.prototype.ensureSeedPlaylistExists = function () {
  const playlistPath = this.getPlaylistPath();
  const playlistDir = path.dirname(playlistPath);
  if (!fs.existsSync(playlistDir)) {
    fs.mkdirSync(playlistDir, { recursive: true });
  }

  if (fs.existsSync(playlistPath)) {
    return;
  }

  const playlistEntries = this.getSeedStations().map((station) => ({
    service: station.service || 'webradio',
    uri: station.uri,
    title: station.title || station.name,
    artist: station.artist || '',
    album: station.album || '',
    albumart: station.albumart || '',
    type: station.type || 'webradio'
  }));

  fs.writeFileSync(playlistPath, JSON.stringify(playlistEntries, null, 2));
  this.logger.info('[radio_scale_peppy] created seed playlist at ' + playlistPath);
};


ControllerRadioScalePeppy.prototype.ensureMyWebRadiosSeeded = function () {
  const favouritesDir = path.dirname(this.myWebRadioPath);
  if (!fs.existsSync(favouritesDir)) {
    fs.mkdirSync(favouritesDir, { recursive: true });
  }

  let entries = [];
  if (fs.existsSync(this.myWebRadioPath)) {
    try {
      const raw = fs.readFileSync(this.myWebRadioPath, 'utf8');
      const parsed = raw && raw.trim() ? JSON.parse(raw) : [];
      if (Array.isArray(parsed)) {
        entries = parsed.filter((item) => item && typeof item === 'object');
      }
    } catch (err) {
      this.logger.warn('[radio_scale_peppy] failed to parse my-web-radio, recreating: ' + err.message);
      entries = [];
    }
  }

  const existing = new Set(entries.map((item) => {
    const uri = String(item.uri || '').trim();
    const name = this.normalizeTextKey(item.name || item.title || '');
    return [uri, name].join('::');
  }));

  let changed = false;
  this.getSeedStations().forEach((station) => {
    const key = [String(station.uri || '').trim(), this.normalizeTextKey(station.title || station.name || '')].join('::');
    const uriOnly = String(station.uri || '').trim();
    const hasUri = entries.some((entry) => String(entry.uri || '').trim() === uriOnly);
    const hasName = entries.some((entry) => this.normalizeTextKey(entry.name || entry.title || '') === this.normalizeTextKey(station.title || station.name || ''));
    if (!existing.has(key) && !hasUri && !hasName) {
      entries.push({
        service: station.service || 'webradio',
        name: station.title || station.name,
        uri: station.uri
      });
      existing.add(key);
      changed = true;
    }
  });

  if (changed || !fs.existsSync(this.myWebRadioPath)) {
    fs.writeFileSync(this.myWebRadioPath, JSON.stringify(entries, null, 2));
    this.logger.info('[radio_scale_peppy] ensured My Web Radios seed at ' + this.myWebRadioPath);
  }
};

ControllerRadioScalePeppy.prototype.loadMyWebRadioStations = function () {
  let entries = [];
  try {
    if (!fs.existsSync(this.myWebRadioPath)) {
      return [];
    }
    const raw = fs.readFileSync(this.myWebRadioPath, 'utf8');
    const parsed = raw && raw.trim() ? JSON.parse(raw) : [];
    entries = this.parseExternalStationEntries(parsed);
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] failed to load My Web Radios: ' + err.message);
    return [];
  }

  if (!entries.length) {
    return [];
  }

  const configured = this.parseStationsJson(this.getStringConfig('stationsJson', '[]'));
  const seedByKey = new Map();
  configured.concat(this.getSeedStations()).forEach((station) => {
    const keys = [station.name, station.title].concat(Array.isArray(station.match) ? station.match : []);
    keys.forEach((key) => {
      const normalized = this.normalizeTextKey(key);
      if (normalized && !seedByKey.has(normalized)) {
        seedByKey.set(normalized, station);
      }
    });
  });

  const usedBuckets = new Set();
  const stations = [];
  const seen = new Set();
  entries.forEach((entry) => {
    const title = String(entry.title || entry.name || '').trim();
    const uri = String(entry.uri || '').trim();
    if (!title || !uri) {
      return;
    }
    const normalizedTitle = this.normalizeTextKey(title);
    const known = seedByKey.get(normalizedTitle) || null;
    let freq = this.extractFrequencyFromText(title);
    if (!Number.isFinite(freq) && known && Number.isFinite(Number(known.freq))) {
      freq = Number(known.freq);
    }
    if (Number.isFinite(freq)) {
      usedBuckets.add(Math.round((freq - this.getNumberConfig('scaleStart', 87.5)) * 10));
    }
    const station = {
      name: known && known.name ? String(known.name) : title,
      title: title,
      freq: Number.isFinite(freq) ? freq : null,
      match: this.buildPlaylistMatchList(known && known.name ? known.name : title),
      uri,
      service: String(entry.service || (known && known.service) || 'webradio'),
      artist: String(entry.artist || ''),
      album: String(entry.album || ''),
      albumart: String(entry.albumart || ''),
      type: String(entry.type || (known && known.type) || 'webradio')
    };
    if (!Number.isFinite(station.freq)) {
      station.freq = this.computeDeterministicStationFrequency(station, usedBuckets);
    }
    const seenKey = [this.normalizeTextKey(station.name || station.title), station.uri].join('::');
    if (seen.has(seenKey)) {
      return;
    }
    seen.add(seenKey);
    stations.push(station);
  });

  return stations;
};

ControllerRadioScalePeppy.prototype.parsePlaylistFile = function (filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return [];
    }
    const raw = fs.readFileSync(filePath, 'utf8');
    if (!raw || !raw.trim()) {
      return [];
    }
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed.filter((item) => item && typeof item === 'object');
    }
    if (parsed && typeof parsed === 'object') {
      return Object.keys(parsed).map((key) => parsed[key]).filter((item) => item && typeof item === 'object');
    }
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] failed to parse playlist ' + filePath + ': ' + err.message);
  }
  return [];
};

ControllerRadioScalePeppy.prototype.extractFrequencyFromText = function (value) {
  const text = String(value || '');
  if (!text) {
    return null;
  }
  const match = text.match(/(8[7-9]|9\d|10\d)([\.,])(\d)/);
  if (!match) {
    return null;
  }
  const freq = Number((match[1] + '.' + match[3]).replace(',', '.'));
  if (!Number.isFinite(freq)) {
    return null;
  }
  const start = this.getNumberConfig('scaleStart', 87.5);
  const end = this.getNumberConfig('scaleEnd', 108.0);
  if (freq < start || freq > end) {
    return null;
  }
  return Math.round(freq * 10) / 10;
};

ControllerRadioScalePeppy.prototype.computeDeterministicStationFrequency = function (stationLike, usedFrequencies) {
  const start = this.getNumberConfig('scaleStart', 87.5);
  const end = this.getNumberConfig('scaleEnd', 108.0);
  const range = end - start;
  const bucketCount = Math.max(1, Math.round(range * 10));
  const token = [stationLike && stationLike.title, stationLike && stationLike.name, stationLike && stationLike.uri].filter(Boolean).join('|');
  let hash = 0;
  for (let i = 0; i < token.length; i += 1) {
    hash = ((hash << 5) - hash) + token.charCodeAt(i);
    hash |= 0;
  }
  let slot = Math.abs(hash) % bucketCount;
  while (usedFrequencies.has(slot)) {
    slot = (slot + 7) % bucketCount;
  }
  usedFrequencies.add(slot);
  const freq = start + (slot / 10);
  return Math.round(freq * 10) / 10;
};

ControllerRadioScalePeppy.prototype.hashStationBucketSeed = function (stationLike) {
  const token = [stationLike && stationLike.title, stationLike && stationLike.name, stationLike && stationLike.uri].filter(Boolean).join('|');
  let hash = 0;
  for (let i = 0; i < token.length; i += 1) {
    hash = ((hash << 5) - hash) + token.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash || 0);
};

ControllerRadioScalePeppy.prototype.assignAdaptiveStationFrequencies = function (stations) {
  const start = this.getNumberConfig('scaleStart', 87.5);
  const end = this.getNumberConfig('scaleEnd', 108.0);
  const range = Math.max(0.1, end - start);
  const bucketCount = Math.max(1, Math.round(range * 10));
  const minSpacingBuckets = Math.max(3, Math.min(14, Math.round(this.getNumberConfig('stationMinSpacingMHz', 1.0) * 10)));
  const clampBucket = (bucket) => Math.max(0, Math.min(bucketCount, bucket));
  const maxDisplayedStations = Math.max(12, Math.round(this.getNumberConfig('maxDisplayedStations', 12)));

  const withMeta = stations.map((station) => {
    const parsedFreq = Number(station && station.freq);
    const hasRealishFreq = Number.isFinite(parsedFreq) && parsedFreq >= start && parsedFreq <= end;
    return {
      station,
      seed: this.hashStationBucketSeed(station),
      hasRealishFreq,
      preferredBucket: hasRealishFreq
        ? clampBucket(Math.round((parsedFreq - start) * 10))
        : null
    };
  });

  const real = withMeta.filter((entry) => entry.hasRealishFreq).sort((a, b) => a.preferredBucket - b.preferredBucket || a.seed - b.seed);
  const unknown = withMeta.filter((entry) => !entry.hasRealishFreq).sort((a, b) => a.seed - b.seed);

  const realBuckets = real.map((entry) => entry.preferredBucket);
  if (realBuckets.length) {
    for (let i = 1; i < realBuckets.length; i += 1) {
      realBuckets[i] = Math.max(realBuckets[i], realBuckets[i - 1] + minSpacingBuckets);
    }
    const overflow = realBuckets[realBuckets.length - 1] - bucketCount;
    if (overflow > 0) {
      for (let i = realBuckets.length - 1; i >= 0; i -= 1) {
        realBuckets[i] -= overflow;
      }
    }
    if (realBuckets[0] < 0) {
      const under = Math.abs(realBuckets[0]);
      for (let i = 0; i < realBuckets.length; i += 1) {
        realBuckets[i] += under;
      }
    }
    for (let pass = 0; pass < 2; pass += 1) {
      for (let i = 0; i < real.length; i += 1) {
        const preferred = real[i].preferredBucket;
        let candidate = Math.max(0, Math.min(bucketCount, preferred));
        if (i > 0) {
          candidate = Math.max(candidate, realBuckets[i - 1] + minSpacingBuckets);
        }
        if (i < real.length - 1) {
          candidate = Math.min(candidate, realBuckets[i + 1] - minSpacingBuckets);
        }
        if (Number.isFinite(candidate)) {
          realBuckets[i] = Math.max(0, Math.min(bucketCount, candidate));
        }
      }
    }
  }

  const occupied = new Set(realBuckets);
  const unknownAssignments = [];
  const canPlace = (bucket) => {
    for (const used of occupied) {
      if (Math.abs(used - bucket) < minSpacingBuckets) {
        return false;
      }
    }
    return true;
  };
  const buildGaps = () => {
    const used = Array.from(occupied).sort((a, b) => a - b);
    const gaps = [];
    let last = 0;
    if (!used.length) {
      gaps.push({ start: 0, end: bucketCount, size: bucketCount });
      return gaps;
    }
    for (let i = 0; i < used.length; i += 1) {
      const current = used[i];
      const gapStart = i === 0 ? 0 : last + minSpacingBuckets;
      const gapEnd = current - minSpacingBuckets;
      if (gapEnd >= gapStart) {
        gaps.push({ start: gapStart, end: gapEnd, size: gapEnd - gapStart + 1 });
      }
      last = current;
    }
    const tailStart = used[used.length - 1] + minSpacingBuckets;
    if (tailStart <= bucketCount) {
      gaps.push({ start: tailStart, end: bucketCount, size: bucketCount - tailStart + 1 });
    }
    return gaps.sort((a, b) => b.size - a.size || a.start - b.start);
  };
  const findNearestAllowed = (preferred, gap) => {
    let candidate = Math.max(gap.start, Math.min(gap.end, preferred));
    if (canPlace(candidate)) {
      return candidate;
    }
    for (let offset = 1; offset <= gap.size; offset += 1) {
      const left = candidate - offset;
      const right = candidate + offset;
      if (left >= gap.start && canPlace(left)) {
        return left;
      }
      if (right <= gap.end && canPlace(right)) {
        return right;
      }
    }
    return null;
  };

  unknown.forEach((entry, index) => {
    const gaps = buildGaps();
    if (!gaps.length) {
      return;
    }
    const candidatePool = gaps.slice(0, Math.min(3, gaps.length));
    const chosenGap = candidatePool[entry.seed % candidatePool.length];
    const fractions = [0.22, 0.38, 0.54, 0.70, 0.82];
    const fraction = fractions[entry.seed % fractions.length];
    const preferred = Math.round(chosenGap.start + ((chosenGap.end - chosenGap.start) * fraction));
    const bucket = findNearestAllowed(preferred, chosenGap);
    if (bucket === null) {
      return;
    }
    occupied.add(bucket);
    unknownAssignments.push({ entry, bucket });
  });

  const normalized = [];
  real.forEach((entry, index) => {
    const bucket = realBuckets[index];
    normalized.push(Object.assign({}, entry.station, {
      freq: Math.round((start + (bucket / 10)) * 10) / 10,
      target_freq: Number(entry.station.freq)
    }));
  });
  unknownAssignments.forEach(({ entry, bucket }) => {
    normalized.push(Object.assign({}, entry.station, {
      freq: Math.round((start + (bucket / 10)) * 10) / 10,
      target_freq: null
    }));
  });

  const sorted = normalized.sort((a, b) => Number(a.freq) - Number(b.freq));
  if (sorted.length <= maxDisplayedStations) {
    return sorted;
  }
  const chosen = [];
  for (let i = 0; i < maxDisplayedStations; i += 1) {
    const idx = Math.min(sorted.length - 1, Math.round((i * (sorted.length - 1)) / Math.max(1, maxDisplayedStations - 1)));
    chosen.push(sorted[idx]);
  }
  const unique = [];
  const seen = new Set();
  chosen.forEach((station) => {
    const key = [station.name, station.uri, station.freq].join('::');
    if (!seen.has(key)) {
      seen.add(key);
      unique.push(station);
    }
  });
  return unique.sort((a, b) => Number(a.freq) - Number(b.freq)).slice(0, maxDisplayedStations);
};

ControllerRadioScalePeppy.prototype.getAdaptiveWindowsForStation = function (station, stations) {
  const list = Array.isArray(stations) ? stations : this.getStations();
  // 1.9.3 retunes the scale for finer mechanical feel.
  // The visual pointer should glide continuously, while station lock itself
  // remains comparatively narrow. Smaller windows reduce the perceived
  // jumpiness and prevent the old "1 cm snap" effect around each sender.
  const globalSnap = Math.max(0.035, Math.min(0.055, this.getNumberConfig('snapWindowMHz', 0.045)));
  const globalRelease = Math.max(globalSnap + 0.025, Math.min(0.14, this.getNumberConfig('releaseWindowMHz', 0.09)));
  const globalNoise = Math.max(globalRelease + 0.07, Math.min(0.45, this.getNumberConfig('noiseWindowMHz', 0.32)));
  const globalMagnetic = Math.max(0.03, Math.min(0.07, this.getNumberConfig('magneticRadiusMHz', 0.04)));
  if (!station || !list.length) {
    return {
      snapWindow: globalSnap,
      releaseWindow: globalRelease,
      noiseWindow: globalNoise,
      magneticRadius: globalMagnetic
    };
  }

  const index = list.findIndex((item) => item.key === station.key);
  const prevGap = index > 0 ? Math.abs(Number(list[index].freq) - Number(list[index - 1].freq)) : null;
  const nextGap = index >= 0 && index < list.length - 1 ? Math.abs(Number(list[index + 1].freq) - Number(list[index].freq)) : null;
  const finiteGaps = [prevGap, nextGap].filter((value) => Number.isFinite(value) && value > 0);
  if (!finiteGaps.length) {
    return {
      snapWindow: globalSnap,
      releaseWindow: globalRelease,
      noiseWindow: globalNoise,
      magneticRadius: globalMagnetic
    };
  }

  const nearestGap = Math.min.apply(null, finiteGaps);
  const snapWindow = Math.min(globalSnap, Math.max(0.035, nearestGap * 0.16));
  const releaseWindow = Math.min(globalRelease, Math.max(snapWindow + 0.03, nearestGap * 0.24));
  const noiseWindow = Math.min(globalNoise, Math.max(releaseWindow + 0.08, nearestGap * 0.42));
  const magneticRadius = Math.min(globalMagnetic, Math.max(0.03, nearestGap * 0.10));

  return {
    snapWindow,
    releaseWindow,
    noiseWindow,
    magneticRadius
  };
};

ControllerRadioScalePeppy.prototype.buildPlaylistMatchList = function (name) {
  const values = [];
  const base = String(name || '').trim();
  if (!base) {
    return values;
  }
  values.push(base);
  values.push(base.toLowerCase());
  values.push(base.replace(/\s+/g, ''));
  values.push(base.replace(/\s+/g, ' '));
  if (/oe\s*3/i.test(base)) {
    values.push('oe3', 'oe 3', 'hitradio oe3');
  }
  if (/fm4/i.test(base)) {
    values.push('fm4', 'orf fm4');
  }
  if (/radio\s*wien/i.test(base)) {
    values.push('radio wien', 'orf radio wien', 'wien');
  }
  if (/krone\s*hit|kronehit/i.test(base)) {
    values.push('kronehit', 'krone hit');
  }
  if (/chillout\s*antenne|antenne\s*bayern\s*chillout/i.test(base)) {
    values.push('chillout antenne', 'antenne bayern chillout', 'chillout');
  }
  if (/oldie\s*antenne|oldies\s*but\s*goldies/i.test(base)) {
    values.push('oldie antenne', 'antenne bayern oldies but goldies', 'oldies but goldies');
  }
  if (/antenne\s*k(a|ä)rnten/i.test(base)) {
    values.push('antenne kärnten', 'antenne karnten');
  }
  if (/deep\s*house/i.test(base)) {
    values.push('deep house radio', 'deep house', 'dhr');
  }
  return Array.from(new Set(values.map((entry) => String(entry).trim()).filter(Boolean)));
};

ControllerRadioScalePeppy.prototype.loadPlaylistStations = function () {
  if (this.getBooleanConfig('playlistAsStationSource', true) !== true) {
    return [];
  }

  const entries = this.parsePlaylistFile(this.getPlaylistPath());
  if (!entries.length) {
    return [];
  }

  const configured = this.parseStationsJson(this.getStringConfig('stationsJson', '[]'));
  const seedByKey = new Map();
  configured.concat(this.getSeedStations()).forEach((station) => {
    const keys = [station.name].concat(Array.isArray(station.match) ? station.match : []);
    keys.forEach((key) => {
      const normalized = this.normalizeTextKey(key);
      if (normalized && !seedByKey.has(normalized)) {
        seedByKey.set(normalized, station);
      }
    });
  });

  const usedBuckets = new Set();
  const stations = [];
  entries.forEach((entry) => {
    const title = String(entry.title || entry.name || '').trim();
    const uri = String(entry.uri || '').trim();
    if (!title || !uri) {
      return;
    }
    const normalizedTitle = this.normalizeTextKey(title);
    const known = seedByKey.get(normalizedTitle) || null;
    let freq = this.extractFrequencyFromText(title);
    if (!Number.isFinite(freq) && known && Number.isFinite(Number(known.freq))) {
      freq = Number(known.freq);
    }
    if (Number.isFinite(freq)) {
      usedBuckets.add(Math.round((freq - this.getNumberConfig('scaleStart', 87.5)) * 10));
    }
    const station = {
      name: known && known.name ? String(known.name) : title,
      title: title,
      freq: Number.isFinite(freq) ? freq : null,
      match: this.buildPlaylistMatchList(known && known.name ? known.name : title),
      uri,
      service: String(entry.service || (known && known.service) || 'webradio'),
      artist: String(entry.artist || ''),
      album: String(entry.album || ''),
      albumart: String(entry.albumart || ''),
      type: String(entry.type || (known && known.type) || 'webradio')
    };
    if (!Number.isFinite(station.freq)) {
      station.freq = this.computeDeterministicStationFrequency(station, usedBuckets);
    }
    stations.push(station);
  });

  return stations;
};

ControllerRadioScalePeppy.prototype.syncTuningConfig = function () {
  this.tuning.autoPlayOnLock = this.getBooleanConfig('autoPlayOnLock', true) !== false;
  this.tuning.controlMode = this.getStringConfig('defaultControlMode', 'normal') === 'scale' ? 'scale' : 'normal';
  this.tuning.tuningMode = this.tuning.controlMode === 'scale'
    ? (this.tuning.autoPlayOnLock ? 'auto' : 'manual')
    : 'normal';
  this.tuning.magneticLockEnabled = this.getBooleanConfig('magneticLockEnabled', true) !== false;
};

ControllerRadioScalePeppy.prototype.writeSettingsFile = function () {
  this.ensureRuntimeDir();
  const settings = {
    enabled: this.isRendererEnabled(),
    fullscreen: this.getBooleanConfig('fullscreen', true) !== false,
    screen_width: this.getNumberConfig('screenWidth', 1920),
    screen_height: this.getNumberConfig('screenHeight', 550),
    fps: this.getNumberConfig('fps', 24),
    visible_fps_cap: this.getNumberConfig('visibleFpsCap', 24),
    hidden_state_reload_ms: this.getNumberConfig('hiddenStateReloadMs', 2000),
    deep_idle_reload_ms: this.getNumberConfig('deepIdleReloadMs', 5000),
    hidden_standby_sleep_ms: this.getNumberConfig('hiddenStandbySleepMs', 250),
    deep_idle_sleep_ms: this.getNumberConfig('deepIdleSleepMs', 1000),
    poll_interval_ms: this.getNumberConfig('pollIntervalMs', 1000),
    info_panel_width: this.getNumberConfig('infoPanelWidth', 430),
    fallback_frequency: this.getNumberConfig('fallbackFrequency', 98.3),
    scale_start: this.getNumberConfig('scaleStart', 87.5),
    scale_end: this.getNumberConfig('scaleEnd', 108.0),
    show_clock: this.getBooleanConfig('showClock', true) !== false,
    show_technical: this.getBooleanConfig('showTechnical', true) !== false,
    tuning_step_mhz: this.getNumberConfig('tuningStepMHz', 0.02),
    snap_window_mhz: this.getNumberConfig('snapWindowMHz', 0.045),
    release_window_mhz: this.getNumberConfig('releaseWindowMHz', 0.09),
    noise_window_mhz: this.getNumberConfig('noiseWindowMHz', 0.32),
    auto_play_on_lock: this.getBooleanConfig('autoPlayOnLock', true) !== false,
    pause_on_unlock: this.getBooleanConfig('stopOnUnlock', false) === true,
    auto_resolve_from_library: this.getBooleanConfig('autoResolveFromLibrary', true) !== false,
    search_fallback: this.getBooleanConfig('searchFallback', true) !== false,
    playlist_name: this.getPlaylistName(),
    playlist_as_station_source: this.getBooleanConfig('playlistAsStationSource', true) !== false,
    audio_hiss_enabled: this.getBooleanConfig('audioHissEnabled', true) !== false,
    audio_hiss_device: this.getStringConfig('audioHissDevice', 'default'),
    magnetic_lock_enabled: this.getBooleanConfig('magneticLockEnabled', true) !== false,
    magnetic_radius_mhz: Math.max(0.03, this.getNumberConfig('magneticRadiusMHz', 0.04)),
    magnetic_strength: Math.max(0.01, this.getNumberConfig('magneticStrength', 0.02)),
    pointer_visual_follow_gain: this.getNumberConfig('pointerVisualFollowGain', 0.38),
    pointer_visual_locked_gain: this.getNumberConfig('pointerVisualLockedGain', 0.48),
    pointer_idle_lock_ms: this.getNumberConfig('pointerIdleLockMs', 220),
    pointer_startup_settle_ms: this.getNumberConfig('pointerStartupSettleMs', 900),
    pointer_settle_epsilon_mhz: this.getNumberConfig('pointerSettleEpsilonMHz', 0.004),
    hiss_start_delay_ms: this.getNumberConfig('hissStartDelayMs', 1600),
    pointer_jitter_enabled: this.getBooleanConfig('pointerJitterEnabled', false) === true,
    lock_visual_snap_enabled: this.getBooleanConfig('lockVisualSnapEnabled', false) === true,
    scale_vertical_offset: Math.max(78, this.getNumberConfig('scaleVerticalOffset', 78)),
    station_label_levels: this.getNumberConfig('stationLabelLevels', 3),
    use_layer_theme: this.getBooleanConfig('useLayerTheme', true) !== false,
    theme_name: this.getStringConfig('themeName', 'braun_hd'),
    shared_overlay_owner_path: this.sharedOverlayOwnerPath,
    stations: this.getStations()
  };

  fs.writeFileSync(this.settingsPath, JSON.stringify(settings, null, 2));
};

ControllerRadioScalePeppy.prototype.startPolling = function () {
  const intervalMs = Math.max(250, this.getNumberConfig('pollIntervalMs', 1000));

  this.stopPolling();
  this.pollTimer = setInterval(() => {
    this.pollState();
  }, intervalMs);

  this.pollState();
};

ControllerRadioScalePeppy.prototype.stopPolling = function () {
  if (this.pollTimer) {
    clearInterval(this.pollTimer);
    this.pollTimer = null;
  }
};

ControllerRadioScalePeppy.prototype.pollState = function () {
  return Promise.resolve()
    .then(() => this.commandRouter.volumioGetState())
    .then((state) => {
      const normalized = this.normalizeState(state || {});
      this.lastVolumioState = normalized;
      this.ensureTuningSeed(normalized);
      const effective = this.applyTuningOverlay(normalized);
      this.writeStateIfChanged(effective);
      this.syncHissWithState(effective);
      return effective;
    })
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] pollState failed: ' + err.message);
      return null;
    });
};

ControllerRadioScalePeppy.prototype.writeStateIfChanged = function (payload) {
  const digest = JSON.stringify(payload);
  if (digest !== this.lastStateDigest) {
    this.lastStateDigest = digest;
    this.writeStateFile(payload);
  }
};

ControllerRadioScalePeppy.prototype.writeStateFile = function (payload) {
  this.ensureRuntimeDir();
  fs.writeFileSync(this.statePath, JSON.stringify(payload, null, 2));
};

ControllerRadioScalePeppy.prototype.buildIdleState = function () {
  return {
    timestamp: Date.now(),
    status: 'stop',
    source_type: 'idle',
    service: '',
    title: '',
    artist: '',
    album: '',
    volume: 0,
    mute: false,
    samplerate: '',
    bitdepth: '',
    track_type: '',
    uri: '',
    duration: 0,
    seek: 0,
    albumart: '',
    active_frequency: this.getNumberConfig('fallbackFrequency', 98.3),
    matched_station: null,
    tuning_position: this.getNumberConfig('fallbackFrequency', 98.3),
    tuning_locked: false,
    tuning_mode: this.getStringConfig('defaultControlMode', 'scale') === 'scale' ? (this.getBooleanConfig('autoPlayOnLock', true) ? 'auto' : 'manual') : 'normal',
    ui_mode: this.getControlMode(),
    tuning_noise: 1,
    tuning_station: null,
    tuning_nearest_station: null,
    tuning_distance: null,
    tuning_last_interaction_ts: 0,
    tuning_last_locked_freq: null,
    tuning_last_stable_position: null,
    overlay_opened_at: 0
  };
};

ControllerRadioScalePeppy.prototype.normalizeState = function (state) {
  const combinedText = [
    state.service,
    state.trackType,
    state.title,
    state.artist,
    state.album,
    state.uri,
    state.albumart,
    state.stream,
    state.channels
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  const sourceType = this.detectSourceType(state);
  const matchedStation = this.resolveStation(state, combinedText, sourceType);

  if (matchedStation && state.uri) {
    this.learnStationFromState(matchedStation, state);
  }

  return {
    timestamp: Date.now(),
    status: state.status || 'stop',
    source_type: sourceType,
    service: state.service || '',
    title: state.title || '',
    artist: state.artist || '',
    album: state.album || '',
    volume: Number(state.volume || 0),
    mute: Boolean(state.mute),
    samplerate: state.samplerate || '',
    bitdepth: state.bitdepth || '',
    track_type: state.trackType || '',
    uri: state.uri || '',
    duration: Number(state.duration || 0),
    seek: Number(state.seek || 0),
    albumart: state.albumart || '',
    active_frequency: matchedStation ? Number(matchedStation.freq) : this.computeFallbackFrequency(combinedText),
    matched_station: matchedStation,
    raw_state: state
  };
};

ControllerRadioScalePeppy.prototype.detectSourceType = function (state) {
  const service = String(state.service || '').toLowerCase();
  const uri = String(state.uri || '').toLowerCase();
  const trackType = String(state.trackType || '').toLowerCase();

  if (
    uri.startsWith('http://') ||
    uri.startsWith('https://') ||
    service.includes('webradio') ||
    service.includes('radio') ||
    trackType.includes('radio')
  ) {
    return 'webradio';
  }

  if (service.includes('spotify') || trackType.includes('spotify')) {
    return 'spotify';
  }

  if (service.includes('airplay') || trackType.includes('airplay')) {
    return 'airplay';
  }

  if (service.includes('bluetooth') || trackType.includes('bluetooth')) {
    return 'bluetooth';
  }

  return 'other';
};

ControllerRadioScalePeppy.prototype.resolveStation = function (state, combinedText) {
  const stations = this.getStations();
  const lower = (combinedText || '').toLowerCase();

  for (const station of stations) {
    const matchList = Array.isArray(station.match) ? station.match : [];
    const found = matchList.some((entry) => lower.includes(String(entry).toLowerCase()));
    if (found) {
      return this.enrichStationPlayableInfo(station);
    }
    if (station.uri && state.uri && station.uri === state.uri) {
      return this.enrichStationPlayableInfo(station);
    }
  }

  return null;
};

ControllerRadioScalePeppy.prototype.computeFallbackFrequency = function (combinedText) {
  const start = this.getNumberConfig('scaleStart', 87.5);
  const end = this.getNumberConfig('scaleEnd', 108.0);
  const fallback = this.getNumberConfig('fallbackFrequency', 98.3);

  if (!combinedText) {
    return fallback;
  }

  let hash = 0;
  for (let i = 0; i < combinedText.length; i += 1) {
    hash = ((hash << 5) - hash) + combinedText.charCodeAt(i);
    hash |= 0;
  }

  const normalized = Math.abs(hash % 1000) / 1000;
  const freq = start + ((end - start) * normalized);
  return Math.round(freq * 10) / 10;
};

ControllerRadioScalePeppy.prototype.parseStationsJson = function (rawValue) {
  try {
    const parsed = JSON.parse(String(rawValue || '[]'));
    if (!Array.isArray(parsed)) {
      return [];
    }

    return parsed
      .filter((item) => item && typeof item === 'object')
      .map((item) => ({
        name: String(item.name || '').trim(),
        freq: Number(item.freq || 0),
        match: Array.isArray(item.match) ? item.match.map((entry) => String(entry)) : [],
        uri: item.uri ? String(item.uri) : '',
        service: item.service ? String(item.service) : 'webradio',
        title: item.title ? String(item.title) : String(item.name || '').trim(),
        artist: item.artist ? String(item.artist) : '',
        album: item.album ? String(item.album) : '',
        albumart: item.albumart ? String(item.albumart) : '',
        type: item.type ? String(item.type) : 'webradio'
      }))
      .filter((item) => item.name && Number.isFinite(item.freq));
  } catch (err) {
    this.logger.warn('[radio_scale_peppy] invalid stationsJson, using empty list');
    return [];
  }
};

ControllerRadioScalePeppy.prototype.getStations = function () {
  const myWebRadioStations = this.loadMyWebRadioStations();
  const playlistStations = this.loadPlaylistStations();
  const baseStations = myWebRadioStations.length
    ? myWebRadioStations
    : (playlistStations.length
      ? playlistStations
      : this.parseStationsJson(this.getStringConfig('stationsJson', '[]')));

  const normalizedBase = this.assignAdaptiveStationFrequencies(
    baseStations.filter((item) => item && item.name)
  );

  const stations = normalizedBase
    .filter((item) => item && item.name && Number.isFinite(Number(item.freq)))
    .sort((a, b) => Number(a.freq) - Number(b.freq))
    .map((station, index) => Object.assign({}, station, {
      key: this.buildStationKey(station, index),
      match: Array.isArray(station.match) ? station.match.slice() : this.buildPlaylistMatchList(station.name || station.title || '')
    }));

  return stations.map((station) => this.enrichStationPlayableInfo(station));
};

ControllerRadioScalePeppy.prototype.buildStationKey = function (station, index) {
  return [station.name || 'station', String(station.freq || ''), station.uri || '', String(index)].join('::');
};

ControllerRadioScalePeppy.prototype.loadStationCache = function () {
  try {
    return JSON.parse(fs.readFileSync(this.stationCachePath, 'utf8')) || {};
  } catch (err) {
    return {};
  }
};

ControllerRadioScalePeppy.prototype.saveStationCache = function () {
  this.ensureRuntimeDir();
  fs.writeFileSync(this.stationCachePath, JSON.stringify(this.stationCache, null, 2));
};


ControllerRadioScalePeppy.prototype.normalizeTextKey = function (value) {
  return String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '');
};

ControllerRadioScalePeppy.prototype.buildStationQueryList = function (station) {
  const values = [];
  if (station && station.name) {
    values.push(station.name);
  }
  if (station && Array.isArray(station.match)) {
    station.match.forEach((entry) => values.push(entry));
  }
  return Array.from(new Set(values.filter(Boolean).map((entry) => String(entry).trim()).filter(Boolean)));
};

ControllerRadioScalePeppy.prototype.getStationSourceWatchPaths = function () {
  const paths = [this.myWebRadioPath];
  const playlistPath = this.getPlaylistPath();
  if (playlistPath) {
    paths.push(playlistPath);
  }
  return Array.from(new Set(paths.filter(Boolean)));
};

ControllerRadioScalePeppy.prototype.startStationSourceWatchers = function () {
  this.stopStationSourceWatchers();

  const debounceMs = Math.max(500, this.getNumberConfig('stationSourceResyncDebounceMs', 1200));
  this.stationSourceWatchPaths = this.getStationSourceWatchPaths();
  this.stationSourceChangeHandler = () => {
    if (this.stationSourceWatchTimer) {
      clearTimeout(this.stationSourceWatchTimer);
    }
    this.stationSourceWatchTimer = setTimeout(() => {
      this.stationSourceWatchTimer = null;
      this.rebuildStationsFromSources('watch');
    }, debounceMs);
  };

  this.stationSourceWatchPaths.forEach((filePath) => {
    try {
      fs.watchFile(filePath, { interval: 1500 }, (curr, prev) => {
        const currTime = curr && Number.isFinite(curr.mtimeMs) ? curr.mtimeMs : 0;
        const prevTime = prev && Number.isFinite(prev.mtimeMs) ? prev.mtimeMs : 0;
        const currSize = curr && Number.isFinite(curr.size) ? curr.size : 0;
        const prevSize = prev && Number.isFinite(prev.size) ? prev.size : 0;
        if (currTime !== prevTime || currSize !== prevSize) {
          this.logger.info('[radio_scale_peppy] station source changed: ' + filePath);
          this.stationSourceChangeHandler();
        }
      });
    } catch (err) {
      this.logger.warn('[radio_scale_peppy] failed to watch station source ' + filePath + ': ' + err.message);
    }
  });
};

ControllerRadioScalePeppy.prototype.stopStationSourceWatchers = function () {
  if (this.stationSourceWatchTimer) {
    clearTimeout(this.stationSourceWatchTimer);
    this.stationSourceWatchTimer = null;
  }
  (this.stationSourceWatchPaths || []).forEach((filePath) => {
    try {
      fs.unwatchFile(filePath);
    } catch (err) {
      // ignore
    }
  });
  this.stationSourceWatchPaths = [];
  this.stationSourceChangeHandler = null;
};

ControllerRadioScalePeppy.prototype.rebuildStationsFromSources = function (reason) {
  try {
    this.refreshExternalStationIndex();
    this.preparedStationPayloads = {};
    this.stationWarmPromises = {};
    this.writeSettingsFile();
    const baseState = this.lastVolumioState || this.buildIdleState();
    this.ensureTuningSeed(baseState);
    const effective = this.applyTuningOverlay(baseState);
    this.writeStateIfChanged(effective);
    this.syncHissWithState(effective);
    this.logger.info('[radio_scale_peppy] rebuilt station sources from ' + reason);
  } catch (err) {
    this.logger.error('[radio_scale_peppy] rebuildStationsFromSources failed: ' + err.stack);
  }
};


ControllerRadioScalePeppy.prototype.parseExternalStationEntries = function (payload) {
  const results = [];

  const visit = (node) => {
    if (!node) {
      return;
    }
    if (Array.isArray(node)) {
      node.forEach(visit);
      return;
    }
    if (typeof node !== 'object') {
      return;
    }

    const uri = node.uri || node.URL || node.url || '';
    const title = node.title || node.name || node.serviceName || node.label || '';
    if (uri && title) {
      results.push({
        title: String(title),
        name: String(title),
        uri: String(uri),
        service: String(node.service || 'webradio'),
        type: String(node.type || 'webradio'),
        albumart: String(node.albumart || node.icon || '')
      });
    }

    Object.keys(node).forEach((key) => {
      if (['uri', 'URL', 'url', 'title', 'name', 'serviceName', 'label', 'service', 'type', 'albumart', 'icon'].includes(key)) {
        return;
      }
      visit(node[key]);
    });
  };

  visit(payload);
  return results;
};

ControllerRadioScalePeppy.prototype.refreshExternalStationIndex = function () {
  const entries = [];

  this.parsePlaylistFile(this.getPlaylistPath()).forEach((entry) => {
    if (entry && entry.uri && (entry.title || entry.name)) {
      entries.push({
        title: String(entry.title || entry.name),
        name: String(entry.title || entry.name),
        uri: String(entry.uri),
        service: String(entry.service || 'webradio'),
        type: String(entry.type || 'webradio'),
        albumart: String(entry.albumart || '')
      });
    }
  });

  this.externalStationSources.forEach((filePath) => {
    try {
      if (!fs.existsSync(filePath)) {
        return;
      }
      const raw = fs.readFileSync(filePath, 'utf8');
      if (!raw || !raw.trim()) {
        return;
      }
      const parsed = JSON.parse(raw);
      this.parseExternalStationEntries(parsed).forEach((entry) => entries.push(entry));
    } catch (err) {
      this.logger.warn('[radio_scale_peppy] failed to parse station source ' + filePath + ': ' + err.message);
    }
  });

  const dedup = new Map();
  entries.forEach((entry) => {
    const key = [this.normalizeTextKey(entry.title || entry.name), entry.uri].join('::');
    if (!dedup.has(key)) {
      dedup.set(key, entry);
    }
  });
  this.externalStationIndex = Array.from(dedup.values());
  return this.externalStationIndex;
};

ControllerRadioScalePeppy.prototype.matchExternalStation = function (station) {
  const list = this.externalStationIndex && this.externalStationIndex.length
    ? this.externalStationIndex
    : this.refreshExternalStationIndex();
  if (!list.length) {
    return null;
  }

  const queries = this.buildStationQueryList(station);
  const normalizedQueries = queries.map((entry) => this.normalizeTextKey(entry)).filter(Boolean);
  if (!normalizedQueries.length) {
    return null;
  }

  let best = null;
  let bestScore = -1;
  list.forEach((entry) => {
    const titleKey = this.normalizeTextKey(entry.title || entry.name);
    let score = 0;
    normalizedQueries.forEach((query) => {
      if (!query || !titleKey) {
        return;
      }
      if (titleKey === query) {
        score = Math.max(score, 100);
      } else if (titleKey.includes(query) || query.includes(titleKey)) {
        score = Math.max(score, 70);
      }
    });
    if (score > bestScore) {
      bestScore = score;
      best = entry;
    }
  });

  return bestScore >= 70 ? best : null;
};


ControllerRadioScalePeppy.prototype.getConfiguredStations = function () {
  return this.getStations();
};

ControllerRadioScalePeppy.prototype.getSortedConfiguredStations = function () {
  return this.getConfiguredStations().slice().sort((a, b) => Number(a.freq) - Number(b.freq));
};

ControllerRadioScalePeppy.prototype.getNeighbourStations = function (focusStation, radius) {
  if (!focusStation || !focusStation.key) {
    return [];
  }
  const stations = this.getSortedConfiguredStations();
  const index = stations.findIndex((station) => station.key === focusStation.key);
  if (index < 0) {
    return [focusStation];
  }
  const result = [];
  for (let offset = -radius; offset <= radius; offset += 1) {
    const station = stations[index + offset];
    if (station) {
      result.push(station);
    }
  }
  return result;
};

ControllerRadioScalePeppy.prototype.getDirectionalWarmStations = function (focusStation, direction, radius, aheadExtra) {
  if (!focusStation || !focusStation.key) {
    return [];
  }

  const stations = this.getSortedConfiguredStations();
  const index = stations.findIndex((station) => station.key === focusStation.key);
  if (index < 0) {
    return [focusStation];
  }

  const normalizedRadius = Math.max(0, Math.min(3, Number(radius || 0)));
  const normalizedAhead = Math.max(0, Math.min(3, Number(aheadExtra || 0)));
  let leftRadius = normalizedRadius;
  let rightRadius = normalizedRadius;

  if (direction > 0) {
    rightRadius += normalizedAhead;
    leftRadius = Math.max(0, normalizedRadius - 1);
  } else if (direction < 0) {
    leftRadius += normalizedAhead;
    rightRadius = Math.max(0, normalizedRadius - 1);
  }

  const result = [];
  for (let offset = -leftRadius; offset <= rightRadius; offset += 1) {
    const station = stations[index + offset];
    if (station) {
      result.push(station);
    }
  }

  return result;
};

ControllerRadioScalePeppy.prototype.getPreparedPayloadTtlMs = function () {
  return Math.max(5000, this.getNumberConfig('preparedPayloadTtlMs', 45000));
};

ControllerRadioScalePeppy.prototype.buildReplaceAndPlayPayload = function (playable) {
  if (!playable || !playable.uri) {
    return null;
  }
  return {
    uri: playable.uri,
    service: playable.service || 'webradio',
    title: playable.title || playable.name,
    artist: playable.artist || '',
    album: playable.album || '',
    albumart: playable.albumart || '',
    type: playable.type || 'webradio'
  };
};

ControllerRadioScalePeppy.prototype.storePreparedPayload = function (playable) {
  if (!playable || !playable.key || !playable.uri) {
    return null;
  }
  const payload = this.buildReplaceAndPlayPayload(playable);
  if (!payload) {
    return null;
  }
  this.preparedStationPayloads[playable.key] = {
    payload,
    preparedAt: Date.now()
  };
  return payload;
};

ControllerRadioScalePeppy.prototype.getPreparedPayload = function (stationKey) {
  if (!stationKey) {
    return null;
  }
  const entry = this.preparedStationPayloads[stationKey];
  if (!entry || !entry.payload) {
    return null;
  }
  if ((Date.now() - Number(entry.preparedAt || 0)) > this.getPreparedPayloadTtlMs()) {
    delete this.preparedStationPayloads[stationKey];
    return null;
  }
  return Object.assign({}, entry.payload);
};

ControllerRadioScalePeppy.prototype.preResolveStation = function (station) {
  if (!station || !station.key) {
    return Promise.resolve(null);
  }

  const playable = this.enrichStationPlayableInfo(station);
  if (playable && playable.playable) {
    this.storePreparedPayload(playable);
    return Promise.resolve(playable);
  }

  if (this.stationWarmPromises[station.key]) {
    return this.stationWarmPromises[station.key];
  }

  const promise = this.resolvePlayableStation(station)
    .then((resolved) => {
      if (resolved && resolved.playable) {
        this.storePreparedPayload(resolved);
        this.logger.info('[radio_scale_peppy] warmed station cache for ' + station.name);
      }
      return resolved;
    })
    .catch((err) => {
      this.logger.warn('[radio_scale_peppy] warm station failed for ' + station.name + ': ' + err.message);
      return null;
    })
    .finally(() => {
      delete this.stationWarmPromises[station.key];
    });

  this.stationWarmPromises[station.key] = promise;
  return promise;
};

ControllerRadioScalePeppy.prototype.warmNearbyStations = function (evalResult, direction) {
  if (this.getBooleanConfig('warmNextStations', true) !== true) {
    return;
  }

  const focusStation = (evalResult && (evalResult.lockedStation || evalResult.nearestStation)) || null;
  if (!focusStation) {
    return;
  }

  const radius = Math.max(0, Math.min(3, Math.round(this.getNumberConfig('warmStationRadius', 1))));
  const aheadExtra = Math.max(0, Math.min(3, Math.round(this.getNumberConfig('warmAheadExtra', 2))));
  const normalizedDirection = direction > 0 ? 1 : direction < 0 ? -1 : 0;
  const focusKey = [focusStation.key, radius, aheadExtra, normalizedDirection].join('::');
  if (this.lastWarmFocusKey === focusKey) {
    return;
  }
  this.lastWarmFocusKey = focusKey;

  this.getDirectionalWarmStations(focusStation, normalizedDirection, radius, aheadExtra).forEach((station) => {
    this.preResolveStation(station);
  });
};

ControllerRadioScalePeppy.prototype.learnResolvedStation = function (station, resolved) {
  if (!station || !station.key || !resolved || !resolved.uri) {
    return null;
  }
  const previous = this.stationCache[station.key] || {};
  const merged = Object.assign({}, previous, {
    uri: String(resolved.uri || ''),
    service: String(resolved.service || station.service || 'webradio'),
    title: String(resolved.title || station.title || station.name || ''),
    artist: String(resolved.artist || previous.artist || station.artist || ''),
    album: String(resolved.album || previous.album || station.album || ''),
    albumart: String(resolved.albumart || previous.albumart || station.albumart || ''),
    type: String(resolved.type || station.type || 'webradio')
  });
  if (JSON.stringify(previous) !== JSON.stringify(merged)) {
    this.stationCache[station.key] = merged;
    this.saveStationCache();
  }
  const playable = this.enrichStationPlayableInfo(station);
  if (playable && playable.playable) {
    this.storePreparedPayload(playable);
  }
  return playable;
};

ControllerRadioScalePeppy.prototype.flattenSearchResults = function (payload) {
  const results = [];
  const visit = (node) => {
    if (!node) {
      return;
    }
    if (Array.isArray(node)) {
      node.forEach(visit);
      return;
    }
    if (typeof node !== 'object') {
      return;
    }
    const uri = node.uri || '';
    const title = node.title || node.name || '';
    if (uri && title) {
      results.push({
        title: String(title),
        name: String(title),
        uri: String(uri),
        service: String(node.service || 'webradio'),
        type: String(node.type || 'webradio'),
        albumart: String(node.albumart || node.icon || ''),
        artist: String(node.artist || ''),
        album: String(node.album || '')
      });
    }
    Object.keys(node).forEach((key) => {
      if (['uri', 'title', 'name', 'service', 'type', 'albumart', 'icon', 'artist', 'album'].includes(key)) {
        return;
      }
      visit(node[key]);
    });
  };
  visit(payload);
  return results;
};

ControllerRadioScalePeppy.prototype.searchStationCandidate = function (station) {
  const queries = this.buildStationQueryList(station);
  const tryNext = (index) => {
    if (index >= queries.length || this.getBooleanConfig('searchFallback', true) !== true) {
      return Promise.resolve(null);
    }
    const query = queries[index];
    return this.httpRequest({
      method: 'GET',
      path: '/api/v1/search?query=' + encodeURIComponent(query)
    }).then((payload) => {
      const candidates = this.flattenSearchResults(payload).filter((entry) => {
        const service = String(entry.service || '').toLowerCase();
        const type = String(entry.type || '').toLowerCase();
        return service.includes('radio') || type.includes('radio') || /^https?:/i.test(String(entry.uri || ''));
      });
      const normalizedQueries = this.buildStationQueryList(station).map((entry) => this.normalizeTextKey(entry));
      let best = null;
      let bestScore = -1;
      candidates.forEach((entry) => {
        const titleKey = this.normalizeTextKey(entry.title || entry.name);
        let score = 0;
        normalizedQueries.forEach((q) => {
          if (!q || !titleKey) {
            return;
          }
          if (titleKey === q) {
            score = Math.max(score, 100);
          } else if (titleKey.includes(q) || q.includes(titleKey)) {
            score = Math.max(score, 60);
          }
        });
        if (score > bestScore) {
          bestScore = score;
          best = entry;
        }
      });
      if (best && best.uri) {
        return best;
      }
      return tryNext(index + 1);
    }).catch((err) => {
      this.logger.warn('[radio_scale_peppy] search fallback failed for ' + query + ': ' + err.message);
      return tryNext(index + 1);
    });
  };
  return tryNext(0);
};

ControllerRadioScalePeppy.prototype.resolvePlayableStation = function (station) {
  const playable = this.enrichStationPlayableInfo(station);
  if (playable && playable.playable) {
    return Promise.resolve(playable);
  }

  if (this.getBooleanConfig('autoResolveFromLibrary', true) === true) {
    const localMatch = this.matchExternalStation(station);
    if (localMatch && localMatch.uri) {
      const resolved = this.learnResolvedStation(station, localMatch);
      if (resolved && resolved.playable) {
        return Promise.resolve(resolved);
      }
    }
  }

  return this.searchStationCandidate(station).then((resolved) => {
    if (resolved && resolved.uri) {
      return this.learnResolvedStation(station, resolved);
    }
    return this.enrichStationPlayableInfo(station);
  });
};

ControllerRadioScalePeppy.prototype.learnStationFromState = function (station, state) {
  if (!station || !station.key || !state || !state.uri) {
    return;
  }
  const learned = {
    uri: String(state.uri || ''),
    service: String(state.service || station.service || 'webradio'),
    title: String(station.title || state.title || station.name || ''),
    artist: String(state.artist || station.artist || ''),
    album: String(state.album || station.album || ''),
    albumart: String(state.albumart || station.albumart || ''),
    type: String(station.type || 'webradio')
  };
  const previous = this.stationCache[station.key] || {};
  const merged = Object.assign({}, previous, learned);
  const prevDigest = JSON.stringify(previous);
  const nextDigest = JSON.stringify(merged);
  if (prevDigest !== nextDigest) {
    this.stationCache[station.key] = merged;
    this.saveStationCache();
  }
  this.storePreparedPayload(this.enrichStationPlayableInfo(station));
};

ControllerRadioScalePeppy.prototype.enrichStationPlayableInfo = function (station) {
  if (!station) {
    return null;
  }
  const cache = this.stationCache[station.key] || {};
  return Object.assign({}, station, {
    uri: station.uri || cache.uri || '',
    service: station.service || cache.service || 'webradio',
    title: station.title || cache.title || station.name,
    artist: station.artist || cache.artist || '',
    album: station.album || cache.album || '',
    albumart: station.albumart || cache.albumart || '',
    type: station.type || cache.type || 'webradio',
    playable: Boolean(station.uri || cache.uri)
  });
};

ControllerRadioScalePeppy.prototype.ensureTuningSeed = function (baseState) {
  if (this.tuning.position !== null && Number.isFinite(this.tuning.position)) {
    return;
  }
  if (Number.isFinite(Number(this.tuning.lastLockedFreq))) {
    this.tuning.position = Number(this.tuning.lastLockedFreq);
    this.tuning.lockedStationKey = this.tuning.lastLockedStationKey || null;
    this.tuning.nearestStationKey = this.tuning.lastLockedStationKey || null;
    this.tuning.noiseLevel = 0;
    return;
  }
  if (baseState && baseState.matched_station && Number.isFinite(Number(baseState.matched_station.freq))) {
    this.tuning.position = Number(baseState.matched_station.freq);
    this.tuning.lockedStationKey = baseState.matched_station.key;
    this.tuning.nearestStationKey = baseState.matched_station.key;
    this.tuning.lastLockedStationKey = baseState.matched_station.key || null;
    this.tuning.lastLockedFreq = Number(baseState.matched_station.freq);
    this.tuning.lastStablePosition = Number(baseState.matched_station.freq);
    this.tuning.noiseLevel = 0;
    return;
  }
  this.tuning.position = Number(baseState && baseState.active_frequency ? baseState.active_frequency : this.getNumberConfig('fallbackFrequency', 98.3));
};

ControllerRadioScalePeppy.prototype.applyTuningOverlay = function (baseState) {
  this.ensureTuningSeed(baseState);
  const tuningEval = this.evaluateTuning();
  const controlMode = this.getControlMode();
  const effective = Object.assign({}, baseState, {
    active_frequency: Number(tuningEval.lockedStation ? tuningEval.lockedStation.freq : tuningEval.position),
    tuning_position: Number(tuningEval.position),
    tuning_locked: Boolean(tuningEval.lockedStation),
    tuning_mode: controlMode === 'scale' ? this.tuning.tuningMode : 'normal',
    ui_mode: controlMode,
    tuning_noise: Number(tuningEval.noiseLevel),
    tuning_station: tuningEval.lockedStation,
    tuning_nearest_station: tuningEval.nearestStation,
    tuning_distance: tuningEval.nearestDistance,
    tuning_last_interaction_ts: Number(this.tuning.lastInteractionTs || 0),
    tuning_last_locked_freq: Number.isFinite(Number(this.tuning.lastLockedFreq)) ? Number(this.tuning.lastLockedFreq) : null,
    tuning_last_stable_position: Number.isFinite(Number(this.tuning.lastStablePosition)) ? Number(this.tuning.lastStablePosition) : null,
    overlay_opened_at: Number(this.overlayOpenedAt || 0),
    matched_station: tuningEval.lockedStation || baseState.matched_station || null
  });

  if (tuningEval.lockedStation) {
    effective.source_type = 'webradio';
  }

  return effective;
};


ControllerRadioScalePeppy.prototype.findNearestStationForPosition = function (position, stations) {
  const list = Array.isArray(stations) ? stations : this.getStations();
  let nearestStation = null;
  let nearestDistance = null;
  for (const station of list) {
    const distance = Math.abs(Number(station.freq) - Number(position));
    if (nearestDistance === null || distance < nearestDistance) {
      nearestStation = station;
      nearestDistance = distance;
    }
  }
  return {
    station: nearestStation,
    distance: nearestDistance
  };
};

ControllerRadioScalePeppy.prototype.applyMagneticLock = function (position, delta) {
  // 1.9.3 intentionally keeps magnetic influence very soft. The physical
  // pointer position should remain continuous and mechanical; sender lock is
  // decided later by evaluateTuning(). This avoids the visible pointer jump
  // that earlier releases produced near a station center frequency.
  if (this.getBooleanConfig('magneticLockEnabled', true) !== true) {
    return position;
  }

  const stations = this.getStations();
  if (!stations.length) {
    return position;
  }

  const scaleStart = this.getNumberConfig('scaleStart', 87.5);
  const scaleEnd = this.getNumberConfig('scaleEnd', 108.0);
  const magneticStrength = Math.max(0.005, Math.min(0.04, this.getNumberConfig('magneticStrength', 0.02)));
  const travelDirection = delta < 0 ? -1 : delta > 0 ? 1 : 0;

  let nextPosition = Number(position);
  const nearestInfo = this.findNearestStationForPosition(nextPosition, stations);
  if (!nearestInfo.station || nearestInfo.distance === null) {
    return Math.max(scaleStart, Math.min(scaleEnd, Math.round(nextPosition * 1000) / 1000));
  }

  const nearestWindows = this.getAdaptiveWindowsForStation(nearestInfo.station, stations);
  if (nearestInfo.distance > nearestWindows.magneticRadius) {
    return Math.max(scaleStart, Math.min(scaleEnd, Math.round(nextPosition * 1000) / 1000));
  }

  const targetFreq = Number(nearestInfo.station.freq);
  const side = targetFreq - nextPosition;
  if (travelDirection !== 0 && Math.sign(side || 0) !== travelDirection) {
    return Math.max(scaleStart, Math.min(scaleEnd, Math.round(nextPosition * 1000) / 1000));
  }

  let proximity = 1 - Math.min(1, nearestInfo.distance / nearestWindows.magneticRadius);
  proximity = proximity * proximity;
  const pull = side * (0.001 + (proximity * 0.0035 * magneticStrength));

  nextPosition += pull;
  nextPosition = Math.max(scaleStart, Math.min(scaleEnd, nextPosition));
  return Math.round(nextPosition * 1000) / 1000;
};

ControllerRadioScalePeppy.prototype.evaluateTuning = function () {
  const stations = this.getStations();
  const position = Number(this.tuning.position || this.config.get('fallbackFrequency') || 98.3);
  const defaultWindows = this.getAdaptiveWindowsForStation(null, stations);

  let nearestStation = null;
  let nearestDistance = null;
  for (const station of stations) {
    const distance = Math.abs(Number(station.freq) - position);
    if (nearestDistance === null || distance < nearestDistance) {
      nearestStation = station;
      nearestDistance = distance;
    }
  }

  const currentLockedStation = stations.find((station) => station.key === this.tuning.lockedStationKey) || null;
  let lockedStation = null;

  if (currentLockedStation) {
    const lockedDistance = Math.abs(Number(currentLockedStation.freq) - position);
    const lockedWindows = this.getAdaptiveWindowsForStation(currentLockedStation, stations);
    if (lockedDistance <= lockedWindows.releaseWindow) {
      lockedStation = currentLockedStation;
      nearestDistance = lockedDistance;
      nearestStation = currentLockedStation;
    }
  }

  const reentryBoostMs = Math.max(0, Math.min(1200, this.getNumberConfig('reentryBoostMs', 450)));
  const reentrySnapMultiplier = Math.max(1, Math.min(1.04, this.getNumberConfig('reentrySnapMultiplier', 1.015)));
  const reentryBoostActive = Boolean(
    this.tuning.recentUnlockStationKey &&
    reentryBoostMs > 0 &&
    (Date.now() - Number(this.tuning.recentUnlockAt || 0)) <= reentryBoostMs
  );

  if (!lockedStation && nearestStation && nearestDistance !== null) {
    const nearestWindows = this.getAdaptiveWindowsForStation(nearestStation, stations);
    let effectiveSnapWindow = nearestWindows.snapWindow;
    if (reentryBoostActive && nearestStation.key === this.tuning.recentUnlockStationKey) {
      effectiveSnapWindow = Math.max(nearestWindows.snapWindow, nearestWindows.snapWindow * reentrySnapMultiplier);
    }
    if (nearestDistance <= effectiveSnapWindow) {
      lockedStation = nearestStation;
    }
  }

  const activeWindows = lockedStation
    ? this.getAdaptiveWindowsForStation(lockedStation, stations)
    : (nearestStation ? this.getAdaptiveWindowsForStation(nearestStation, stations) : defaultWindows);

  if (lockedStation) {
    this.tuning.lastLockedStationKey = lockedStation.key;
    this.tuning.lastLockedFreq = Number(lockedStation.freq);
    this.tuning.lastStablePosition = Number(position);
    this.tuning.recentUnlockStationKey = null;
    this.tuning.recentUnlockAt = 0;
    this.tuning.tuneUnlockPauseApplied = false;
  } else if (currentLockedStation) {
    this.tuning.recentUnlockStationKey = currentLockedStation.key;
    this.tuning.recentUnlockAt = Date.now();
  }

  this.tuning.lockedStationKey = lockedStation ? lockedStation.key : null;
  this.tuning.nearestStationKey = nearestStation ? nearestStation.key : null;
  this.tuning.nearestDistance = nearestDistance;
  this.tuning.noiseLevel = lockedStation ? 0 : Math.max(0, Math.min(1, Number((nearestDistance || activeWindows.noiseWindow) / activeWindows.noiseWindow)));

  return {
    position,
    lockedStation,
    nearestStation,
    nearestDistance,
    noiseLevel: this.tuning.noiseLevel
  };
};

ControllerRadioScalePeppy.prototype.clearPendingActivation = function () {
  if (this.pendingActivationTimer) {
    clearTimeout(this.pendingActivationTimer);
    this.pendingActivationTimer = null;
  }
  this.activationInFlight = null;
  this.activationInFlightPromise = null;
  this.lastActivationIssuedKey = null;
  this.lastActivationIssuedAt = 0;
  this.tuning.pendingActivation = null;
};

ControllerRadioScalePeppy.prototype.scheduleLockedStationActivation = function (station) {
  if (!station || !station.key) {
    this.clearPendingActivation();
    return Promise.resolve({ success: false, reason: 'No locked station' });
  }

  const currentUri = String((this.lastVolumioState && this.lastVolumioState.uri) || '');
  if (
    station.uri &&
    currentUri === station.uri &&
    this.lastVolumioState &&
    this.lastVolumioState.status === 'play'
  ) {
    this.clearPendingActivation();
    this.stopHiss();
    this.tuning.lastActivatedStationKey = station.key;
    this.tuning.tuneUnlockPauseApplied = false;
    return Promise.resolve({ success: true, skipped: true, reason: 'already-playing' });
  }

  const cooldownMs = Math.max(120, Math.min(500, this.getNumberConfig('stationActivationCooldownMs', 220)));
  if (this.activationInFlight && this.activationInFlight.key === station.key && this.activationInFlightPromise) {
    return this.activationInFlightPromise;
  }
  if (this.lastActivationIssuedKey === station.key && (Date.now() - this.lastActivationIssuedAt) < cooldownMs) {
    return Promise.resolve({ success: true, skipped: true, reason: 'cooldown', key: station.key });
  }
  if (this.tuning.pendingActivation && this.tuning.pendingActivation.key === station.key) {
    return Promise.resolve({ success: true, scheduled: true, coalesced: true, key: station.key });
  }

  this.clearPendingActivation();

  const debounceMs = Math.max(25, Math.min(90, this.getNumberConfig('stationActivationDebounceMs', 50)));
  this.tuning.pendingActivation = {
    key: station.key,
    scheduledAt: Date.now(),
    delayMs: debounceMs
  };

  this.pendingActivationTimer = setTimeout(() => {
    const pending = this.tuning.pendingActivation;
    this.pendingActivationTimer = null;
    this.tuning.pendingActivation = null;

    if (!pending || pending.key !== station.key) {
      return;
    }

    this.activateTunedStation(station)
      .then(() => this.pollState())
      .catch((err) => {
        this.logger.warn('[radio_scale_peppy] debounced activation failed: ' + err.message);
      });
  }, debounceMs);

  return Promise.resolve({ success: true, scheduled: true, key: station.key, delayMs: debounceMs });
};

ControllerRadioScalePeppy.prototype.adjustTuning = function (direction, data) {
  const step = Math.max(0.005, this.getNumberConfig('tuningStepMHz', 0.02));
  const delta = data && typeof data.delta !== 'undefined' ? Number(data.delta) : direction;
  const scaleStart = this.getNumberConfig('scaleStart', 87.5);
  const scaleEnd = this.getNumberConfig('scaleEnd', 108.0);

  this.ensureTuningSeed(this.lastVolumioState);
  this.tuning.controlMode = 'scale';
  this.tuning.tuningMode = this.tuning.autoPlayOnLock ? 'auto' : 'manual';
  this.tuning.position = Math.max(scaleStart, Math.min(scaleEnd, Number(this.tuning.position) + (step * delta)));
  this.tuning.position = this.applyMagneticLock(this.tuning.position, delta);
  this.tuning.position = Math.round(this.tuning.position * 1000) / 1000;
  this.tuning.lastInteractionTs = Date.now();
  this.tuning.lastTuneDirection = delta < 0 ? -1 : delta > 0 ? 1 : 0;

  const beforeLockedKey = this.tuning.lockedStationKey;
  const evalResult = this.evaluateTuning();
  const afterLockedKey = this.tuning.lockedStationKey;
  this.warmNearbyStations(evalResult, this.tuning.lastTuneDirection);

  const immediateState = this.applyTuningOverlay(this.lastVolumioState || this.buildIdleState());
  this.writeStateIfChanged(immediateState);
  this.syncHissWithState(immediateState);

  const shouldReactivateLockedStation = Boolean(
    afterLockedKey &&
    this.tuning.autoPlayOnLock && (
      afterLockedKey !== this.tuning.lastActivatedStationKey ||
      !this.lastVolumioState ||
      this.lastVolumioState.status !== 'play'
    )
  );

  if (shouldReactivateLockedStation) {
    this.scheduleLockedStationActivation(evalResult.lockedStation);
  } else if (!afterLockedKey) {
    this.clearPendingActivation();
    return this.stopPlaybackOnUnlock(beforeLockedKey)
      .then(() => Promise.resolve({ success: true, tuning: immediateState }));
  }

  return Promise.resolve({ success: true, tuning: immediateState });
};

ControllerRadioScalePeppy.prototype.activateTunedStation = function (station) {
  this.clearPendingActivation();
  if (!station) {
    return Promise.resolve({ success: false, reason: 'No locked station' });
  }

  return this.resolvePlayableStation(station).then((playable) => {
    if (!playable || !playable.playable) {
      this.toastOnce('warning', PUBLIC_OVERLAY_NAME, `Station ${station.name} could not be resolved to a stream URI`);
      return { success: false, reason: 'Station has no URI' };
    }

    const currentUri = String((this.lastVolumioState && this.lastVolumioState.uri) || '');
    if (currentUri && currentUri === playable.uri && this.lastVolumioState.status === 'play' && !this.tuning.tuneUnlockPauseApplied) {
      this.stopHiss();
      this.tuning.lastActivatedStationKey = playable.key;
      this.tuning.lastLockedStationKey = playable.key;
      this.tuning.lastLockedFreq = Number(station.freq);
      this.tuning.lastStablePosition = Number(station.freq);
      this.tuning.tuneUnlockPauseApplied = false;
      return { success: true, skipped: true };
    }

    const cooldownMs = Math.max(120, Math.min(500, this.getNumberConfig('stationActivationCooldownMs', 220)));
    if (this.activationInFlight && this.activationInFlight.key === playable.key && this.activationInFlightPromise) {
      return this.activationInFlightPromise;
    }
    if (this.lastActivationIssuedKey === playable.key && (Date.now() - this.lastActivationIssuedAt) < cooldownMs && !this.tuning.tuneUnlockPauseApplied) {
      return Promise.resolve({ success: true, skipped: true, reason: 'cooldown', key: playable.key });
    }

    const payload = this.getPreparedPayload(playable.key) || this.storePreparedPayload(playable) || this.buildReplaceAndPlayPayload(playable);

    this.lastActivationIssuedKey = playable.key;
    this.lastActivationIssuedAt = Date.now();
    this.activationInFlight = { key: playable.key, startedAt: this.lastActivationIssuedAt };
    this.logger.info('[radio_scale_peppy] replaceAndPlay ' + JSON.stringify(payload));

    const run = () => this.stopHissAndWait()
      .then(() => this.httpRequest({
        method: 'POST',
        path: '/api/v1/replaceAndPlay',
        json: payload
      }))
      .then((response) => {
        this.tuning.lastActivatedStationKey = playable.key;
        this.tuning.lastLockedStationKey = playable.key;
        this.tuning.lastLockedFreq = Number(station.freq);
        this.tuning.lastStablePosition = Number(station.freq);
        this.tuning.recentUnlockStationKey = null;
        this.tuning.recentUnlockAt = 0;
        this.tuning.tuneUnlockPauseApplied = false;
        this.warmNearbyStations({ lockedStation: station, nearestStation: station }, this.tuning.lastTuneDirection || 0);
        return response;
      })
      .catch((err) => {
        this.commandRouter.pushToastMessage('error', PUBLIC_OVERLAY_NAME, 'Station start failed: ' + err.message);
        throw err;
      })
      .finally(() => {
        if (this.activationInFlight && this.activationInFlight.key === playable.key) {
          this.activationInFlight = null;
          this.activationInFlightPromise = null;
        }
      });

    this.activationInFlightPromise = this.activationSerial
      .catch(() => ({}))
      .then(() => run());
    this.activationSerial = this.activationInFlightPromise.catch(() => ({}));

    return this.activationInFlightPromise;
  });
};

ControllerRadioScalePeppy.prototype.stopPlaybackForUnlock = function (stationKey) {
  const unlockKey = stationKey || this.tuning.lastActivatedStationKey || this.tuning.lockedStationKey || null;
  this.tuning.recentUnlockStationKey = unlockKey;
  this.tuning.recentUnlockAt = Date.now();
  if (this.tuning.tuneUnlockPauseApplied) {
    this.tuning.lastActivatedStationKey = null;
    return Promise.resolve({ success: true, skipped: true });
  }
  return this.restCommand('stop').then((result) => {
    this.tuning.tuneUnlockPauseApplied = true;
    this.tuning.lastActivatedStationKey = null;
    return result;
  }).catch((err) => {
    this.logger.warn('[radio_scale_peppy] stop on unlock failed: ' + err.message);
    this.tuning.lastActivatedStationKey = null;
    return { success: false, reason: err.message };
  });
};

/** Move the virtual pointer one step to the left and re-evaluate lock/noise. */
ControllerRadioScalePeppy.prototype.tuneLeft = function (data) {
  this.logger.info('[radio_scale_peppy] tuneLeft ' + JSON.stringify(data || ''));
  return this.adjustTuning(-1, data);
};

/** Move the virtual pointer one step to the right and re-evaluate lock/noise. */
ControllerRadioScalePeppy.prototype.tuneRight = function (data) {
  this.logger.info('[radio_scale_peppy] tuneRight ' + JSON.stringify(data || ''));
  return this.adjustTuning(1, data);
};

/** Pause or resume playback using Volumio's regular transport logic. */
ControllerRadioScalePeppy.prototype.tunePause = function () {
  this.logger.info('[radio_scale_peppy] tunePause');
  return this.restCommand('pause')
    .then(() => this.pollState())
    .then(() => ({ success: true }));
};

/** Add the currently matched / tuned station to Volumio favourites. */
ControllerRadioScalePeppy.prototype.tuneFavourite = function () {
  this.logger.info('[radio_scale_peppy] tuneFavourite');
  const overlay = this.applyTuningOverlay(this.lastVolumioState || this.buildIdleState());
  const baseStation = overlay.tuning_station || overlay.matched_station || null;

  const resolveCandidate = baseStation
    ? this.resolvePlayableStation(baseStation).catch(() => this.getCurrentStateFavouriteFallback())
    : Promise.resolve(this.getCurrentStateFavouriteFallback());

  return resolveCandidate.then((station) => {
    if (!station || !station.uri) {
      this.commandRouter.pushToastMessage('warning', PUBLIC_OVERLAY_NAME, 'No station available for favourites');
      return { success: false, reason: 'No station available' };
    }

    const payload = {
      uri: station.uri,
      title: station.title || station.name,
      service: station.service || 'webradio'
    };

    return this.emitSocketEvent('addToFavourites', payload)
      .then((result) => {
        this.commandRouter.pushToastMessage('success', PUBLIC_OVERLAY_NAME, `${station.name || station.title} added to favourites`);
        return result;
      })
      .catch((err) => {
        this.commandRouter.pushToastMessage('error', PUBLIC_OVERLAY_NAME, 'Favourite failed: ' + err.message);
        throw err;
      });
  });
};

ControllerRadioScalePeppy.prototype.tuneDoublePress = function () {
  this.logger.info('[radio_scale_peppy] tuneDoublePress');
  return this.toggleControlMode();
};


/**
 * Forward one encoder step to standard Volumio previous/next transport control.
 * This path is used whenever encoder 2 is in `normal` mode.
 */
ControllerRadioScalePeppy.prototype.playbackStep = function (direction) {
  const command = direction < 0 ? 'prev' : 'next';
  this.logger.info('[radio_scale_peppy] playbackStep ' + command);
  return this.restCommand(command)
    .then(() => this.pollState())
    .then(() => ({ success: true, mode: this.getControlMode(), command }));
};

/** Encoder 1 long press is the stable exit gesture back to the Volumio GUI. */
ControllerRadioScalePeppy.prototype.encoder1LongPress = function () {
  this.logger.info('[radio_scale_peppy] encoder1LongPress');
  return this.goToSourceSelect();
};

/** GPIO/button helper that opens the overlay without using the browse tile. */
ControllerRadioScalePeppy.prototype.encoder1OpenScale = function () {
  this.logger.info('[radio_scale_peppy] encoder1OpenScale');
  return this.openScale(true);
};

/**
 * Compatibility alias for installations where encoder 1 short press is mapped
 * directly to the overlay open action.
 */
ControllerRadioScalePeppy.prototype.encoder1ShortPress = function () {
  this.logger.info('[radio_scale_peppy] encoder1ShortPress');
  return this.openScale(true);
};

/**
 * Compatibility alias for GPIO 13 mappings used in rotaryencoder2.
 * Some stable field setups already reference this exact method name.
 */
ControllerRadioScalePeppy.prototype.gpio13OpenScale = function () {
  this.logger.info('[radio_scale_peppy] gpio13OpenScale');
  return this.openScale(true);
};

/** Encoder 1 double press is intentionally disabled to avoid UI crash loops. */
ControllerRadioScalePeppy.prototype.encoder1DoublePress = function () {
  this.logger.info('[radio_scale_peppy] encoder1DoublePress disabled');
  return Promise.resolve({ success: true, disabled: true });
};

/**
 * Encoder 2 left rotation.
 * - in `scale` mode: move the radio pointer
 * - in `normal` mode: forward to Volumio previous track / station
 */
ControllerRadioScalePeppy.prototype.encoder2Left = function (data) {
  this.logger.info('[radio_scale_peppy] encoder2Left ' + JSON.stringify(data || ''));
  if (Date.now() < this.modeSwitchLockUntil) {
    return Promise.resolve({ success: true, ignored: 'mode-switch-guard' });
  }
  if (this.getControlMode() === 'scale') {
    return this.tuneLeft(data);
  }
  return this.playbackStep(-1);
};

/**
 * Encoder 2 right rotation.
 * - in `scale` mode: move the radio pointer
 * - in `normal` mode: forward to Volumio next track / station
 */
ControllerRadioScalePeppy.prototype.encoder2Right = function (data) {
  this.logger.info('[radio_scale_peppy] encoder2Right ' + JSON.stringify(data || ''));
  if (Date.now() < this.modeSwitchLockUntil) {
    return Promise.resolve({ success: true, ignored: 'mode-switch-guard' });
  }
  if (this.getControlMode() === 'scale') {
    return this.tuneRight(data);
  }
  return this.playbackStep(1);
};

/** Encoder 2 short press toggles play/pause. */
ControllerRadioScalePeppy.prototype.encoder2ShortPress = function () {
  this.logger.info('[radio_scale_peppy] encoder2ShortPress');
  return this.tunePause();
};

/** Encoder 2 long press stores the current station as favourite. */
ControllerRadioScalePeppy.prototype.encoder2LongPress = function () {
  this.logger.info('[radio_scale_peppy] encoder2LongPress');
  return this.tuneFavourite();
};

/** Encoder 2 double press switches between scale mode and normal mode. */
ControllerRadioScalePeppy.prototype.encoder2DoublePress = function () {
  this.logger.info('[radio_scale_peppy] encoder2DoublePress');
  return this.toggleControlMode();
};

ControllerRadioScalePeppy.prototype.setScaleMode = function () {
  this.logger.info('[radio_scale_peppy] setScaleMode');
  return this.openScale(true);
};

ControllerRadioScalePeppy.prototype.setNormalMode = function () {
  this.logger.info('[radio_scale_peppy] setNormalMode');
  return this.goToSourceSelect();
};

/** Small status endpoint used by the source plugin and diagnostics. */
ControllerRadioScalePeppy.prototype.getControlStatus = function () {
  return Promise.resolve({
    success: true,
    controlMode: this.getControlMode(),
    tuningMode: this.tuning.tuningMode,
    tuningLocked: Boolean(this.tuning.lockedStationKey),
    rendererRunning: this.isRendererRunning(),
    rendererReady: this.isRendererReady(),
    browseSourceUri: this.browseSourceUri
  });
};

ControllerRadioScalePeppy.prototype.getCurrentFavouriteCandidate = function () {
  const overlay = this.applyTuningOverlay(this.lastVolumioState || this.buildIdleState());
  const station = overlay.tuning_station || overlay.matched_station || null;
  if (station) {
    const playable = this.enrichStationPlayableInfo(station);
    if (playable.playable) {
      return playable;
    }
  }
  return this.getCurrentStateFavouriteFallback();
};

ControllerRadioScalePeppy.prototype.toastOnce = function (type, title, message) {
  const key = [type, title, message].join('|');
  if (this.tuning.lastToastKey === key) {
    return;
  }
  this.tuning.lastToastKey = key;
  this.commandRouter.pushToastMessage(type, title, message);
};

ControllerRadioScalePeppy.prototype.getCurrentStateFavouriteFallback = function () {
  const st = this.lastVolumioState || {};
  if (!st.uri) {
    return null;
  }
  return {
    key: ['runtime', st.uri].join('::'),
    name: st.title || st.service || 'Current Stream',
    title: st.title || st.service || 'Current Stream',
    uri: st.uri,
    service: st.service || 'webradio',
    artist: st.artist || '',
    album: st.album || '',
    albumart: st.albumart || '',
    playable: true
  };
};

ControllerRadioScalePeppy.prototype.getHissAudioDirectory = function () {
  return path.join(this.pluginDir, 'audio');
};

ControllerRadioScalePeppy.prototype.getHissVariantPath = function (variant) {
  const allowed = ['very_weak', 'weak', 'medium', 'strong', 'very_strong'];
  const safeVariant = allowed.includes(String(variant)) ? String(variant) : 'medium';
  return path.join(this.getHissAudioDirectory(), 'hiss_' + safeVariant + '.wav');
};

ControllerRadioScalePeppy.prototype.pickHissVariant = function (noiseLevel) {
  const level = Math.max(0, Math.min(1, Number(noiseLevel || 0)));
  if (level <= 0.08) {
    return null;
  }
  if (level <= 0.24) {
    return 'very_weak';
  }
  if (level <= 0.42) {
    return 'weak';
  }
  if (level <= 0.62) {
    return 'medium';
  }
  if (level <= 0.82) {
    return 'strong';
  }
  return 'very_strong';
};

ControllerRadioScalePeppy.prototype.spawnHissProcess = function (variant) {
  const filePath = this.getHissVariantPath(variant);
  if (!fs.existsSync(filePath)) {
    this.logger.warn('[radio_scale_peppy] hiss file missing: ' + filePath);
    return;
  }

  const audioDevice = this.getStringConfig('audioHissDevice', 'default').replace(/"/g, '\"');
  const quotedPath = filePath.replace(/"/g, '\"');
  const loopCmd = 'while true; do /usr/bin/aplay -q -D "' + audioDevice + '" "' + quotedPath + '"; sleep 0.02; done';

  this.hissLoopWanted = true;
  this.hissVariant = variant;
  this.logger.info('[radio_scale_peppy] starting hiss audio: ' + variant);

  const child = spawn('/bin/bash', ['-lc', loopCmd], {
    detached: true,
    stdio: 'ignore',
    env: Object.assign({}, process.env, {
      HOME: '/home/volumio'
    })
  });

  child.unref();
  this.hissProcess = child;
};

ControllerRadioScalePeppy.prototype.stopHiss = function () {
  this.hissLoopWanted = false;
  this.hissVariant = null;
  if (!this.hissProcess) {
    return;
  }
  try {
    process.kill(-this.hissProcess.pid, 'SIGTERM');
  } catch (err) {
    try {
      this.hissProcess.kill('SIGTERM');
    } catch (killErr) {
      // ignore
    }
  }
  this.hissProcess = null;
};

ControllerRadioScalePeppy.prototype.stopHissAndWait = function () {
  const hadHiss = Boolean(this.hissProcess);
  this.stopHiss();
  if (!hadHiss) {
    return Promise.resolve({ success: true, hadHiss: false });
  }
  const waitMs = Math.max(120, this.getNumberConfig('stationActivationHissReleaseMs', 220));
  return new Promise((resolve) => setTimeout(() => resolve({ success: true, hadHiss: true, waitMs }), waitMs));
};

ControllerRadioScalePeppy.prototype.ensureHissVariant = function (variant) {
  if (!variant) {
    this.stopHiss();
    return;
  }
  if (this.hissProcess && this.hissVariant === variant) {
    return;
  }
  this.stopHiss();
  this.spawnHissProcess(variant);
};

ControllerRadioScalePeppy.prototype.syncHissWithState = function (effectiveState) {
  const hissEnabled = this.getBooleanConfig('audioHissEnabled', true) !== false;
  if (!hissEnabled) {
    this.clearHissSyncTimer();
    this.stopHiss();
    return;
  }

  const mode = String((effectiveState && effectiveState.ui_mode) || this.getControlMode() || 'normal');
  if (mode !== 'scale') {
    this.overlayOpenedAt = 0;
    this.clearHissSyncTimer();
    this.stopHiss();
    return;
  }

  if (effectiveState && effectiveState.tuning_locked) {
    this.clearHissSyncTimer();
    this.stopHiss();
    return;
  }

  if (!this.isRendererReady()) {
    this.clearHissSyncTimer();
    this.stopHiss();
    this.hissSyncTimer = setTimeout(() => {
      this.hissSyncTimer = null;
      const latestState = this.lastVolumioState || this.buildIdleState();
      const effectiveLatest = this.applyTuningOverlay(latestState);
      this.syncHissWithState(effectiveLatest);
    }, 120);
    return;
  }

  const startupDelayMs = Math.max(0, this.getNumberConfig('hissStartDelayMs', 1600));
  const sinceOpenMs = this.overlayOpenedAt ? (Date.now() - this.overlayOpenedAt) : startupDelayMs;
  if (sinceOpenMs < startupDelayMs) {
    this.clearHissSyncTimer();
    this.stopHiss();
    this.hissSyncTimer = setTimeout(() => {
      this.hissSyncTimer = null;
      const latestState = this.lastVolumioState || this.buildIdleState();
      const effectiveLatest = this.applyTuningOverlay(latestState);
      this.syncHissWithState(effectiveLatest);
    }, Math.max(60, startupDelayMs - sinceOpenMs));
    return;
  }

  this.clearHissSyncTimer();
  const variant = this.pickHissVariant(effectiveState ? effectiveState.tuning_noise : 1);
  this.ensureHissVariant(variant);
};

ControllerRadioScalePeppy.prototype.httpRequest = function (options) {
  const method = options.method || 'GET';
  const payload = typeof options.json !== 'undefined' ? JSON.stringify(options.json) : null;
  const headers = Object.assign({}, options.headers || {});

  if (payload) {
    headers['Content-Type'] = 'application/json';
    headers['Content-Length'] = Buffer.byteLength(payload);
  }

  return new Promise((resolve, reject) => {
    const req = http.request({
      host: '127.0.0.1',
      port: 3000,
      path: options.path,
      method,
      headers,
      timeout: options.timeout || 4000
    }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => {
        body += chunk;
      });
      res.on('end', () => {
        if (res.statusCode && res.statusCode >= 400) {
          reject(new Error(`HTTP ${res.statusCode}: ${body}`));
          return;
        }
        if (!body) {
          resolve({ success: true });
          return;
        }
        try {
          resolve(JSON.parse(body));
        } catch (err) {
          resolve(body);
        }
      });
    });

    req.on('timeout', () => {
      req.destroy(new Error('Request timeout'));
    });
    req.on('error', (err) => reject(err));

    if (payload) {
      req.write(payload);
    }
    req.end();
  });
};

ControllerRadioScalePeppy.prototype.restCommand = function (cmd, params) {
  const search = new URLSearchParams(Object.assign({ cmd }, params || {}));
  return this.httpRequest({
    method: 'GET',
    path: '/api/v1/commands/?' + search.toString()
  });
};

ControllerRadioScalePeppy.prototype.emitSocketEvent = function (eventName, payload) {
  return new Promise((resolve, reject) => {
    const socket = io('http://127.0.0.1:3000', {
      forceNew: true,
      reconnection: false,
      transports: ['websocket', 'polling']
    });

    let done = false;
    const timer = setTimeout(() => {
      finish(new Error('WebSocket timeout'));
    }, 4000);

    const finish = (err, result) => {
      if (done) {
        return;
      }
      done = true;
      clearTimeout(timer);
      try {
        socket.disconnect();
      } catch (disconnectErr) {
        // no-op
      }
      if (err) {
        reject(err);
      } else {
        resolve(result || { success: true });
      }
    };

    socket.on('connect', () => {
      socket.emit(eventName, payload || {});
      setTimeout(() => finish(null, { success: true }), 300);
    });
    socket.on('pushToastMessage', (msg) => {
      if (msg && msg.type === 'error') {
        finish(new Error(msg.message || 'Operation failed'));
      }
    });
    socket.on('connect_error', (err) => finish(err instanceof Error ? err : new Error(String(err))));
    socket.on('error', (err) => finish(err instanceof Error ? err : new Error(String(err))));
  });
};

/**
 * Spawn the Python fullscreen renderer.
 *
 * The renderer only reads runtime JSON files. That separation keeps Volumio
 * playback / socket logic in Node.js and limits renderer-side crash impact.
 */
ControllerRadioScalePeppy.prototype.startRenderer = function () {
  if (this.rendererProcess) {
    this.logger.info('[radio_scale_peppy] renderer already running');
    return;
  }
  if (this.isResidentRendererServiceEnabled() && this.isRendererRunning()) {
    this.logger.info('[radio_scale_peppy] resident renderer already running via service');
    return;
  }

  this.clearRendererRetryTimer();
  this.rendererShutdownRequested = false;
  this.clearRendererReadyFlag();
  const launcher = path.join(this.pluginDir, 'run_radio_scale.sh');
  const residentMode = this.isResidentRendererEnabled();
  this.logger.info('[radio_scale_peppy] starting renderer: ' + launcher + ' resident=' + JSON.stringify(residentMode));
  if (!fs.existsSync('/tmp/.X11-unix/X0')) {
    this.logger.warn('[radio_scale_peppy] X11 socket /tmp/.X11-unix/X0 not found - resident preload may retry later');
  }

  this.rendererOwnedByPlugin = true;
  this.rendererProcess = spawn('/bin/bash', [launcher], {
    cwd: this.pluginDir,
    env: Object.assign({}, process.env, {
      RADIO_SCALE_PLUGIN_DIR: this.pluginDir,
      RADIO_SCALE_RESIDENT: residentMode ? '1' : '0',
      DISPLAY: ':0',
      XAUTHORITY: '/home/volumio/.Xauthority',
      SDL_VIDEODRIVER: 'x11',
      SDL_AUDIODRIVER: 'dummy',
      PYGAME_HIDE_SUPPORT_PROMPT: '1'
    }),
    detached: false,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  this.rendererProcess.stdout.on('data', (data) => {
    this.logger.info('[radio_scale_peppy] ' + data.toString().trim());
  });

  this.rendererProcess.stderr.on('data', (data) => {
    this.logger.error('[radio_scale_peppy] ' + data.toString().trim());
  });

  this.rendererProcess.on('close', (code) => {
    this.logger.info('[radio_scale_peppy] renderer exited with code ' + code);
    this.rendererProcess = null;
    this.rendererOwnedByPlugin = false;
    this.clearRendererReadyFlag();
    if (!this.rendererShutdownRequested && this.shouldPreloadResidentRenderer()) {
      this.logger.warn('[radio_scale_peppy] resident renderer exited unexpectedly - scheduling retry');
      this.scheduleResidentRendererStart(this.getNumberConfig('residentRendererRetryMs', 5000));
    }
  });
};

/** Stop the Python renderer process if it is currently running. */
ControllerRadioScalePeppy.prototype.stopRenderer = function () {
  this.clearRendererRetryTimer();
  this.rendererShutdownRequested = true;

  if (this.rendererProcess && this.rendererOwnedByPlugin) {
    try {
      this.rendererProcess.kill('SIGTERM');
    } catch (err) {
      this.logger.warn('[radio_scale_peppy] renderer SIGTERM failed: ' + err.message);
    }
    this.rendererProcess = null;
    this.rendererOwnedByPlugin = false;
  } else if (this.isResidentRendererServiceEnabled() && this.isRendererRunning()) {
    this.logger.info('[radio_scale_peppy] stopRenderer skipped because resident renderer is service-managed');
  }

  this.clearRendererReadyFlag();
};

ControllerRadioScalePeppy.prototype.restartRenderer = function () {
  this.stopRenderer();
  this.startRenderer();
};

ControllerRadioScalePeppy.prototype.normalizeSaveData = function (data) {
  if (Array.isArray(data)) {
    return data.reduce((acc, item) => {
      if (item && typeof item.id !== 'undefined') {
        acc[item.id] = item.value;
      }
      return acc;
    }, {});
  }

  return Object.assign({}, data || {});
};
