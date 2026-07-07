"""Enable ``python -m grapheme_kit ...`` alongside the installed command."""

from grapheme_kit.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
