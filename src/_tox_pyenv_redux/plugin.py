from __future__ import annotations

import re
from pathlib import Path

from pyenv_inspect import find_pyenv_python_executable
from tox import hookimpl


_BASEPYTHON_REGEX = re.compile(r'python(?P<version>\d\.\d{1,2})')


@hookimpl
def tox_get_python_executable(envconfig) -> Path | None:
    match = _BASEPYTHON_REGEX.fullmatch(envconfig.basepython)
    if not match:
        return None
    return find_pyenv_python_executable(match.group('version'))
