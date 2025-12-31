# ftag

A command-line tool for tagging files with custom labels.

## Overview

**ftag** lets you organize your files with custom tags without modifying the files themselves. Tags are stored in a local SQLite database, making it easy to find and filter files across your filesystem.

## Features

- **Tag files**: Add custom tags to any file
- **List tagged files**: View all tagged files in the current directory
- **Filter by tag**: Find all files with a specific tag
- **Persistent storage**: Tags are stored in `~/.ftag/` using SQLite
- **Path repair**: Automatically tracks files even if they move (inode-based)

## Installation

```bash
pip install -e .
```

## Usage

### Add a tag to a file

```bash
ftag add some-tag-name some/dir/some-file.txt
```

### List all tagged files in the current directory

```bash
ftag ls
```

### Filter files by tag

```bash
ftag find some-tag-name
```

## Development

Run tests:

```bash
pytest tests/
```

Run in development mode:

```bash
python -m ftag
```

## Future Plans

- macOS and Linux releases
- Ranger file manager integration
- Tag removal and management commands
- Export/import tag collections
- Search across multiple directories

## License

See [LICENSE](LICENSE) for details.
