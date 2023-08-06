import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { MainAreaWidget, ICommandPalette } from '@jupyterlab/apputils';

import { ILauncher } from '@jupyterlab/launcher';

import { reactIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';

import { DatalayerWidget } from './widget';

import '../style/index.css';

/**
 * The command IDs used by the react-widget plugin.
 */
namespace CommandIDs {
  export const create = 'create-jupyter-manager-widget';
}

/**
 * Initialization data for the @datalayer/jupyter-manager extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@datalayer/jupyter-manager:plugin',
  autoStart: true,
  requires: [ICommandPalette],
  optional: [ISettingRegistry, ILauncher],
  activate: (
    app: JupyterFrontEnd,
    palette: ICommandPalette,
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher
  ) => {
    const { commands } = app;
    const command = CommandIDs.create;
    commands.addCommand(command, {
      caption: 'Show Jupyter Manager',
      label: 'Jupyter Manager',
      icon: (args: any) => reactIcon,
      execute: () => {
        const content = new DatalayerWidget();
        const widget = new MainAreaWidget<DatalayerWidget>({ content });
        widget.title.label = 'Jupyter Manager';
        widget.title.icon = reactIcon;
        app.shell.add(widget, 'main');
      }
    });
    const category = 'Jupyter Manager';
    palette.addItem({ command, category, args: { origin: 'from palette' } });
    if (launcher) {
      launcher.add({
        command
      });
    }
    console.log('JupyterLab extension @datalayer/jupyter-manager is activated!');
    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('@datalayer/jupyter-manager settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for @datalayer/jupyter-manager.', reason);
        });
    }
    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The datalayer server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
