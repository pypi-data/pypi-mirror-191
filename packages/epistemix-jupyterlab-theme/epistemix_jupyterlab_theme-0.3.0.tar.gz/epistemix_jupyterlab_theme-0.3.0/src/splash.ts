import { JupyterFrontEnd } from '@jupyterlab/application';
import { Dialog, ISplashScreen } from '@jupyterlab/apputils';
import { Throttler } from '@lumino/polling';
import { DisposableDelegate } from '@lumino/disposable';

const SPLASH_RECOVER_TIMEOUT = 12000;

const reset = 'apputils:reset';

export function registerSplash(app: JupyterFrontEnd): ISplashScreen {
  const { commands, restored } = app;

  const splash = createSplash();
  const news = createNews();
  console.log(news);

  // Create debounced recovery dialog function.
  let dialog: Dialog<unknown> | null;
  const recovery = new Throttler(
    async () => {
      if (dialog) {
        return;
      }

      dialog = new Dialog({
        title: 'Loading...',
        body: `The loading screen is taking a long time. 
Would you like to clear the workspace or keep waiting?`,
        buttons: [
          Dialog.cancelButton({ label: 'Keep Waiting' }),
          Dialog.warnButton({ label: 'Clear Workspace' })
        ]
      });

      try {
        const result = await dialog.launch();
        dialog.dispose();
        dialog = null;
        if (result.button.accept && commands.hasCommand(reset)) {
          return commands.execute(reset);
        }

        // Re-invoke the recovery timer in the next frame.
        requestAnimationFrame(() => {
          // Because recovery can be stopped, handle invocation rejection.
          void recovery.invoke().catch(() => undefined);
        });
      } catch (error) {
        /* no-op */
      }
    },
    { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' }
  );

  // Return ISplashScreen.
  let splashCount = 0;
  return {
    show: () => {
      splashCount++;

      document.body.appendChild(splash);
      // document.body.appendChild(news);

      // Because recovery can be stopped, handle invocation rejection.
      void recovery.invoke().catch(() => undefined);

      return new DisposableDelegate(async () => {
        await restored;
        if (--splashCount === 0) {
          void recovery.stop();

          if (dialog) {
            dialog.dispose();
            dialog = null;
          }

          splash.classList.add('splash-fade');
          window.setTimeout(() => {
            document.body.removeChild(splash);
          }, 200);
        }
      });
    }
  };
}

function createSplash() {
  const splash = document.createElement('div');
  splash.id = 'jupyterlab-splash';
  splash.className = 'jupyterlab-splash';
  splash.style.backgroundColor = '#000533';
  splash.style.display = 'flex';
  splash.style.justifyContent = 'center';
  splash.style.alignItems = 'center';

  const logo = document.createElement('div');
  logo.id = 'main-logo';
  logo.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="360" height="50" viewBox="0 0 360 50">
      <title>Epistemix</title>
      <path d="m337.43 31.87-4.28 5.14h-8.32l8.87-9.73 3.73 4.59Zm-10.01-19.86h7.56l6.19 7.73 6.08-7.73h8.25l-9.37 11.92 10.66 13.08h-8.76l-20.61-25Zm-27.42 25v-25h8v25h-8Zm-55 0v-25h10l7.89 13.67 7.71-13.67H281v25h-8V20.26l-9.33 16.75h-2.65l-9-16.75v16.75H245Zm-43 0v-25h24v5h-16v5h14v5h-14v5h17v5h-25Zm-34 0v-20h-9v-5h26v5h-9v20h-8Zm-37.27.46c-9.39 0-14.25-3-14.64-8.46h8c.39 1.82 1.89 3.25 6.5 3.25 3.61 0 5.68-.89 5.68-2.57 0-1.68-1.86-2.07-6.71-2.54-9.11-.79-12.61-3-12.61-8 0-4.75 4.79-8 12.89-8 8.1 0 12.79 2.43 13.43 7.86h-7.89c-.5-1.75-2.25-2.64-5.46-2.64-3.39 0-5 .75-5 2.21s1.29 1.82 6.32 2.29c8.36.68 13.11 2.39 13.11 8.07-.01 5.07-4.74 8.53-13.63 8.53h.01ZM91 37.01v-25h8v25h-8Zm-35-13h4.5c2.9 0 4.5-1.17 4.5-3.52v-.09c0-2.38-1.67-3.34-4.47-3.34H56v6.95Zm-8 13v-25h12.83c8.22 0 12.17 2.76 12.17 8.21v.18c0 5.38-4.3 8.65-11.83 8.65H56v8l-8-.04Zm-21-15v5H13v5h17v5H5v-15h22Zm-22-5v-5h24v5H5Z" fill="#e8ecfc"/>
    </svg>
  `;

  splash.appendChild(logo);

  return splash;
}

function createNews() {
  const news = document.createElement('div');
  news.id = 'jupyterlab-news';
  news.className = 'jupyterlab-news visible';

  const newsModal = document.createElement('div');
  newsModal.className = 'news-modal';
  newsModal.innerHTML = '<p>This is the news!</p>';

  news.appendChild(newsModal);

  const closeButton = document.createElement('button');
  closeButton.className = 'close-news';
  closeButton.innerText = 'Continue';
  closeButton.addEventListener('click', () => {
    news.classList.remove('visible');
  });

  newsModal.appendChild(closeButton);

  // news.classList.add('visible');

  return news;
}
