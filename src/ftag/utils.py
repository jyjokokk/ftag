from pathlib import Path


def display_path(path: Path, cwd: Path, abs_: bool) -> str:
    if abs_:
        return str(path)
    try:
        return str(path.relative_to(cwd))
    except ValueError:
        return str(path)
