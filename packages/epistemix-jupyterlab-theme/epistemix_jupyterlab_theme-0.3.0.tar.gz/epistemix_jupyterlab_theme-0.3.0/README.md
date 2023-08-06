# epistemix_jupyterlab_theme

Epistemix theme for JupyterLab.

## Requirements

- JupyterLab >= 3.0

## Install

To install the extension from PyPI, execute:

```bash
pip install epistemix-jupyterlab-theme
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall epistemix-jupyterlab-theme
```

## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

First install [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or some kind of package/environment manager.

Then create an environment for jupyterlab and activate that environment.

```bash
# Create environment
conda create -n jupyterlab-ext --override-channels --strict-channel-priority -c conda-forge -c nodefaults jupyterlab=3 nodejs jupyter-packaging git
```

```bash
# Activate environment
conda activate jupyterlab-ext
```

Note: You’ll need to run the command above in each new terminal you open before you can work with the tools you installed in the jupyterlab-ext environment.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the epistemix_jupyterlab_theme directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development install in a Docker container

See the README in the `docker_dev_environment` folder.

### Development uninstall

```bash
pip uninstall epistemix_jupyterlab_theme
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `epistemix_jupyterlab_theme` within that folder.

### Packaging the extension

See [RELEASE](RELEASE.md)
