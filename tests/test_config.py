from pathlib import Path

from ftag.config import load_config


def test_load_config_returns_defaults_when_no_file() -> None:
    cfg = load_config()
    assert cfg["ftag_dir"] == str(Path.home() / ".ftag")
    assert cfg["db_path"] == str(Path.home() / ".ftag" / "ftag.sqlite3.")
    assert cfg["verbose"] is False
    assert cfg["debug"] is False


def test_load_config_with_env_override_db_path(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_DB_PATH", "/custom/path/db.sqlite3")
    cfg = load_config()
    assert cfg["db_path"] == "/custom/path/db.sqlite3"


def test_load_config_with_env_override_verbose_true(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_VERBOSE", "true")
    cfg = load_config()
    assert cfg["verbose"] is True


def test_load_config_with_env_override_verbose_false(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_VERBOSE", "false")
    cfg = load_config()
    assert cfg["verbose"] is False


def test_load_config_with_env_override_debug_true(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_DEBUG", "true")
    cfg = load_config()
    assert cfg["debug"] is True


def test_load_config_with_env_override_debug_false(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_DEBUG", "false")
    cfg = load_config()
    assert cfg["debug"] is False


def test_load_config_with_multiple_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("FTAG_DB_PATH", "/custom/db.sqlite3")
    monkeypatch.setenv("FTAG_VERBOSE", "true")
    monkeypatch.setenv("FTAG_DEBUG", "true")
    cfg = load_config()
    assert cfg["db_path"] == "/custom/db.sqlite3"
    assert cfg["verbose"] is True
    assert cfg["debug"] is True


def test_load_config_from_file(tmp_path, monkeypatch) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_text('ftag_dir = "/custom/ftag"\nverbose = true\n')
    monkeypatch.setattr("ftag.config.CONFIG_PATH", config_file)
    cfg = load_config()
    assert cfg["ftag_dir"] == "/custom/ftag"
    assert cfg["verbose"] is True


def test_env_overrides_file_config(tmp_path, monkeypatch) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_text("verbose = false\n")
    monkeypatch.setattr("ftag.config.CONFIG_PATH", config_file)
    monkeypatch.setenv("FTAG_VERBOSE", "true")
    cfg = load_config()
    assert cfg["verbose"] is True
    assert cfg["verbose"] is True
