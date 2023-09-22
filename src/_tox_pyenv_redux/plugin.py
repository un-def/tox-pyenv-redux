from __future__ import annotations

import sys
from importlib.metadata import distribution
from typing import TYPE_CHECKING

from tox.plugin import impl


if TYPE_CHECKING:
    from importlib.metadata import EntryPoint

    from tox.config.sets import EnvConfigSet


_DISCOVERY_ENV_VAR = 'VIRTUALENV_DISCOVERY'
_DISCOVERY_ENTRYPOINT_GROUP = 'virtualenv.discovery'
_PYENV_DISCOVERY_DISTRIBUTION = 'virtualenv-pyenv'
_PYENV_DISCOVERY_DEFAULT_ENTRYPOINT = 'pyenv'
_PYENV_DISCOVERY_ENTRYPOINT_PREFIX = 'pyenv-'

_PYENV_DISCOVERY_SETTING = 'pyenv_discovery'
_PYENV_DISCOVERY_OPTION_DEFAULT = 'default'
_PYENV_DISCOVERY_OPTION_OFF = 'off'


def _get_pyenv_discovery_entrypoints() -> list[EntryPoint]:
    dist = distribution(_PYENV_DISCOVERY_DISTRIBUTION)
    if sys.version_info < (3, 10):
        return [
            entrypoint for entrypoint in dist.entry_points
            if entrypoint.group == _DISCOVERY_ENTRYPOINT_GROUP
        ]
    return dist.entry_points.select(group=_DISCOVERY_ENTRYPOINT_GROUP)


def _get_pyenv_discovery_modes() -> list[str]:
    _prefix_len = len(_PYENV_DISCOVERY_ENTRYPOINT_PREFIX)
    pyenv_discovery_modes = [
        mode for entrypoint in _get_pyenv_discovery_entrypoints()
        if (mode := entrypoint.name[_prefix_len:])
    ]
    return pyenv_discovery_modes


@impl
def tox_add_env_config(env_conf: EnvConfigSet) -> None:
    env_conf.add_config(
        _PYENV_DISCOVERY_SETTING,
        of_type=str,
        default=_PYENV_DISCOVERY_OPTION_DEFAULT,
        desc='virtualenv-pyenv discovery',
    )
    value = env_conf[_PYENV_DISCOVERY_SETTING]
    discovery: str | None
    if value == _PYENV_DISCOVERY_OPTION_OFF:
        discovery = None
    elif value == _PYENV_DISCOVERY_OPTION_DEFAULT:
        discovery = _PYENV_DISCOVERY_DEFAULT_ENTRYPOINT
    elif value in _get_pyenv_discovery_modes():
        discovery = f'{_PYENV_DISCOVERY_ENTRYPOINT_PREFIX}{value}'
    else:
        raise ValueError(
            f'{_PYENV_DISCOVERY_SETTING}: unexpected value: {value}')
    if discovery is not None:
        env_conf['set_env'].update({_DISCOVERY_ENV_VAR: discovery})
