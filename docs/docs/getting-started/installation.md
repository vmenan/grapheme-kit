# Installation

## Prerequisites

- **Python**: Version 3.14 or newer.
- **uv**: We recommend using the `uv` package manager for fast and reliable dependency resolution. (See [uv documentation](https://docs.astral.sh/uv/)).

## Install from Source

Currently, the recommended way to install `grapheme-kit` is by cloning the repository and syncing dependencies via `uv`. This will set up the library and install both the `graphemes-plusplus` and `gpp` command line executables.

```bash
git clone https://github.com/vmenan/graphemes_plusplus.git
cd graphemes_plusplus
uv sync
```

## Verify Installation

Open a Python shell and try importing the library:

```python
from graphemes_plusplus import Graphemizer

g = Graphemizer("வணக்கம்")
print(g.graphemes)
# Output: ['வ', 'ண', 'க்', 'க', 'ம்']
```

If you see the output above without any errors, the installation was successful.

### Verify the CLI

You can also verify that the command-line interface was successfully installed and is available in your environment:

```bash
gpp --help
```

Or using the long alias:

```bash
graphemes-plusplus --help
```

Both commands should print the help text detailing the available subcommands and options.

## Dependencies

When you run `uv sync`, the following core dependencies are automatically installed:

- `grapheme` (≥0.6.0): Used as the base Unicode grapheme cluster foundation.
- `textdistance` (≥4.6.3): Used to compute Levenshtein and Hamming distances.
- `sacrebleu` (≥2.6.0): The base library extended for `GraphemeCHRF`.
