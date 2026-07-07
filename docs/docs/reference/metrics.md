# Metrics

> Classes and functions for evaluating NLP models using grapheme-aware calculations.

## Import

```python
from grapheme_kit.metric import GraphemeCHRF, CER, charbleu
```

## API

### `GraphemeCHRF`

<div class="api-signature">
class GraphemeCHRF(CHRF)
</div>

Inherits from `sacrebleu.metrics.chrf.CHRF`. Computes the chrF (and chrF++) metric at the grapheme level. It accepts raw text strings and automatically segments them into grapheme clusters using `Graphemizer` before computing n-gram statistics.

**Constructor Parameters** (inherited from `CHRF`):
- `char_order` (int): Maximum order of character (grapheme) n-grams (default 6).
- `word_order` (int): Maximum order of word n-grams (default 0). Set to `2` for standard chrF++.
- `beta` (float): Beta parameter to balance precision and recall (default 2.0).
- `lowercase` (bool): If `True`, lowercases the input before scoring.
- `whitespace` (bool): If `True`, includes whitespaces in the n-gram extraction.

#### `corpus_score(hypotheses: list[str], references: list[list[str]]) -> CHRFScore`
Calculates the score over an entire corpus.

#### `sentence_score(hypothesis: str, references: list[str]) -> CHRFScore`
Calculates the score for a single sentence.

**Example**:

```python
from grapheme_kit.metric import GraphemeCHRF

hyp = ["Good morning, how are you?"]
refs = [["Good morning, how are you today?"]]

chrf = GraphemeCHRF()
print(chrf.corpus_score(hyp, refs).score)
# Output: 79.25462666195415

chrf_pp = GraphemeCHRF(word_order=2)
print(chrf_pp.corpus_score(hyp, refs).score)
# Output: 79.86632440942023
```

---

### `CER(hypothesis: str, reference: str) -> float`

<div class="api-signature">
def CER(hypothesis: str, reference: str) -> float
</div>

Computes the Character Error Rate (CER) between a hypothesis and reference string based on graphemes: the grapheme Levenshtein distance divided by the number of graphemes in the reference.

**Returns**: A `float` (0.0 means perfect match; can exceed 1.0, unlike bounded metrics, when the hypothesis is much longer/more broken than the reference).

**Example**:

```python
from grapheme_kit.metric import CER

print(CER("කනවා", "කනව"))
# Output: 0.3333333333333333

print(CER("annyeonghaseyo", "annyeonghaseyo yo"))
# Output: 0.17647058823529413
```

---

### `charbleu(reference: str, hypothesis: str, max_n: int = 4, weights: list[float] | None = None) -> float`

<div class="api-signature">
def charbleu(reference: str, hypothesis: str, max_n: int = 4, weights=None) -> float
</div>

Grapheme-aware CharBLEU: a character(grapheme)-level BLEU variant. Computes n-gram precision at each order from 1 to `max_n`, combines them with a (optionally weighted) geometric mean, and applies a brevity penalty if the hypothesis has fewer graphemes than the reference.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `reference` | `str` | The ground-truth string. Note this is the *first* positional argument, unlike `CER`. |
| `hypothesis` | `str` | The predicted string. |
| `max_n` | `int` | Maximum grapheme n-gram order considered (default 4). |
| `weights` | `list[float] \| None` | Per-order weights, must sum to 1 if provided; defaults to uniform weighting across valid orders. |

**Returns**: A `float` between 0.0 and 1.0 (1.0 is a perfect match).

**Example**:

```python
from grapheme_kit.metric import charbleu

print(charbleu("Xin chào các bạn", "Xin chào bạn"))
# Output: 0.9146912192286945
```
