# cli.py
from ftag.config import load_config


def main() -> None:
    cfg = load_config()
    print(cfg)
    print("This is the CLI entry point for the ftag package.")


if __name__ == "__main__":
    main()
