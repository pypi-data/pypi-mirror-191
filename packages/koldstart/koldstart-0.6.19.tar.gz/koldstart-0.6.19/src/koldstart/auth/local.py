from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_HOME_DIR = str(Path.home() / ".fal")
_FAL_HOME_DIR = os.getenv("FAL_HOME_DIR", _DEFAULT_HOME_DIR)
_TOKEN_FILE = "auth0_token"


def _check_dir_exist(input_location=None):
    """
    Checks if a specific directory exists, creates if not.
    In case the user didn't set a custom dir, will turn to the default home
    """
    dir = Path(_FAL_HOME_DIR).expanduser()

    if input_location:
        dir = dir / input_location

    if not dir.exists():
        dir.mkdir(parents=True)

    return dir


def _read_refresh_token(path: Path) -> str | None:
    if path.exists():
        return path.read_text()


def _write_refresh_token(path: Path, access_token: str):
    path.write_text(access_token)


def load_token() -> str | None:
    return _read_refresh_token(_check_dir_exist() / _TOKEN_FILE)


def save_token(token: str) -> None:
    return _write_refresh_token(_check_dir_exist() / _TOKEN_FILE, token)


def delete_token() -> None:
    path = _check_dir_exist() / _TOKEN_FILE
    path.unlink()
