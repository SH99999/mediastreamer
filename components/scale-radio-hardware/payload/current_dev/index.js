'use strict';

const libQ = require('kew');
const fs = require('fs-extra');
const io = require('socket.io-client');
const i2c = require('i2c-bus');
const VConf = require('v-conf');

const PLUGIN_NAME = 'Rotary Encoder II Angle Bridge';
const SOCKET_URL = 'http://localhost:3000';
const MAX_ANGLE = 4095;
const REG = {
  STATUS: 0x0B,
  RAW_ANGLE: 0x0C
};

module.exports = ControllerRotaryEncoderIIAngleBridge;

function ControllerRotaryEncoderIIAngleBridge(context) {
  this.context = context;
  this.commandRouter = context.coreCommand;
  this.logger = context.logger;

  this.config = null;
  this.socket = null;
  this.i2cHandle = null;
  this.i2cHandleBus = null;
  this.pollTimer = null;

  this.lastBucket = null;
  this.lastVolume = null;
  this.lastToastAt = 0;
  this.lastButtonAt = 0;

  this.currentState = {
    available: false,
    magnetDetected: false,
    magnetTooWeak: false,
    magnetTooStrong: false,
    rawAngle: 0,
    normalized: 0,
    percent: 0,
    bucket: 0,
    calibration: {
      rawMin: 0,
      rawMax: MAX_ANGLE,
      invertDirection: false
    },
    buttons: {
      enabled: false,
      lastButton: null
    }
  };
}

