# Distance Metrics

> Computes grapheme-aware edit distances between strings.

## Import

```python
from graphemes_plusplus import levenshtein, hamming
```

## API

### `levenshtein(s1: str, s2: str) -> int`

<div class="api-signature">
def levenshtein(s1: str, s2: str) -> int
</div>

Computes the Levenshtein distance (minimum number of single-character edits required to change one word into the other) between two strings. 

**Key Detail**: Unlike standard string distance libraries, this function computes the distance based on **grapheme clusters**, not code points.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `s1` | `str` | The first string. |
| `s2` | `str` | The second string. |

**Returns**: An `int` representing the edit distance.

**Example**:

```python
from graphemes_plusplus import levenshtein

# "ஸ்ரீ" is 1 grapheme. "ஸ்ரி" is 2 graphemes. Distance is 2.
print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
# Output: 2

# Sinhala conjunct example
print(levenshtein("ක්‍රම", "කම"))
# Output: 1

# Empty strings
print(levenshtein("", "test"))
# Output: 4
```

---

### `hamming(s1: str, s2: str) -> int`

<div class="api-signature">
def hamming(s1: str, s2: str) -> int
</div>

Computes the Hamming distance (number of positions at which the corresponding symbols are different) between two strings. 

**Key Detail**: Computes the distance based on grapheme clusters. The input strings are normally expected to have an equal number of graphemes. If the lengths differ, the missing graphemes are counted as mismatches.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `s1` | `str` | The first string. |
| `s2` | `str` | The second string. |

**Returns**: An `int` representing the Hamming distance.

**Example**:

```python
from graphemes_plusplus import hamming

print(hamming("රැ", "රැහ"))
# Output: 1

# Exact match
print(hamming("එවන්න", "එවන්න"))
# Output: 0
```
