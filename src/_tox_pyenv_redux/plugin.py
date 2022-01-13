from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from pyenv_inspect.path import (
    get_pyenv_python_bin_path, get_pyenv_versions_directory,
)
from pyenv_inspect.version import Version
from tox import hookimpl


_BASEPYTHON_REGEX = re.compile(r'python(?P<version>\d\.\d{1,2})')


@hookimpl
def tox_get_python_executable(envconfig):
    match = _BASEPYTHON_REGEX.fullmatch(envconfig.basepython)
    if not match:
        return
    requested_version = Version.from_string_version(match.group('version'))
    best_match_version: Optional[Version] = None
    best_match_dir: Optional[Path] = None
    for version_dir in get_pyenv_versions_directory().iterdir():
        version = Version.from_string_version(version_dir.name)
        if version is None:
            continue
        if version in requested_version:
            if not best_match_version or version > best_match_version:
                best_match_version = version
                best_match_dir = version_dir
    if not best_match_version:
        return None
    return get_pyenv_python_bin_path(best_match_dir)
