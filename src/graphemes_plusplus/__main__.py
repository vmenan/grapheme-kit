"""Enable ``python -m graphemes_plusplus ...`` alongside the installed command."""

from graphemes_plusplus.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
