from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import TypedDict, cast

DEFAULT_CONFIG: Config = {
    "ftag_dir": str(Path.home() / ".ftag"),
    "db_path": str(Path.home() / ".ftag" / "ftag.sqlite3."),
    "verbose": False,
    "debug": False,
}


class Config(TypedDict):
    ftag_dir: str
    db_path: str
    verbose: bool
    debug: bool


CONFIG_PATH = Path.home() / ".config" / "ftag" / "config.toml"


def _load_config_from_file() -> dict:
    if not CONFIG_PATH.exists():
        return {}

    with CONFIG_PATH.open("rb") as f:
        return tomllib.load(f)


def _apply_env_overrides(cfg: Config) -> None:
    if "FTAG_DB_PATH" in os.environ:
        cfg["db_path"] = os.environ["FTAG_DB_PATH"]

    if "FTAG_VERBOSE" in os.environ:
        cfg["verbose"] = os.environ["FTAG_VERBOSE"].lower() == "true"

    if "FTAG_DEBUG" in os.environ:
        cfg["debug"] = os.environ["FTAG_DEBUG"].lower() == "true"


def load_config() -> Config:
    cfg = DEFAULT_CONFIG.copy()

    cfg.update(cast(Config, _load_config_from_file()))
    _apply_env_overrides(cfg)

    return cfg
