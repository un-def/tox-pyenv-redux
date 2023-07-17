# tox-pyenv-redux

A [tox][tox] Python discovery plugin for [pyenv][pyenv]–installed interpreters

**IMPORTANT**: this plugin is only compatible with legacy versions of tox (0.x—3.x). Starting with tox version 4, the Python discovery job is delegated to [virtualenv][virtualenv] ([docs][tox-docs-discovery-migration]).

## Migration to tox 4

1. Uninstall tox-pyenv-redux
2. Install [virtualenv-pyenv][virtualenv-pyenv]
3. Set the virtualenv discovery mechanism to `pyenv` using one of the following methods:
    * the environment variable in a shell (e.g., in `.bashrc`, `.zshenv`, `.envrc`, `.env`):
      ```shell
      export VIRTUALENV_DISCOVERY=pyenv
      ```
    * the environment variable in [a tox config][tox-docs-config]:
      ```ini
      [testenv]
      set_env =
        VIRTUALENV_DISCOVERY = pyenv
      ```
    * the option in [a virtualenv config][virtualenv-docs-config]:
      ```ini
      [virtualenv]
      discovery = pyenv
      ```


[tox]: https://tox.wiki/
[pyenv]: https://github.com/pyenv/pyenv
[virtualenv]: https://virtualenv.pypa.io/
[virtualenv-pyenv]: https://github.com/un-def/virtualenv-pyenv
[tox-docs-discovery-migration]: https://tox.wiki/en/latest/plugins.html#tox-get-python-executable
[tox-docs-config]: https://tox.wiki/en/latest/config.html
[virtualenv-docs-config]: https://virtualenv.pypa.io/en/latest/cli_interface.html#conf-file
