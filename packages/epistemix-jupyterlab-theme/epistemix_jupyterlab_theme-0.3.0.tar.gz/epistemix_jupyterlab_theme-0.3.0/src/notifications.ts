import { JupyterFrontEnd } from '@jupyterlab/application';

export function registerNotifications(app: JupyterFrontEnd): void {
  const notifications = createNotifications();
  app.restored.then(() => {
    document.body.appendChild(notifications);
    const container = notifications.firstChild! as HTMLElement;
    const height = container.offsetHeight;
    container.style.marginBottom = `-${height}px`;
    setTimeout(() => {
      container.style.marginBottom = '0px';
      container.classList.add('visible');
    }, 2000);
  });
}

export const notificationList = [
  {
    date: '2022-02-08',
    description: '<p>Added "Introductory-Models" folder to the platform.</p>'
  }
];

function createNotifications() {
  const lastDismissDate = getCookie('lastDismissDate');

  const notifications = document.createElement('div');
  notifications.id = 'jupyterlab-notifications';
  notifications.className = 'jupyterlab-notifications';

  const notificationsContainer = document.createElement('div');
  notificationsContainer.className = 'jupyterlab-notifications-container';

  notifications.appendChild(notificationsContainer);

  const filteredNotifications = notificationList
    .sort((a, b) => {
      const aa = new Date(a.date).getTime();
      const bb = new Date(b.date).getTime();
      return bb - aa;
    })
    .filter(n => n.date > lastDismissDate);

  for (let i = 0; i < filteredNotifications.length; i++) {
    if (i >= 3) {
      break;
    }
    const n = filteredNotifications[i];
    const notification = document.createElement('div');
    notification.className = 'jupyterlab-notification';
    notification.innerHTML = `<i class="notification-date">${
      new Date(n.date).toLocaleString().split(',')[0]
    }</i>${n.description}`;

    const closeButton = document.createElement('button');
    closeButton.className = 'dismiss-notification';
    closeButton.innerHTML =
      '<svg clip-rule="evenodd" fill-rule="evenodd" stroke-linejoin="round" stroke-miterlimit="2" viewBox="0 0 24 24"><path d="m12 10.93 5.719-5.72c.146-.146.339-.219.531-.219.404 0 .75.324.75.749 0 .193-.073.385-.219.532l-5.72 5.719 5.719 5.719c.147.147.22.339.22.531 0 .427-.349.75-.75.75-.192 0-.385-.073-.531-.219l-5.719-5.719-5.719 5.719c-.146.146-.339.219-.531.219-.401 0-.75-.323-.75-.75 0-.192.073-.384.22-.531l5.719-5.719-5.72-5.719c-.146-.147-.219-.339-.219-.532 0-.425.346-.749.75-.749.192 0 .385.073.531.219z"/></svg>';
    closeButton.addEventListener('click', () => {
      const cookieValue = getCookie('lastDismissDate');
      if (!cookieValue || cookieValue <= n.date) {
        setCookie('lastDismissDate', n.date, 365);
      }
      notification.classList.add('hide');
      setTimeout(() => {
        notification.remove();
      }, 500);
    });

    notification.prepend(closeButton);

    notificationsContainer.appendChild(notification);
  }

  return notifications;
}

function setCookie(cname: string, cvalue: string, exdays: number) {
  const d = new Date();
  d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
  const expires = 'expires=' + d.toUTCString();
  document.cookie = cname + '=' + cvalue + ';' + expires + ';path=/';
}

function getCookie(cname: string) {
  const name = cname + '=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}
