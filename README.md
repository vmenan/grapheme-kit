# graphemes++

A minimalistic grapheme segmentation library for Tamil and Sinhala scripts.

## Installation

Install from PyPI:

```bash
pip install graphemes-plusplus
```

For development, clone the repository and install with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/vmenan/graphemes_plusplus.git
cd graphemes_plusplus
uv sync
```

## Usage

### Segment a string

```python
>>> from graphemes_plusplus import Graphemizer
>>> g = Graphemizer("ஸ்ரீ மதி")
>>> g.graphemes
['ஸ்ரீ', ' ', 'ம', 'தி']
>>> len(g)
4
>>> for grapheme in g:
...     print(grapheme)
ஸ்ரீ

ம
தி
```

### Compute distance

```python
>>> from graphemes_plusplus import levenshtein, hamming
>>> levenshtein("ஸ்ரீ", "ஸ்ரி")
1
>>> hamming("ஸ்ரீ", "ஸ்ரீ")
0
```

### Normalize a file

```python
>>> from graphemes_plusplus.utils import normalize_file
>>> normalize_file("input.txt")
'input_normalized.txt'
>>> normalize_file("input.txt", "output.txt")
'output.txt'
```

### Command line

Installing the package also provides the `graphemes-plusplus` command (short alias `gpp`):

```bash
gpp graphemize "ஸ்ரீ வணக்கம்" --count        # Tamil
gpp graphemize "ශ්‍රී ලංකාව" --count          # Sinhala
gpp distance "ஸ்ரீ" "ஸ்ரி" --level both
gpp evaluate "நல்ல மாணவன்" "நல்ல" --metric chrf
echo "ශ්‍රී" | gpp decompose --round-trip      # stdin works too
```

Use `gpp --help` (or `gpp <command> --help`) for the full list of commands and options.
