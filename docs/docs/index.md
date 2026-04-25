# graphemes++

A Python library for accurate grapheme-level segmentation and processing, designed specifically for Indic scripts like Tamil and Sinhala.

Standard string processing libraries operate on Unicode code points. However, Indic scripts use complex sequences of code points such as consonant-vowel combinations and zero-width joiners to render a single visual grapheme. `graphemes++` parses these visual clusters accurately.

## Key Features

- **Accurate Segmentation**: Resolves multi-byte visual clusters and conjuncts effectively.
- **Language Aware**: Contains specialized logic for Tamil (e.g., `க்ஷ`, `ஸ்ரீ`) and Sinhala (ZWJ sequences).
- **Phonetic Transliteration**: Decompose graphemes into phonetic bases and vowels, and compose them back.
- **Robust Metrics**: Includes `GraphemeCHRF` and Character Error Rate (`CER`) scaled properly to grapheme boundaries rather than code points, leading to more accurate NLP evaluation.
- **Distance Algorithms**: Computes true grapheme-aware Levenshtein and Hamming distances.

## Quick Example

```python
from graphemes_plusplus import Graphemizer

text = "ஸ்ரீ மதி"
g = Graphemizer(text)

print(g.graphemes)
# Output: ['ஸ்ரீ', ' ', 'ம', 'தி']

print(len(g))
# Output: 4
```

## Documentation Map

- **[Installation](getting-started/installation.md)**: Details on installing the package via `pip` or `uv`.
- **[Quick Start](getting-started/quickstart.md)**: A brief overview to get started with core components.
- **[User Guide](user-guide/tamil.md)**: Best practices for Tamil and Sinhala text.
- **[API Reference](api/graphemizer.md)**: Complete coverage of all available modules and classes.
