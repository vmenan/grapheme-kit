# Quick Start

This guide walks you through the core features of `graphemes++` in under 5 minutes.

## 1. Segment Text into Graphemes

The `Graphemizer` class is the primary entry point. It takes a string, normalizes it, and splits it into proper grapheme clusters.

```python
from graphemes_plusplus import Graphemizer

# Tamil text
g = Graphemizer("ஸ்ரீ மதி")
print(g.graphemes)  # ['ஸ்ரீ', ' ', 'ம', 'தி']
print(len(g))       # 4
```

The `Graphemizer` is iterable:

```python
for grapheme in g:
    print(grapheme)
# Output:
# ஸ்ரீ
# (space)
# ம
# தி
```

> **Why not just `list(text)`?**
> In Tamil and Sinhala, a single visual character (grapheme) can consist of multiple Unicode code points. For example, `ஸ்ரீ` is 4 code points but **1 grapheme**. Python's `list()` would split it into 4 separate items, which is linguistically incorrect.
>
>
## 2. Compute Grapheme-Aware Distances

```python
from graphemes_plusplus import levenshtein, hamming

# Levenshtein distance (edit distance)
print(levenshtein("ஸ்ரீ", "ஸ்ரி"))  # 1

# Hamming distance (substitution-only, equal length required)
print(hamming("ஸ்ரீ", "ஸ்ரீ"))     # 0
```

## 3. Decompose and Compose

Break graphemes into phonetic components and reconstruct them:

```python
from graphemes_plusplus import decompose, compose

# Decompose into consonant + vowel components
decomposed = decompose("கா")
print(decomposed)  # க் + ஆ components

# Compose back
original = compose(decomposed)
print(original)    # கா
```

## 4. Evaluate with Metrics

Use grapheme-aware chrF and CER for NLP evaluation:

```python
from graphemes_plusplus.metric import GraphemeCHRF, CER

# chrF score
chrf = GraphemeCHRF()
score = chrf.corpus_score(
    ["வணக்கம் உலகம்"],
    [["வணக்கம் உலகம்"]]
)
print(score)  # 100.0

# Character Error Rate
cer = CER("predicted text", "reference text")
print(cer)
```

---

> **Next Steps**
> - Explore the full [API Reference](../api/graphemizer.md) for detailed documentation
> - Read the [Tamil](../user-guide/tamil.md) or [Sinhala](../user-guide/sinhala.md) specific guides
> - Learn about [Evaluation Metrics](../user-guide/evaluation.md) for NLP tasks
>
