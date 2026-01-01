#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys

from ftag.db import get_connection
from ftag.models import TagRepository
from ftag.utils import display_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser("ftag")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add", aliases=["a"])
    add.add_argument("tag")
    add.add_argument("files", nargs="+")

    ls = sub.add_parser("ls", aliases=["l"])
    ls.add_argument("-a", "--all", action="store_true")
    ls.add_argument("--abs", action="store_true")
    ls.add_argument("--tag")

    find = sub.add_parser("find", aliases=["f"])
    find.add_argument("tag")

    tags = sub.add_parser("tags", aliases=["t"])
    tags.add_argument("file", nargs="?")

    rm = sub.add_parser("rm")
    rm.add_argument("tag")
    rm.add_argument("files", nargs="+")

    return parser


def cmd_add(repo: TagRepository, tag: str, files: list[str]) -> None:
    for f in files:
        path = Path(f)
        if not path.exists():
            print(f"ftag: file not found {f}", file=sys.stderr)
            continue

        repo.add_tag(path, tag)


def cmd_ls(repo: TagRepository, all_: bool, abs_: bool, tag: str | None) -> None:
    cwd = Path.cwd()

    if tag:
        paths = repo.files_with_tag(tag)
        for p in paths:
            print(display_path(p, cwd, abs_))
        return

    under = None if all_ else cwd
    entries = repo.list_files(under=under)

    for entry in entries:
        path_str = display_path(entry.path, cwd, abs_)
        tags_str = ", ".join(entry.tags)
        print(f"{path_str}: {tags_str}")


def cmd_find(repo: TagRepository, tag: str) -> None:
    for path in repo.files_with_tag(tag):
        print(path)


def cmd_tags(repo: TagRepository, file: str | None) -> None:
    if file:
        path = Path(file)
        tags = repo.tags_for_file(path)
    else:
        tags = repo.all_tags()

    for tag in sorted(tags):
        print(tag)


def cmd_rm(repo: TagRepository, tag: str, files: list[str]) -> None:
    for f in files:
        path = Path(f)
        if not path.exists():
            continue
        repo.remove_tag(path, tag)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    conn = get_connection()
    repo = TagRepository(conn)

    match args.cmd:
        case "add" | "a":
            cmd_add(repo, args.tag, args.files)
        case "ls":
            cmd_ls(repo, args.all, args.abs, args.tag)
        case "find" | "f":
            cmd_find(repo, args.tag)
        case "tags" | "t":
            cmd_tags(repo, args.file)
        case "rm":
            cmd_rm(repo, args.tag, args.files)
