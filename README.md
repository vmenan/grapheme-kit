# grapheme-kit

Grapheme-cluster-aware segmentation, string distance, and evaluation metrics for any language.

[![PyPI](https://img.shields.io/pypi/v/grapheme-kit)](https://pypi.org/project/grapheme-kit/)
[![Python](https://img.shields.io/pypi/pyversions/grapheme-kit)](https://pypi.org/project/grapheme-kit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**[Live Demo](https://grapheme-kit.pages.dev) · [Documentation](https://grapheme-kit-docs.pages.dev)**

---

## Why grapheme-kit?

Unicode text is complex: a single *visible* character (grapheme cluster) often spans multiple code points. Naive string operations get lengths, distances, and evaluation metrics wrong when combining marks, diacritics, or conjuncts are present.

`grapheme-kit` operates at the grapheme-cluster level, ensuring all measurements reflect human-perceived text structure, not raw byte or code point counts.

```python
from grapheme_kit import Graphemizer

# Burmese
g = Graphemizer("ကျွန်ုပ်")
len("ကျွန်ုပ်")     # 8 code points (naive)
len(g)           # 3 grapheme clusters (correct)

# Bengali
g = Graphemizer("নমস্কার")
len("নমস্কার")    # 5 code points (naive)
len(g)           # 7 grapheme clusters (correct)
```

---

## Installation

```bash
pip install grapheme-kit
```

```bash
# development
git clone https://github.com/vmenan/grapheme-kit.git
cd grapheme-kit
uv sync
```

---

## Features

### Segmentation
Split text from any script into correct grapheme clusters:
```python
from grapheme_kit import Graphemizer

g = Graphemizer("किताब")
g.graphemes   # ['कि', 'ता', 'ब']
len(g)        # 3

# Burmese
g = Graphemizer("ကျွန်ုပ်")
g.graphemes   # ['ကျွ', 'န်ု', 'ပ်']
len(g)        # 3
```

### String Distance
Grapheme-aware implementations of popular distance and similarity algorithms:
```python
from grapheme_kit import levenshtein
from grapheme_kit.distance import jaro_winkler, damerau_levenshtein

# Hebrew
levenshtein("שָׁלוֹם", "שָׁלוֹב")          # 1 (only one cluster differs)

# Arabic 
levenshtein("مُعَلِّمٌ", "مُعَلِّمُ")          # 1 (diacritic-level edit, one grapheme)

# Hindi
levenshtein("किताब", "कताब")          # 1 (one grapheme cluster removed)

# Latin/English
levenshtein("kitten", "sitting")       # 3
jaro_winkler("martha", "marhta")       # 0.9611
```

### Evaluation Metrics
Compute machine translation or text generation metrics based on grapheme clusters rather than character code points:
```python
from grapheme_kit.metric import GraphemeCHRF, CER, charbleu

# chrF
GraphemeCHRF().sentence_score("நல்ல", ["நல்ல மாணவன்"]).score  # 37.1051

# Character Error Rate (CER)
CER("كِتَابٌ", "كِتَابَ")  # 0.25

# CharBLEU
charbleu("the quick brown fox", "the quick red fox")  # 0.7086
```

### Decompose / Compose
Phonetic decomposition and composition (currently supported for select Indic scripts like Tamil and Sinhala):
```python
from grapheme_kit import decompose, compose

decompose("කා")                   # 'ක්ආ'
compose("ක්ආ")                    # 'කා'
compose(decompose("வணக்கம்")) == "வணக்கம்"  # True
```

---

## Command Line

The package exposes a `grapheme-kit` executable with a short alias `gkit`:

```bash
gkit graphemize "مَرْحَبًا" --count
gkit graphemize "किताब" --count
gkit distance "שָׁלוֹם" "שָׁלוֹב" --level both
gkit evaluate "நல்ல மாணவன்" "நல்ல" --metric chrf
gkit decompose "ලංකාව" --round-trip
```

Use `gkit --help` or `gkit <command> --help` for the full list of commands and options.

---

## Documentation

Full documentation, guides, and API reference: [grapheme-kit-docs.pages.dev](https://grapheme-kit-docs.pages.dev)

Try it interactively in the [live demo](https://grapheme-kit.pages.dev/graphemizer/).

---

## Contributing

Issues and pull requests are welcome. Please open an issue first for major changes.

## License

MIT © grapheme-kit contributors. See [LICENSE](LICENSE) for details.
