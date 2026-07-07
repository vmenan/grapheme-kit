# Conjuncts and ZWJ Sequences

This section explains the two most important special grapheme patterns in Tamil and Sinhala: conjuncts and Zero-Width Joiner sequences.

## Tamil Conjuncts

Some sequences of characters merge visually to form a completely new shape, known as a **conjunct**. Standard Unicode grapheme splitting does not know about these language-specific merges.

A common Tamil conjunct is `க்ஷ` (Ksha). It is composed of two separate clusters `க்` and `ஷ`, but visually it renders as one inseparable unit.

```python
from grapheme_kit import Graphemizer

# Without grapheme-kit, this would split into ['க்', 'ஷ', ...]
g = Graphemizer("க்ஷத்ரியன்")

print(g.graphemes)
# Output: ['க்ஷ', 'த்', 'ரி', 'ய', 'ன்']
```

The library uses a look-ahead rule: if the current cluster is `க்` and the next cluster starts with `ஷ`, they are merged into a single grapheme.

## The Shri Cluster

Another important conjunct is the honorific "Shri" in Tamil, which can be written as `ஸ்ரீ` or `ஶ்ரீ`. These consist of two separate Unicode clusters but visually render as one symbol.

```python
from grapheme_kit import Graphemizer

print(Graphemizer("ஸ்ரீ").graphemes)
# Output: ['ஸ்ரீ']   — correctly kept as 1 grapheme

print(Graphemizer("ஸ்ரி").graphemes)
# Output: ['ஸ்', 'ரி']  — correctly split into 2 graphemes
```

## Sinhala ZWJ Sequences

Sinhala script makes extensive use of the **Zero-Width Joiner** (ZWJ, `U+200D`). It is an invisible character used to force two adjacent characters to merge into a conjunct.

For example, `ක්` followed by ZWJ followed by `ර` renders as the single conjunct `ක්‍ර`.

```python
from grapheme_kit import Graphemizer

# The string contains an invisible ZWJ between ක් and ර
g = Graphemizer("ක්‍රමය")

print(g.graphemes)
# Output: ['ක්‍ර', 'ම', 'ය']
```

`grapheme-kit` maintains an internal list of valid Sinhala ZWJ sequences and ensures they are always preserved as a single grapheme.

---

**Next:** [Phonetic Decomposition](decomposition.md)
