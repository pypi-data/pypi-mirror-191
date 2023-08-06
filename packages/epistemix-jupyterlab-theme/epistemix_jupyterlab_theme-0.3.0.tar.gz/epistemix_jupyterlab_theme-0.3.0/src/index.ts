import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import {
  ICommandPalette,
  ISplashScreen,
  IThemeManager
} from '@jupyterlab/apputils';
import { ICodeMirror } from '@jupyterlab/codemirror';

import { registerFRED } from './fred-language';
import { registerStyles } from './styles';
import { registerSplash } from './splash';
import { registerWelcomePage } from './welcome';
import { registerNotifications } from './notifications';

const theme: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:theme',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    registerStyles(manager);
  }
};

const fred: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:fred',
  autoStart: true,
  requires: [ICodeMirror],
  activate: (app: JupyterFrontEnd, codeMirror: ICodeMirror) => {
    registerFRED(app, codeMirror.CodeMirror);
  }
};

const splash: JupyterFrontEndPlugin<ISplashScreen> = {
  id: 'epistemix_jupyterlab_theme:splash',
  autoStart: true,
  provides: ISplashScreen,
  activate: (app: JupyterFrontEnd) => {
    return registerSplash(app);
  }
};

const launcher: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:launcher',
  autoStart: true,
  requires: [ICommandPalette],
  activate: (app: JupyterFrontEnd, palette: ICommandPalette) => {
    registerWelcomePage(app, palette);
  }
};

const notifications: JupyterFrontEndPlugin<void> = {
  id: 'epistemix_jupyterlab_theme:notifications',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    registerNotifications(app);
  }
};

const plugins = [theme, fred, splash, launcher, notifications];

export default plugins;
