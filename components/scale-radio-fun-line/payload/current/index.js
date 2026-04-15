'use strict';

const libQ = require('kew');
const fs = require('fs');
const path = require('path');
const vConf = require('v-conf');

module.exports = ControllerFunLineaOverlay;

function ControllerFunLineaOverlay(context) {
  this.context = context;
  this.commandRouter = context.coreCommand;
  this.logger = context.logger;
  this.configManager = context.configManager;
  this.config = new vConf();
}

ControllerFunLineaOverlay.prototype.onVolumioStart = function () {
  const configFile = this.commandRouter.pluginManager.getConfigurationFile(this.context, 'config.json');
  this.config = new vConf();
  this.config.loadFile(configFile);
  return libQ.resolve();
};

ControllerFunLineaOverlay.prototype.onStart = function () {
  this.logger.info('[fun_linea_overlay] onStart');
  return libQ.resolve();
};

ControllerFunLineaOverlay.prototype.onStop = function () {
  this.logger.info('[fun_linea_overlay] onStop');
  return libQ.resolve();
};

ControllerFunLineaOverlay.prototype.getUIConfig = function () {
  try {
    const uiConfigPath = path.join(__dirname, 'UIConfig.json');
    const payload = fs.readFileSync(uiConfigPath, 'utf8');
    return libQ.resolve(JSON.parse(payload));
  } catch (err) {
    this.logger.error('[fun_linea_overlay] getUIConfig failed: ' + err.message);
    return libQ.reject(err);
  }
};

ControllerFunLineaOverlay.prototype.getConfigurationFiles = function () {
  return ['config.json'];
};
