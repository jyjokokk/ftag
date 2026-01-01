import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileTag:
    path: Path
    tags: list[str]


class TagRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row

    def add_tag(self, path: Path, tag: str) -> None:
        file_path = path.resolve()

        with self.conn:
            self.conn.execute(
                """--sql
                INSERT OR IGNORE INTO files(path) VALUES (?)""",
                (str(file_path),),
            )

            self.conn.execute(
                """--sql
                INSERT OR IGNORE INTO tags(name) VALUES (?)""",
                (tag,),
            )

            self.conn.execute(
                """--sql
                INSERT OR IGNORE INTO file_tags(file_id, tag_id)
                VALUES (
                    (SELECT id FROM files WHERE path = ?),
                    (SELECT id FROM tags WHERE name = ?)
                )
                """,
                (str(file_path), tag),
            )

    def list_files(self, under: Path | None = None) -> list[FileTag]:
        query = """--sql
        SELECT f.path, GROUP_CONCAT(t.name) AS tags
        FROM files f
        JOIN file_tags ft ON ft.file_id = f.id
        JOIN tags t ON t.id = ft.tag_id
        """
        params: list[str] = []

        if under:
            under = under.resolve()
            query += " WHERE f.path LIKE ?"
            params.append(str(under) + "%")

        query += " GROUP BY f.path ORDER BY f.path"

        rows = self.conn.execute(query, params).fetchall()

        return [
            FileTag(path=Path(row["path"]), tags=row["tags"].split(",")) for row in rows
        ]

    def files_with_tag(self, tag: str) -> list[Path]:
        rows = self.conn.execute(
            """--sql
            SELECT f.path
            FROM files f
            JOIN file_tags ft ON ft.file_id = f.id
            JOIN tags t ON t.id = ft.tag_id
            WHERE t.name = ?
            ORDER BY f.path
            """,
            (tag,),
        ).fetchall()

        return [Path(row["path"]) for row in rows]

    def tags_for_file(self, path: Path) -> list[str]:
        file_path = path.resolve()
        rows = self.conn.execute(
            """--sql
            SELECT t.name
            FROM tags t
            JOIN file_tags ft ON ft.tag_id = t.id
            JOIN files f ON f.id = ft.file_id
            WHERE f.path = ?
            ORDER BY t.name
            """,
            (str(file_path),),
        ).fetchall()

        return [row["name"] for row in rows]

    def remove_tag(self, path: Path, tag: str) -> None:
        file_path = path.resolve()

        with self.conn:
            self.conn.execute(
                """--sql
                DELETE FROM file_tags
                WHERE file_id = (SELECT id FROM files WHERE path = ?)
                  AND tag_id = (SELECT id FROM tags WHERE name = ?)
                """,
                (str(file_path), tag),
            )

    def all_tags(self) -> list[str]:
        rows = self.conn.execute(
            """--sql
            SELECT name FROM TAGS ORDER BY name;
            """
        ).fetchall()
        return [row["name"] for row in rows]
