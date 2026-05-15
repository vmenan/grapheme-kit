# graphemes++

Standard string processing libraries operate on Unicode code points. However, Indic scripts use complex sequences of code points such as consonant-vowel combinations and zero-width joiners to render a single visual grapheme. `graphemes++` parses these visual clusters accurately, ensuring that NLP tasks match human intuition.

For example, standard Python sees the word "Shri" in Tamil as 4 separate code points. Visually, it is a single cluster. `graphemes++` understands this and accurately treats it as 1 grapheme.

## Key Features

- **Accurate Segmentation**: Resolves multi-byte visual clusters and conjuncts effectively.
- **Language Aware**: Contains specialized logic for Tamil conjuncts and Sinhala ZWJ sequences.
- **Phonetic Transliteration**: Decompose graphemes into phonetic bases and vowels, and compose them back.
- **Distance Algorithms**: Computes true grapheme-aware Levenshtein and Hamming distances.
- **Robust Metrics**: Includes `GraphemeCHRF` and Character Error Rate (`CER`) scaled properly to grapheme boundaries rather than code points, leading to more accurate NLP evaluation.

## Quick Example

```python
from graphemes_plusplus import Graphemizer

# "vanakkam" (hello) in Tamil
g = Graphemizer("வணக்கம்")

print(g.graphemes)
# Output: ['வ', 'ண', 'க்', 'க', 'ம்']

print(len(g))
# Output: 5
```

## Why graphemes++?

| Feature | Python Built-in | `grapheme` Library | `graphemes++` |
| --- | --- | --- | --- |
| **Basic Unicode parsing** | Yes | Yes | Yes |
| **Tamil conjuncts (e.g. Ksha, Shri)** | No (splits into parts) | No (splits into parts) | Yes (merged correctly) |
| **Sinhala ZWJ sequences** | No | No | Yes |
| **Indic phonetic decomposition** | No | No | Yes |
| **Grapheme-aware NLP metrics** | No (uses code points) | No | Yes (GraphemeCHRF, CER) |

## Documentation Map

- **[Installation](getting-started/installation.md)**: Prerequisites and how to install.
- **[Quick Start](getting-started/quickstart.md)**: Jump right into the code with a brief overview of core components.
- **[Tutorials](tutorials/introduction.md)**: A beginner guide to understanding and processing Indic texts.
- **[How-To Guides](how-to/grapheme-segmentation.md)**: Recipes and patterns for common segmentation and evaluation tasks.
- **[API Reference](reference/graphemizer.md)**: Complete coverage of all available modules and classes.
- **[Explanation](explanation/tamil-script-rules.md)**: Theoretical insights into the script rules and NLP metrics.

![Python Version](https://img.shields.io/badge/python-%3E%3D3.14-green)
![License](https://img.shields.io/badge/license-MIT-green)
