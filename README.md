# graphemes++

A minimalistic grapheme segmentation library for Tamil and Sinhala scripts.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/vmenan/graphemes_plusplus.git
cd graphemes-plusplus
uv sync
```

## Usage

### Segment a string

```python
from graphemes_plusplus import Graphemizer

g = Graphemizer("some text")

g.graphemes       # list of grapheme clusters
len(g)            # number of graphemes
list(g)           # convert to list

for grapheme in g:
    print(grapheme)
```

### Normalize a file

```python
from graphemes_plusplus.utils import normalize_file

normalize_file("input.txt")                        # saves as input_normalized.txt
normalize_file("input.txt", "output.txt")          # custom output path
```
