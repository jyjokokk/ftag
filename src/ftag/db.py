import sqlite3
from pathlib import Path

from ftag.config import load_config

SCHEMA = """--sql
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    inode INTEGER,
    device INTEGER
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE

);

CREATE TABLE IF NOT EXISTS file_tags (
    file_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (file_id, tag_id),
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
"""


def get_connection() -> sqlite3.Connection:
    cfg = load_config()
    DB_PATH = Path(cfg.get("db_path"))
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # Add this line
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn
