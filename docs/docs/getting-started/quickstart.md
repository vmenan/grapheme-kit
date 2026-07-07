# Quick Start

This guide gives you a fast, hands-on experience with every major feature in `grapheme-kit` under 5 minutes.

## 1. Evaluate with Metrics

Calculate NLP evaluation metrics scaled to grapheme boundaries. This ensures that a single missed modifier doesn't unfairly penalize the model as multiple code point errors. `grapheme-kit` provides `GraphemeCHRF` (chrF/chrF++), `CER`, and `charbleu`.

```python
from graphemes_plusplus.metric import GraphemeCHRF, CER, charbleu

hypothesis = "සිංහල"
reference = "සිංහල"

# GraphemeCHRF Corpus Score (chrF)
metric = GraphemeCHRF()
score = metric.corpus_score([hypothesis], [[reference]])
print(score.score)
# Output: 100.0

# Character Error Rate (CER)
error_rate = CER("කනවා", "කනව")
print(error_rate)
# Output: 0.3333333333333333 (1 error / 3 total graphemes)

# CharBLEU
cb_score = charbleu("Xin chào các bạn", "Xin chào bạn")
print(cb_score)
# Output: 0.9146912192286945
```

## 2. Compute Distance

Compute the edit distance (Levenshtein), Hamming distance, Damerau-Levenshtein, Jaro, Jaro-Winkler, and Longest Common Subsequence between two strings using grapheme-aware calculations.

```python
from graphemes_plusplus import levenshtein, hamming
from graphemes_plusplus.distance import damerau_levenshtein, jaro, jaro_winkler, longest_common_subsequence

# "ஸ்ரீ" is 1 grapheme. "ஸ்ரி" is 2 graphemes.
# Therefore, the Levenshtein distance is 2.
print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
# Output: 2

print(hamming("රැ", "රැහ"))
# Output: 1

print(damerau_levenshtein("weird", "wierd"))
# Output: 1

print(jaro("MARTHA", "MARHTA"))
# Output: 0.9444444444444445

print(longest_common_subsequence("GATTACA", "GCATCAG"))
# Output: 5
```

## 3. Segment Text

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

## 4. Decompose & Compose Phonetics

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

## Next Steps

- Want a deeper understanding of the theory? Check out the [Tutorials](../tutorials/introduction.md) series.
- Looking for practical application patterns? Read the [How-To Guides](../how-to/nlp-evaluation.md).
- Need comprehensive details? Dive into the [API Reference](../reference/metrics.md).
