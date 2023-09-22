from __future__ import annotations

import subprocess
from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    import pathlib


@pytest.fixture
def config_path(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / 'tox.ini'


_BASE_CONFIG = """
    [tox]
    no_package = true

    [testenv]
    skip_install = true
    commands =
        python -c 'import os; print(os.environ.get("VIRTUALENV_DISCOVERY"))'
"""


def _write_config(
    config_path: pathlib.Path, *, pyenv_discovery: str | None = None,
) -> None:
    config_chunks = [_BASE_CONFIG]
    if pyenv_discovery is not None:
        config_chunks.append(f'pyenv_discovery = {pyenv_discovery}')
    config_path.write_text('\n'.join(config_chunks))


def _run_tox(config_path: pathlib.Path, *, fail: bool = False) -> str:
    process = subprocess.run(
        ['python', '-m', 'tox', '-c', config_path, '-qq', 'run'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if fail:
        assert process.returncode != 0
    else:
        assert process.returncode == 0
    return process.stdout.strip()


def test_implicit_default_mode(config_path):
    _write_config(config_path)

    output = _run_tox(config_path)

    assert output == 'pyenv'


def test_explicit_default_mode(config_path):
    _write_config(config_path, pyenv_discovery='default')

    output = _run_tox(config_path)

    assert output == 'pyenv'


@pytest.mark.parametrize('mode', ['fallback', 'compat'])
def test_modes(config_path, mode):
    _write_config(config_path, pyenv_discovery=mode)

    output = _run_tox(config_path)

    assert output == f'pyenv-{mode}'


def test_off_with_env_var(monkeypatch, config_path):
    monkeypatch.setenv('VIRTUALENV_DISCOVERY', 'builtin')
    _write_config(config_path, pyenv_discovery='off')

    output = _run_tox(config_path)

    assert output == 'builtin'


def test_off_without_env_var(monkeypatch, config_path):
    monkeypatch.delenv('VIRTUALENV_DISCOVERY', raising=False)
    _write_config(config_path, pyenv_discovery='off')

    output = _run_tox(config_path)

    assert output == 'None'


def test_unknown_mode(config_path):
    _write_config(config_path, pyenv_discovery='unknown-mode')

    output = _run_tox(config_path, fail=True)

    assert 'pyenv_discovery: unexpected value: unknown-mode' in output


def test_get_pyenv_discovery_modes():
    from _tox_pyenv_redux.plugin import _get_pyenv_discovery_modes

    modes = _get_pyenv_discovery_modes()

    # virtualenv-pyenv version 0.4.0 modes
    assert sorted(modes) == ['compat', 'fallback', 'strict']
