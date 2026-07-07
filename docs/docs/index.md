# <span class="gk-wordmark">grapheme<span class="gk-kit">Kit</span></span>

Every character-level NLP metric — chrF, CER, edit distance — silently assumes that one Unicode code point is one visually perceived character. That assumption holds for English and most Latin-script languages, so nothing about those metrics needs to change for them. It breaks down for complex scripts like Tamil and Sinhala, where a single visual unit (a **grapheme cluster**) can be built from several code points — and standard metrics end up scoring the wrong thing.

`grapheme-kit` redefines these metrics at the **grapheme** level instead of the code-point level. It doesn't replace chrF, chrF++, or CER — it complements them: the standard metrics give you the code-point-local view, `grapheme-kit` gives you the linguistic-unit view. For scripts where the two coincide, the numbers agree. For scripts where they diverge, `grapheme-kit` is the one that matches what a human actually reads.

For example, standard Python sees the Tamil word "Shri" (`ஸ்ரீ`) as 4 separate code points. Visually, and linguistically, it is a single cluster. `grapheme-kit` treats it as 1 grapheme — and scores it that way everywhere: segmentation, distance, and evaluation metrics alike.

## Key Features

- **Grapheme-Aware Evaluation Metrics**: chrF, chrF++, Character Error Rate (`CER`), and CharBLEU, redefined at the grapheme boundary instead of the code-point boundary — usable on any language, most impactful on complex scripts.
- **Grapheme-Aware Distance**: Levenshtein, Damerau-Levenshtein, Hamming, Jaro, Jaro-Winkler, and Longest Common Subsequence, all computed over grapheme clusters instead of code points.
- **Accurate Segmentation**: resolves multi-code-point visual clusters and conjuncts correctly, including Tamil conjuncts and Sinhala ZWJ sequences.
- **Phonetic Canonicalization**: decompose Tamil/Sinhala graphemes into consonant + vowel and compose them back — the one part of the library that is genuinely script-specific.
- **Two Interfaces**: a Python API and a `gpp` command-line tool, so the same grapheme-aware numbers are available whether you're scripting, exploring in a notebook, or piping text on the command line.

## Quick Example

```python
from graphemes_plusplus.metric import CER

# A speech-recognition system drops one vowel marker from "kanawa".
reference  = "කනවා"
hypothesis = "කනව"

# Code-point CER treats this as a 4-character string with 1 substitution.
# Grapheme CER correctly sees 3 visual units with 1 wrong -- the real error rate.
print(CER(hypothesis, reference))
# Output: 0.3333333333333333
```

## Why grapheme-kit?

The problem isn't Tamil or Sinhala specifically — it's that code points and visually-perceived characters silently diverge for some scripts and not others. A metric defined on code points is only ever *accidentally* correct.

| | Code-point metrics (standard chrF / CER) | `grapheme-kit` |
| --- | --- | --- |
| **English, German, and other scripts where code point = grapheme** | Correct | Identical result — no regression |
| **Tamil, Sinhala, and other scripts where one grapheme spans several code points** | Silently wrong — miscounts the error rate | Correct — scores the visual unit, not the encoding |
| **Segmentation** | Splits on code points | Splits on grapheme clusters (Tamil conjuncts, Sinhala ZWJ) |
| **Phonetic decomposition** | Not applicable | Decompose/compose Tamil & Sinhala graphemes into consonant + vowel |
| **Interfaces** | — | Python API and `gpp` command-line tool |

## Documentation Map

- **[NLP Evaluation](how-to/nlp-evaluation.md)** and **[Measuring Quality](tutorials/metrics.md)**: the grapheme-aware metrics that are the core of this library.
- **[System Architecture](explanation/system-architecture.md)**: how a segmentation request, a metric request, and a distance request all flow through one common grapheme interface.
- **[Installation](getting-started/installation.md)** and **[Quick Start](getting-started/quickstart.md)**: get running in a few minutes.
- **[Tutorials](tutorials/introduction.md)**: a guided walkthrough from the code-point/grapheme distinction through to Tamil/Sinhala-specific segmentation and decomposition.
- **[How-To Guides](how-to/nlp-evaluation.md)**: task-focused recipes, including the [command line](how-to/cli-usage.md).
- **[API Reference](reference/metrics.md)**: complete coverage of every module and class.
- **[Explanation](explanation/evaluation-metrics.md)**: the mathematical and linguistic reasoning behind the metrics and the Tamil/Sinhala script rules.

![Python Version](https://img.shields.io/badge/python-%3E%3D3.14-green)
![License](https://img.shields.io/badge/license-MIT-green)
