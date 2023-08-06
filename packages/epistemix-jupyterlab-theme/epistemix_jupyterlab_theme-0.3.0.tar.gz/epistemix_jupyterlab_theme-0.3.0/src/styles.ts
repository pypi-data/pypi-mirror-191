import { IThemeManager } from '@jupyterlab/apputils';

export function registerStyles(manager: IThemeManager): void {
  const style = 'epistemix_jupyterlab_theme/index.css';

  manager.register({
    name: 'Epistemix',
    isLight: false,
    load: () => manager.loadCSS(style),
    unload: () => Promise.resolve(undefined)
  });
}
