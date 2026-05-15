# Installation

## Prerequisites

- **Python**: Version 3.14 or newer.
- **uv**: We recommend using the `uv` package manager for fast and reliable dependency resolution. (See [uv documentation](https://docs.astral.sh/uv/)).

## Install from Source

Currently, the recommended way to install `graphemes++` is by cloning the repository and syncing dependencies via `uv`.

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

## Dependencies

When you run `uv sync`, the following core dependencies are automatically installed:

- `grapheme` (≥0.6.0): Used as the base Unicode grapheme cluster foundation.
- `textdistance` (≥4.6.3): Used to compute Levenshtein and Hamming distances.
- `sacrebleu` (≥2.6.0): The base library extended for `GraphemeCHRF`.
