# Distance Metrics

> Computes grapheme-aware edit distances and similarity scores between strings.

## Import

```python
from grapheme_kit.distance import (
    levenshtein,
    hamming,
    damerau_levenshtein,
    jaro,
    jaro_winkler,
    longest_common_subsequence,
)
```

## API

All six functions share the same contract: they operate on **grapheme clusters**, not code points, and take two strings as input.

### `levenshtein(s1: str, s2: str) -> int`
Minimum number of single-grapheme edits (insert/delete/substitute) to turn `s1` into `s2`.

### `damerau_levenshtein(s1: str, s2: str) -> int`
Like `levenshtein`, but also treats an adjacent-grapheme transposition as a single edit.

### `hamming(s1: str, s2: str) -> int`
Number of positions at which the corresponding graphemes differ. Inputs are normally expected to have the same grapheme count; mismatched-length inputs count the extra graphemes as mismatches.

### `jaro(s1: str, s2: str) -> float`
Jaro similarity (0.0-1.0, higher is more similar) based on matching and transposed graphemes within a proximity window.

### `jaro_winkler(s1: str, s2: str) -> float`
Jaro similarity with an added bonus for a shared grapheme prefix -- typically the better choice for short strings like names or single words.

### `longest_common_subsequence(s1: str, s2: str) -> int`
Length of the longest sequence of graphemes (not necessarily contiguous) common to both strings, in order.

**Example**:

```python
from grapheme_kit import levenshtein, hamming
from grapheme_kit.distance import damerau_levenshtein, jaro, jaro_winkler, longest_common_subsequence

# "ஸ்ரீ" is 1 grapheme. "ஸ்ரி" is 2 graphemes.
print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
# Output: 2

# Sinhala conjunct example
print(levenshtein("ක්‍රම", "කම"))
# Output: 1

print(hamming("රැ", "රැහ"))
# Output: 1

print(damerau_levenshtein("weird", "wierd"))
# Output: 1

print(jaro("MARTHA", "MARHTA"))
# Output: 0.9444444444444445

print(jaro_winkler("MARTHA", "MARHTA"))
# Output: 0.9611111111111111

print(longest_common_subsequence("GATTACA", "GCATCAG"))
# Output: 5
```
