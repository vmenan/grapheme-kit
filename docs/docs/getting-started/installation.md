# Installation

## Requirements

- **Python** ≥ 3.14
- **pip** or **uv** package manager

## Install from Source

Currently, `graphemes++` is installed from source via Git clone:

**Using uv (recommended)**

```bash
git clone https://github.com/vmenan/graphemes_plusplus.git
cd graphemes_plusplus
uv sync
```


**Using pip**

```bash
git clone https://github.com/vmenan/graphemes_plusplus.git
cd graphemes_plusplus
pip install -e .
```


## Dependencies

`graphemes++` depends on the following packages (installed automatically):

| Package | Version | Purpose |
|---|---|---|
| `grapheme` | ≥ 0.6.0 | Base Unicode grapheme clustering |
| `textdistance` | ≥ 4.6.3 | Levenshtein & Hamming distance algorithms |
| `sacrebleu` | ≥ 2.0.0 | chrF/chrF++ metric base class |

## Verify Installation

After installation, verify everything works:

```python
>>> from graphemes_plusplus import Graphemizer
>>> g = Graphemizer("வணக்கம்")
>>> g.graphemes
['வ', 'ண', 'க்', 'க', 'ம்']
```

> **Ready to go!**
> If you see the grapheme list output without errors, the installation is complete. Head to the [Quick Start](quickstart.md) guide next.
>
