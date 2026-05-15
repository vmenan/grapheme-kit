# Quick Start

This guide gives you a fast, hands-on experience with every major feature in `graphemes++` under 5 minutes.

## 1. Segment Text

Use `Graphemizer` to split text into visual grapheme clusters correctly.

```python
from graphemes_plusplus import Graphemizer

text = "ஸ்ரீ மதி"
g = Graphemizer(text)

print(g.graphemes)
# Output: ['ஸ்ரீ', ' ', 'ம', 'தி']

print(len(g))
# Output: 4

for grapheme in g:
    print(grapheme)
# Output:
# ஸ்ரீ
#  
# ம
# தி
```

## 2. Compute Distance

Compute the edit distance (Levenshtein) and Hamming distance between two strings using grapheme-aware calculations.

```python
from graphemes_plusplus import levenshtein, hamming

# "ஸ்ரீ" is 1 grapheme. "ஸ்ரி" is 2 graphemes.
# Therefore, the distance is 2.
print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
# Output: 2

print(hamming("රැ", "රැහ"))
# Output: 1
```

## 3. Decompose & Compose Phonetics

Break down complex clusters into their phonetic base consonants and vowels, and compose them back seamlessly.

```python
from graphemes_plusplus import decompose, compose

# Decomposing a complex Tamil cluster
decomposed = decompose("ஸ்ரீ")
print(decomposed)
# Output: ஸ்ர்ஈ

# Composing it back to the original form
composed = compose(decomposed)
print(composed)
# Output: ஸ்ரீ
```

## 4. Evaluate with Metrics

Calculate NLP evaluation metrics scaled to grapheme boundaries. This ensures that a single missed modifier doesn't unfairly penalize the model as multiple code point errors.

```python
from graphemes_plusplus.metric import GraphemeCHRF, CER

hypothesis = "සිංහල"
reference = "සිංහල"

# GraphemeCHRF Corpus Score
metric = GraphemeCHRF()
score = metric.corpus_score([hypothesis], [[reference]])
print(score.score)
# Output: 100.0

# Character Error Rate (CER)
error_rate = CER("කනවා", "කනව")
print(error_rate)
# Output: 0.3333333333333333 (1 error / 3 total graphemes)
```

## Next Steps

- Want a deeper understanding of the theory? Check out the [Tutorials](../tutorials/introduction.md) series.
- Looking for practical application patterns? Read the [How-To Guides](../how-to/grapheme-segmentation.md).
- Need comprehensive details? Dive into the [API Reference](../reference/graphemizer.md).
