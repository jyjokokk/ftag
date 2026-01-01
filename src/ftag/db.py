import os
import sqlite3
from pathlib import Path

FTAG_DIR = Path(os.getenv("FTAG_DIR", Path(__file__).parent.parent))
DB_PATH = Path(FTAG_DIR / "ftag.db")

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


def get_all_tags(conn: sqlite3.Connection) -> list[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM tags ORDER BY name")
    rows = cursor.fetchall()
    return [row[0] for row in rows]


def get_connection() -> sqlite3.Connection:
    FTAG_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    return conn


a = [2, 3, 4]

b = [print(i) for i in a]
