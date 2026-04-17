# Metrics

Grapheme-aware evaluation metrics for NLP tasks involving Tamil and Sinhala text. Includes `GraphemeCHRF` (chrF/chrF++) and `CER` (Character Error Rate).

**Module:** `graphemes_plusplus.metric`

## GraphemeCHRF

Computes the chrF(++) metric at the grapheme level. Extends SacreBLEU's `CHRF` class to operate on grapheme clusters instead of raw Unicode characters.

```python
class GraphemeCHRF(char_order=6, word_order=0, beta=2, ...)
```

**Inherits from:** `sacrebleu.metrics.chrf.CHRF`

### Parameters

Inherits all parameters from SacreBLEU's `CHRF`. Key parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `char_order` | `int` | `6` | Maximum order of character (grapheme) n-grams |
| `word_order` | `int` | `0` | Maximum order of word n-grams. Set to `2` for chrF++ |
| `beta` | `float` | `2` | Balance between precision and recall |
| `lowercase` | `bool` | `False` | Whether to lowercase before comparison |
| `whitespace` | `bool" | `False` | Whether to include whitespace graphemes in n-grams |

### Configurations

**chrF (default)**

```python
from graphemes_plusplus.metric import GraphemeCHRF

chrf = GraphemeCHRF()  # word_order=0
```


**chrF++**

```python
from graphemes_plusplus.metric import GraphemeCHRF

chrf_pp = GraphemeCHRF(word_order=2)  # includes word n-grams
```


### Methods

#### `corpus_score(hypotheses, references) → CHRFScore`

Compute corpus-level chrF score.

```python
>>> chrf = GraphemeCHRF()
>>> score = chrf.corpus_score(
...     ["வணக்கம் உலகம்"],      # hypotheses
...     [["வணக்கம் உலகம்"]]     # references (list of lists)
... )
>>> print(score.score)
100.0
```

#### `sentence_score(hypothesis, references) → CHRFScore`

Compute sentence-level chrF score.

```python
>>> chrf = GraphemeCHRF()
>>> score = chrf.sentence_score("සිංහල", ["සිංහල"])
>>> print(score.score)
100.0
```

### How It Differs from Standard chrF

| Aspect | Standard chrF | GraphemeCHRF |
|---|---|---|
| Unit | Unicode code points | Grapheme clusters |
| `ஸ்ரீ` treated as | 4 separate characters | 1 grapheme |
| Sinhala ZWJ | Broken into parts | Kept as single grapheme |
| Better for | Latin scripts | Indic scripts (Tamil, Sinhala) |

---

## CER

Computes the **Character Error Rate** between a hypothesis and reference string at the grapheme level.

```python
CER(hypothesis: str, reference: str) → float
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `hypothesis` | `str` | The predicted/generated string |
| `reference` | `str` | The ground truth string |
| **Returns** | `float` | CER value (0.0 = perfect match) |

### Formula

$$
\text{CER} = \frac{\text{LevenshteinDistance}(\text{hyp}, \text{ref})}{\text{len}(\text{ref\_graphemes})}
$$

### Examples

```python
>>> from graphemes_plusplus.metric import CER
>>> CER("வணக்கம்", "வணக்கம்")
0.0
>>> CER("", "வணக்கம்")
1.0
```

> **Edge cases**
> - If both hypothesis and reference are empty, CER returns `0.0`
> - If only the reference is empty but hypothesis is not, CER returns `1.0`
>
>
## See Also

- [Distance Functions](distance.md) — The Levenshtein function used by CER
- [Graphemizer](graphemizer.md) — Segments text into graphemes before metric computation
