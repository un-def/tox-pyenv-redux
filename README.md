# tox-pyenv-redux

A [tox][tox] Python discovery plugin for [pyenv][pyenv]–installed interpreters

## Compatibility

* For legacy versions of tox (0.x—3.x), use tox-pyenv-redux 0.x (`tox-pyenv-redux < 1`). These versions do not rely on [virtualenv-pyenv][virtualenv-pyenv] and **DO NOT** support the `pyenv_discovery` setting.
* For the current version of tox (4.x), use tox-pyenv-redux 1.x (`tox-pyenv-redux >= 1, < 2`). These versions delegate the discovery job to [virtualenv-pyenv][virtualenv-pyenv].

## Installation

```shell
pip install tox-pyenv-redux
```

## Usage

The plugin is enabled by default and configured to use the default discovery [operation mode][virtualenv-pyenv-docs-operation-mode]. To change the mode or disable the plugin, set the `pyenv_discovery` environment setting to one of the following values:

* One of the [operation modes][virtualenv-pyenv-docs-operation-mode] (e.g., `fallback`) to use the specific operation mode. `pyenv_discovery = fallback` is equivalent to `export VIRTUALENV_DISCOVERY=pyenv-fallback`.
* `default` to use the default operation mode. This is the default value. `pyenv_discovery = default` (or no setting) is equivalent to `export VIRTUALENV_DISCOVERY=pyenv`.
* `off` to disable the plugin. The plugin will not touch the `VIRTUALENV_DISCOVERY` environment variable, but the [virtualenv-pyenv][virtualenv-pyenv] discovery can still be in effect if virtualenv is already configured to use it (via the `VIRTUALENV_DISCOVERY` environment variable or the `discovery` config setting).

## Examples

* Set the `fallback` operation mode via a config file:

  ```ini
  [tox]
  min_version = 4.0
  requires = tox-pyenv-redux

  [testenv]
  pyenv_discovery = fallback
  deps = pytest
  commands = pytest {posargs}
  ```

* Disable the plugin via command line arguments:

  ```shell
  tox run -x testenv.pyenv_discovery=off
  ```


[tox]: https://tox.wiki/
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv-pyenv]: https://github.com/un-def/virtualenv-pyenv
[virtualenv-pyenv-docs-operation-mode]: https://github.com/un-def/virtualenv-pyenv/blob/master/README.md#operation-mode
