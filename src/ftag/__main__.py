#!/usr/bin/env python3
from ftag.config import load_config


def main() -> None:
    # Load configuration
    load_config()
    print("This is the main entry point for the ftag package.")


if __name__ == "__main__":
    main()
