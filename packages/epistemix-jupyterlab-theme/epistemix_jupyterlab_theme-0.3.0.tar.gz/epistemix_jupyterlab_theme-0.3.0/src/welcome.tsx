import React from 'react';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { ICommandPalette, ReactWidget } from '@jupyterlab/apputils';
import { notificationList } from './notifications';

class ExampleWidget extends ReactWidget {
  constructor() {
    super();
    this.addClass('welcome-widget');
    this.addClass('jp-RenderedHTMLCommon');
    this.id = 'welcome-widget';
    this.title.label = 'Welcome';
    this.title.closable = true;
    this.title.iconClass = 'fa fa-door-open';
  }

  render() {
    return (
      <div className="welcome-widget-content">
        <h1>Welcome to the Epistemix Platform!</h1>
        <p>
          The Epistemix Platform is a web-based IDE that will enable you to
          design, run, and analyze agent-based models with FRED, the Framework
          for Reconstructing Epidemiological Dynamics.
        </p>
        <h2>Getting Started</h2>
        <p>
          On the left of the screen, you will find your home folder, as well as
          the files in your current working directory.
        </p>
        <p>
          Use your mouse to navigate to the Quickstart Guide and complete each
          lesson.
        </p>
        <h2>Additional Resources</h2>
        <ul>
          <li>
            <a href="https://docs.epistemix.com/">Documentation Home Page</a>
          </li>
          <li>
            <a href="https://epistemix.discourse.group/">Discourse Forum</a>
          </li>
          <li>
            <a href="https://blog.epistemix.com/blog/">Blog</a>
          </li>
        </ul>
        <p>
          For any other questions, please email{' '}
          <a href="mailto:learning@epistemix.com">learning@epistemix.com</a>.
        </p>
        <h2>Things to Note</h2>
        <p>
          Changes made to the contents of the Quickstart Guide and other
          pre-populated folders are not considered persistent. Updates to the
          guides can cause any changes that you've made to them to be
          overwritten. When writing a model, ensure that you are not working in
          a subdirectory of any of the existing guides.
        </p>
        <p>
          <i>
            Tip: To reopen this page, open the command palette (<kbd>Shift</kbd>{' '}
            + <kbd>CMD/CTRL</kbd> + <kbd>C</kbd>) and search "Open Welcome
            Page".
          </i>
        </p>
        <h2>Latest Updates</h2>
        <ul className="welcome-notifications">
          {notificationList.map(n => {
            return (
              <li key={n.date}>
                <i className="notification-date">{n.date}</i>
                <div dangerouslySetInnerHTML={{ __html: n.description }} />
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

export function registerWelcomePage(
  app: JupyterFrontEnd,
  palette: ICommandPalette
): void {
  const command = 'welcome-page:open';

  const createCommand = () => {
    const widget = new ExampleWidget();
    app.shell.add(widget, 'main');
  };

  app.restored.then(() => {
    const widgets = app.shell.widgets('main');
    if (!widgets.next()) {
      createCommand();
    }
  });

  app.commands.addCommand(command, {
    label: 'Open Welcome Page',
    execute: () => {
      createCommand();
    }
  });

  palette.addItem({ command, category: 'my-category' });
}