ControllerRotaryEncoderIIAngleBridge.prototype.onVolumioStart = function() {
  const configFile = this.commandRouter.pluginManager.getConfigurationFile(this.context, 'config.json');
  this.config = new VConf();
  this.config.loadFile(configFile);
  this.ensureDefaultConfig();
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.onStart = function() {
  try {
    this.connectSocket();
    if (this.config.get('enabled')) {
      this.startPolling();
    }
  }
  catch (error) {
    this.logger.error(PLUGIN_NAME + ': onStart failed: ' + error.message);
  }
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.onStop = function() {
  this.stopPolling();
  this.disconnectSocket();
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.onRestart = function() {
  this.restartRuntime();
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.onInstall = function() {
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.onUninstall = function() {
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.getConfigurationFiles = function() {
  return ['config.json'];
};

ControllerRotaryEncoderIIAngleBridge.prototype.getUIConfig = function() {
  const defer = libQ.defer();
  const self = this;
  const langCode = self.commandRouter.sharedVars.get('language_code') || 'en';

  self.commandRouter.i18nJson(
    __dirname + '/i18n/strings_' + langCode + '.json',
    __dirname + '/i18n/strings_en.json',
    __dirname + '/UIConfig.json'
  ).then(function(uiconf) {
    // Sensor section
    uiconf.sections[0].content[0].value = !!self.config.get('enabled');
    uiconf.sections[0].content[1].value = self.selectValue(self.getIntConfig('i2cBus', 1), self.getIntConfig('i2cBus', 1) === 1 ? '1 (GPIO2/GPIO3)' : String(self.getIntConfig('i2cBus', 1)));
    uiconf.sections[0].content[2].value = String(self.config.get('i2cAddress') || '0x36');
    uiconf.sections[0].content[3].value = self.getIntConfig('pollIntervalMs', 50);
    uiconf.sections[0].content[4].value = !!self.config.get('startupToast');

    // Calibration section
    uiconf.sections[1].content[0].value = !!self.config.get('invertDirection');
    uiconf.sections[1].content[1].value = self.getIntConfig('rawMin', 0);
    uiconf.sections[1].content[2].value = self.getIntConfig('rawMax', MAX_ANGLE);
    uiconf.sections[1].content[3].value = self.getIntConfig('resolutionSteps', 20);

    // Angle action section
    const actionType = String(self.config.get('actionType') || 'toast_percent');
    uiconf.sections[2].content[0].value = self.selectValue(actionType, self.getActionLabel(actionType));
    uiconf.sections[2].content[1].value = self.getIntConfig('toastCooldownMs', 350);
    uiconf.sections[2].content[2].value = self.getIntConfig('volumeStepPercent', 2);
    uiconf.sections[2].content[3].value = String(self.config.get('emitEndpoint') || '');
    uiconf.sections[2].content[4].value = String(self.config.get('emitMethod') || '');
    uiconf.sections[2].content[5].value = String(self.config.get('emitData') || '{}');

    // Button section
    const buttonActionType = String(self.config.get('buttonActionType') || 'transport');
    uiconf.sections[3].content[0].value = !!self.config.get('buttonsEnabled');
    uiconf.sections[3].content[1].value = self.selectValue(buttonActionType, self.getButtonActionLabel(buttonActionType));
    uiconf.sections[3].content[2].value = self.getIntConfig('buttonDebounceMs', 120);
    uiconf.sections[3].content[3].value = String(self.config.get('buttonEndpoint') || '');
    uiconf.sections[3].content[4].value = String(self.config.get('buttonMethod') || '');
    uiconf.sections[3].content[5].value = String(self.config.get('buttonData') || '{}');

    defer.resolve(uiconf);
  }).fail(function(error) {
    self.logger.error(PLUGIN_NAME + ': failed to load UIConfig: ' + error);
    defer.reject(error);
  });

  return defer.promise;
};

ControllerRotaryEncoderIIAngleBridge.prototype.saveSensorConfig = function(data) {
  this.config.set('enabled', !!data.enabled);
  this.config.set('i2cBus', this.extractSelectedValue(data.i2cBus, 1));
  this.config.set('i2cAddress', String(data.i2cAddress || '0x36').trim());
  this.config.set('pollIntervalMs', this.clamp(this.parseIntSafe(data.pollIntervalMs, 50), 20, 1000));
  this.config.set('startupToast', !!data.startupToast);

  this.restartRuntime();
  this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Sensor settings saved');
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.saveCalibrationConfig = function(data) {
  this.config.set('invertDirection', !!data.invertDirection);
  this.config.set('rawMin', this.clamp(this.parseIntSafe(data.rawMin, 0), 0, MAX_ANGLE));
  this.config.set('rawMax', this.clamp(this.parseIntSafe(data.rawMax, MAX_ANGLE), 0, MAX_ANGLE));
  this.config.set('resolutionSteps', this.clamp(this.parseIntSafe(data.resolutionSteps, 20), 2, 200));

  this.resetLiveState();
  this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Calibration saved');
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.saveActionConfig = function(data) {
  this.config.set('actionType', this.extractSelectedValue(data.actionType, 'toast_percent'));
  this.config.set('toastCooldownMs', this.clamp(this.parseIntSafe(data.toastCooldownMs, 350), 0, 5000));
  this.config.set('volumeStepPercent', this.clamp(this.parseIntSafe(data.volumeStepPercent, 2), 1, 20));
  this.config.set('emitEndpoint', String(data.emitEndpoint || '').trim());
  this.config.set('emitMethod', String(data.emitMethod || '').trim());
  this.config.set('emitData', String(data.emitData || '{}').trim() || '{}');

  this.resetLiveState();
  this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Angle action settings saved');
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.saveButtonConfig = function(data) {
  this.config.set('buttonsEnabled', !!data.buttonsEnabled);
  this.config.set('buttonActionType', this.extractSelectedValue(data.buttonActionType, 'transport'));
  this.config.set('buttonDebounceMs', this.clamp(this.parseIntSafe(data.buttonDebounceMs, 120), 40, 1000));
  this.config.set('buttonEndpoint', String(data.buttonEndpoint || '').trim());
  this.config.set('buttonMethod', String(data.buttonMethod || '').trim());
  this.config.set('buttonData', String(data.buttonData || '{}').trim() || '{}');
  this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Button settings saved');
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.probeSensor = function() {
  try {
    const frame = this.readSensorFrame();
    const state = this.processFrame(frame, true);
    this.config.set('lastProbeRaw', state.rawAngle);
    this.config.set('lastProbePercent', state.percent);
    this.config.set('lastProbeMagnet', state.magnetDetected);

    this.commandRouter.pushToastMessage(
      'info',
      PLUGIN_NAME,
      'RAW ' + state.rawAngle + ' | ' + state.percent + '% | magnet ' + (state.magnetDetected ? 'OK' : 'missing')
    );
    return libQ.resolve(state);
  }
  catch (error) {
    this.commandRouter.pushToastMessage('error', PLUGIN_NAME, error.message);
    return libQ.reject(error);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.captureMin = function() {
  return this.captureCalibrationValue('rawMin', 'Minimum');
};

ControllerRotaryEncoderIIAngleBridge.prototype.captureMax = function() {
  return this.captureCalibrationValue('rawMax', 'Maximum');
};

ControllerRotaryEncoderIIAngleBridge.prototype.resetCalibration = function() {
  this.config.set('rawMin', 0);
  this.config.set('rawMax', MAX_ANGLE);
  this.resetLiveState();
  this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Calibration reset to 0-4095');
  return libQ.resolve();
};

ControllerRotaryEncoderIIAngleBridge.prototype.showCurrentState = function() {
  const state = this.currentState || {};
  const message = state.available
    ? ('RAW ' + state.rawAngle + ' | ' + state.percent + '% | bucket ' + state.bucket)
    : 'No processed state yet. Use probe or enable live polling.';

  this.commandRouter.pushToastMessage('info', PLUGIN_NAME, message);
  return libQ.resolve(state);
};

ControllerRotaryEncoderIIAngleBridge.prototype.simulateButtonPress = function(data) {
  const button = String((data && data.button) || 'select').trim().toLowerCase();
  this.handleButtonPress(button, true);
  return libQ.resolve({ ok: true, button: button });
};

ControllerRotaryEncoderIIAngleBridge.prototype.getCurrentState = function() {
  return libQ.resolve(this.currentState);
};

ControllerRotaryEncoderIIAngleBridge.prototype.captureCalibrationValue = function(configKey, label) {
  try {
    const frame = this.readSensorFrame();
    const raw = frame.rawAngle;
    this.config.set(configKey, raw);
    this.resetLiveState();
    this.commandRouter.pushToastMessage('success', PLUGIN_NAME, label + ' captured: ' + raw);
    return libQ.resolve({ key: configKey, value: raw });
  }
  catch (error) {
    this.commandRouter.pushToastMessage('error', PLUGIN_NAME, error.message);
    return libQ.reject(error);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.ensureDefaultConfig = function() {
  const defaults = {
    enabled: false,
    i2cBus: 1,
    i2cAddress: '0x36',
    pollIntervalMs: 50,
    invertDirection: false,
    rawMin: 0,
    rawMax: MAX_ANGLE,
    actionType: 'toast_percent',
    resolutionSteps: 20,
    toastCooldownMs: 350,
    volumeStepPercent: 2,
    emitEndpoint: '',
    emitMethod: '',
    emitData: '{}',
    buttonsEnabled: false,
    buttonActionType: 'transport',
    buttonDebounceMs: 120,
    buttonEndpoint: '',
    buttonMethod: '',
    buttonData: '{}',
    startupToast: true,
    lastProbeRaw: 0,
    lastProbePercent: 0,
    lastProbeMagnet: false
  };

  Object.keys(defaults).forEach((key) => {
    if (this.config.get(key) === undefined) {
      this.config.set(key, defaults[key]);
    }
  });
};

ControllerRotaryEncoderIIAngleBridge.prototype.connectSocket = function() {
  if (this.socket) {
    return;
  }

  this.socket = io.connect(SOCKET_URL, {
    reconnection: true,
    forceNew: false
  });
};

ControllerRotaryEncoderIIAngleBridge.prototype.disconnectSocket = function() {
  if (this.socket) {
    try {
      this.socket.disconnect();
    }
    catch (error) {
      this.logger.warn(PLUGIN_NAME + ': socket disconnect error: ' + error.message);
    }
    this.socket = null;
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.startPolling = function() {
  this.stopPolling();
  this.openBus();

  const pollIntervalMs = this.clamp(this.getIntConfig('pollIntervalMs', 50), 20, 1000);
  this.pollTimer = setInterval(() => {
    try {
      const frame = this.readSensorFrame();
      const state = this.processFrame(frame, false);
      this.executeAngleAction(state);
    }
    catch (error) {
      this.logger.error(PLUGIN_NAME + ': poll error: ' + error.message);
    }
  }, pollIntervalMs);

  if (this.config.get('startupToast')) {
    this.commandRouter.pushToastMessage('success', PLUGIN_NAME, 'Live polling started on I2C bus ' + this.getIntConfig('i2cBus', 1));
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.stopPolling = function() {
  if (this.pollTimer) {
    clearInterval(this.pollTimer);
    this.pollTimer = null;
  }
  this.closeBus();
};

ControllerRotaryEncoderIIAngleBridge.prototype.restartRuntime = function() {
  this.stopPolling();
  this.resetLiveState();

  if (this.config.get('enabled')) {
    try {
      this.startPolling();
    }
    catch (error) {
      this.commandRouter.pushToastMessage('error', PLUGIN_NAME, error.message);
    }
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.resetLiveState = function() {
  this.lastBucket = null;
  this.lastVolume = null;
  this.lastToastAt = 0;
};

ControllerRotaryEncoderIIAngleBridge.prototype.openBus = function() {
  const busNumber = this.getIntConfig('i2cBus', 1);
  const devicePath = '/dev/i2c-' + busNumber;

  if (!fs.existsSync(devicePath)) {
    throw new Error('I2C bus ' + busNumber + ' not found (' + devicePath + '). Enable I2C first.');
  }

  if (this.i2cHandle && this.i2cHandleBus === busNumber) {
    return;
  }

  this.closeBus();
  this.i2cHandle = i2c.openSync(busNumber);
  this.i2cHandleBus = busNumber;
};

ControllerRotaryEncoderIIAngleBridge.prototype.closeBus = function() {
  if (this.i2cHandle) {
    try {
      this.i2cHandle.closeSync();
    }
    catch (error) {
      this.logger.warn(PLUGIN_NAME + ': closeBus warning: ' + error.message);
    }
    this.i2cHandle = null;
    this.i2cHandleBus = null;
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.readSensorFrame = function() {
  this.openBus();

  const address = this.getAddress();
  const status = this.i2cHandle.readByteSync(address, REG.STATUS);
  const buffer = Buffer.alloc(2);
  this.i2cHandle.readI2cBlockSync(address, REG.RAW_ANGLE, 2, buffer);

  const rawAngle = (((buffer[0] & 0x0F) << 8) | buffer[1]) & 0x0FFF;

  return {
    status: status,
    rawAngle: rawAngle,
    magnetDetected: !!(status & 0x20),
    magnetTooWeak: !!(status & 0x10),
    magnetTooStrong: !!(status & 0x08)
  };
};

ControllerRotaryEncoderIIAngleBridge.prototype.processFrame = function(frame, manualOnly) {
  const normalized = this.mapRawToNormalized(frame.rawAngle);
  const percent = Math.round(normalized * 100);
  const bucket = this.getBucket(normalized);

  this.currentState = {
    available: true,
    magnetDetected: frame.magnetDetected,
    magnetTooWeak: frame.magnetTooWeak,
    magnetTooStrong: frame.magnetTooStrong,
    rawAngle: frame.rawAngle,
    normalized: normalized,
    percent: percent,
    bucket: bucket,
    manualOnly: !!manualOnly,
    calibration: {
      rawMin: this.getIntConfig('rawMin', 0),
      rawMax: this.getIntConfig('rawMax', MAX_ANGLE),
      invertDirection: !!this.config.get('invertDirection')
    },
    buttons: {
      enabled: !!this.config.get('buttonsEnabled'),
      lastButton: this.currentState && this.currentState.buttons ? this.currentState.buttons.lastButton : null
    }
  };

  return this.currentState;
};

ControllerRotaryEncoderIIAngleBridge.prototype.executeAngleAction = function(state) {
  const actionType = String(this.config.get('actionType') || 'toast_percent');

  if (!state.magnetDetected) {
    return;
  }

  switch (actionType) {
    case 'none':
      break;
    case 'toast_percent':
      this.toastPercent(state);
      break;
    case 'volumio_volume':
      this.mapToVolume(state);
      break;
    case 'custom_emit':
      this.customEmit(state);
      break;
    default:
      this.logger.warn(PLUGIN_NAME + ': unknown actionType ' + actionType);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.toastPercent = function(state) {
  const now = Date.now();
  const cooldownMs = this.getIntConfig('toastCooldownMs', 350);

  if (this.lastBucket !== state.bucket && now - this.lastToastAt >= cooldownMs) {
    this.commandRouter.pushToastMessage('info', PLUGIN_NAME, 'Angle ' + state.percent + '% (raw ' + state.rawAngle + ')');
    this.lastBucket = state.bucket;
    this.lastToastAt = now;
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.mapToVolume = function(state) {
  if (!this.socket) {
    return;
  }

  const step = this.clamp(this.getIntConfig('volumeStepPercent', 2), 1, 20);
  const quantizedVolume = this.clamp(Math.round(state.percent / step) * step, 0, 100);

  if (this.lastVolume !== quantizedVolume) {
    this.socket.emit('volume', quantizedVolume);
    this.lastVolume = quantizedVolume;
    this.lastBucket = state.bucket;
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.customEmit = function(state) {
  if (!this.socket || this.lastBucket === state.bucket) {
    return;
  }

  const endpoint = String(this.config.get('emitEndpoint') || '').trim();
  const method = String(this.config.get('emitMethod') || '').trim();
  const extraData = this.parseJsonConfig('emitData');

  if (!endpoint || !method || !extraData) {
    return;
  }

  this.socket.emit('callMethod', {
    endpoint: endpoint,
    method: method,
    data: Object.assign({}, extraData, {
      sensor: {
        rawAngle: state.rawAngle,
        normalized: state.normalized,
        percent: state.percent,
        bucket: state.bucket,
        magnetDetected: state.magnetDetected,
        magnetTooWeak: state.magnetTooWeak,
        magnetTooStrong: state.magnetTooStrong
      }
    })
  });

  this.lastBucket = state.bucket;
};

ControllerRotaryEncoderIIAngleBridge.prototype.handleButtonPress = function(button, fromGui) {
  if (!this.config.get('buttonsEnabled')) {
    this.commandRouter.pushToastMessage('warning', PLUGIN_NAME, 'Buttons are disabled in settings');
    return;
  }

  const now = Date.now();
  const debounceMs = this.getIntConfig('buttonDebounceMs', 120);
  if (now - this.lastButtonAt < debounceMs) {
    return;
  }
  this.lastButtonAt = now;

  const mode = String(this.config.get('buttonActionType') || 'transport');
  if (mode === 'transport') {
    this.emitTransport(button);
  }
  else if (mode === 'volume_step') {
    this.emitVolumeStep(button);
  }
  else if (mode === 'custom_emit') {
    this.emitButtonCustom(button);
  }

  if (!this.currentState.buttons) {
    this.currentState.buttons = {};
  }
  this.currentState.buttons.lastButton = button;

  if (fromGui) {
    this.commandRouter.pushToastMessage('info', PLUGIN_NAME, 'Button simulated: ' + button);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.emitTransport = function(button) {
  if (!this.socket) {
    return;
  }
  if (button === 'prev') {
    this.socket.emit('prev');
  }
  else if (button === 'next') {
    this.socket.emit('next');
  }
  else {
    this.socket.emit('pause');
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.emitVolumeStep = function(button) {
  if (!this.socket) {
    return;
  }

  const state = this.currentState || {};
  const basePercent = Number.isFinite(state.percent) ? state.percent : 50;
  const delta = button === 'next' ? 5 : (button === 'prev' ? -5 : 0);
  const nextVolume = this.clamp(basePercent + delta, 0, 100);
  this.socket.emit('volume', nextVolume);
};

ControllerRotaryEncoderIIAngleBridge.prototype.emitButtonCustom = function(button) {
  if (!this.socket) {
    return;
  }

  const endpoint = String(this.config.get('buttonEndpoint') || '').trim();
  const method = String(this.config.get('buttonMethod') || '').trim();
  const extraData = this.parseJsonConfig('buttonData');

  if (!endpoint || !method || !extraData) {
    return;
  }

  this.socket.emit('callMethod', {
    endpoint: endpoint,
    method: method,
    data: Object.assign({}, extraData, {
      button: button,
      sensor: {
        rawAngle: this.currentState.rawAngle,
        percent: this.currentState.percent
      }
    })
  });
};

ControllerRotaryEncoderIIAngleBridge.prototype.mapRawToNormalized = function(raw) {
  const rawMin = this.clamp(this.getIntConfig('rawMin', 0), 0, MAX_ANGLE);
  const rawMax = this.clamp(this.getIntConfig('rawMax', MAX_ANGLE), 0, MAX_ANGLE);
  let normalized;

  if (rawMin === rawMax) {
    normalized = raw / MAX_ANGLE;
  }
  else {
    const span = (rawMax - rawMin + 4096) % 4096;
    const offset = (raw - rawMin + 4096) % 4096;

    if (offset <= span) {
      normalized = offset / span;
    }
    else {
      const distanceToMin = this.circularDistance(raw, rawMin);
      const distanceToMax = this.circularDistance(raw, rawMax);
      normalized = distanceToMin <= distanceToMax ? 0 : 1;
    }
  }

  if (this.config.get('invertDirection')) {
    normalized = 1 - normalized;
  }

  return this.clamp(normalized, 0, 1);
};

ControllerRotaryEncoderIIAngleBridge.prototype.circularDistance = function(a, b) {
  const forward = (a - b + 4096) % 4096;
  const backward = (b - a + 4096) % 4096;
  return Math.min(forward, backward);
};

ControllerRotaryEncoderIIAngleBridge.prototype.getBucket = function(normalized) {
  const steps = this.clamp(this.getIntConfig('resolutionSteps', 20), 2, 200);
  return this.clamp(Math.round(normalized * (steps - 1)), 0, steps - 1);
};

ControllerRotaryEncoderIIAngleBridge.prototype.getAddress = function() {
  return this.parseAddress(this.config.get('i2cAddress') || '0x36');
};

ControllerRotaryEncoderIIAngleBridge.prototype.parseAddress = function(value) {
  if (typeof value === 'number') {
    return value;
  }

  const stringValue = String(value).trim().toLowerCase();
  if (stringValue.indexOf('0x') === 0) {
    return parseInt(stringValue, 16);
  }
  return parseInt(stringValue, 10);
};

ControllerRotaryEncoderIIAngleBridge.prototype.extractSelectedValue = function(value, fallback) {
  if (value && typeof value === 'object' && value.value !== undefined) {
    return value.value;
  }
  if (value !== undefined && value !== null && value !== '') {
    return value;
  }
  return fallback;
};

ControllerRotaryEncoderIIAngleBridge.prototype.selectValue = function(value, label) {
  return { value: value, label: label };
};

ControllerRotaryEncoderIIAngleBridge.prototype.getActionLabel = function(actionType) {
  switch (actionType) {
    case 'none':
      return 'Do nothing (monitor only)';
    case 'toast_percent':
      return 'Toast current percent';
    case 'volumio_volume':
      return 'Map angle to Volumio volume';
    case 'custom_emit':
      return 'Call another plugin method';
    default:
      return String(actionType);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.getButtonActionLabel = function(actionType) {
  switch (actionType) {
    case 'transport':
      return 'Volumio transport';
    case 'volume_step':
      return 'Volume step';
    case 'custom_emit':
      return 'Call another plugin method';
    default:
      return String(actionType);
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.parseJsonConfig = function(key) {
  const raw = String(this.config.get(key) || '{}').trim() || '{}';
  try {
    return JSON.parse(raw);
  }
  catch (error) {
    this.commandRouter.pushToastMessage('error', PLUGIN_NAME, 'Invalid JSON in ' + key);
    return null;
  }
};

ControllerRotaryEncoderIIAngleBridge.prototype.getIntConfig = function(key, fallback) {
  return this.parseIntSafe(this.config.get(key), fallback);
};

ControllerRotaryEncoderIIAngleBridge.prototype.parseIntSafe = function(value, fallback) {
  const parsed = parseInt(value, 10);
  return Number.isNaN(parsed) ? fallback : parsed;
};

ControllerRotaryEncoderIIAngleBridge.prototype.clamp = function(value, min, max) {
  return Math.max(min, Math.min(max, value));
};
