# Metrics

> Classes and functions for evaluating NLP models using grapheme-aware calculations.

## Import

```python
from graphemes_plusplus.metric import GraphemeCHRF, CER, character_ngram_fscore
```

## API

### `GraphemeCHRF`

<div class="api-signature">
class GraphemeCHRF(CHRF)
</div>

Inherits from `sacrebleu.metrics.chrf.CHRF`. Computes the chrF (and chrF++) metric at the grapheme level. It accepts raw text strings and automatically segments them into grapheme clusters using `Graphemizer` before computing n-gram statistics.

**Constructor Parameters**:

(Inherited from `CHRF`)
- `char_order` (int): Maximum order of character (grapheme) n-grams (default 6).
- `word_order` (int): Maximum order of word n-grams (default 0). Set to `2` for standard chrF++.
- `beta` (float): Beta parameter to balance precision and recall (default 2.0).
- `lowercase` (bool): If `True`, lowercases the input before scoring.
- `whitespace` (bool): If `True`, includes whitespaces in the n-gram extraction.

#### `corpus_score(hypotheses: list[str], references: list[list[str]]) -> CHRFScore`

<div class="api-signature">
def corpus_score(hypotheses, references)
</div>

Calculates the score over an entire corpus.

#### `sentence_score(hypothesis: str, references: list[str]) -> CHRFScore`

<div class="api-signature">
def sentence_score(hypothesis, references)
</div>

Calculates the score for a single sentence.

**Example**:

```python
from graphemes_plusplus.metric import GraphemeCHRF

hyp = ["வணக்கம்"]
refs = [["வணக்கம்"]]

chrf = GraphemeCHRF()
print(chrf.corpus_score(hyp, refs).score)
# Output: 100.0

chrf_pp = GraphemeCHRF(word_order=2)
print(chrf_pp.corpus_score(hyp, refs).score)
# Output: 100.0
```

---

### `CER(hypothesis: str, reference: str) -> float`

<div class="api-signature">
def CER(hypothesis: str, reference: str) -> float
</div>

Computes the Character Error Rate (CER) between a hypothesis and reference string based on graphemes. It is defined as the grapheme Levenshtein distance divided by the number of graphemes in the reference.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `hypothesis` | `str` | The predicted string. |
| `reference` | `str` | The ground truth string. |

**Returns**: A `float` representing the error rate (0.0 means perfect match).

**Example**:

```python
from graphemes_plusplus.metric import CER

print(CER("කනවා", "කනව"))
# Output: 0.3333333333333333

print(CER("", ""))
# Output: 0.0
```

---

### `character_ngram_fscore(hypothesis: str, reference: str, n: int = 2) -> float`

<div class="api-signature">
def character_ngram_fscore(hypothesis: str, reference: str, n: int = 2) -> float
</div>

Computes the Character N-gram F-score between a hypothesis and a reference string. The text is split into character n-grams based on grapheme boundaries, then Precision, Recall, and F-score are calculated.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `hypothesis` | `str` | The predicted string. |
| `reference` | `str` | The ground truth string. |
| `n` | `int` | Size of the character n-gram (default `2` for bigrams). |

**Returns**: A `float` representing the F-score (0.0 to 1.0).

**Example**:

```python
from graphemes_plusplus.metric import character_ngram_fscore

# Perfect bigram match
print(character_ngram_fscore("ප්‍රධාන", "ප්‍රධාන"))
# Output: 1.0

# Partial match
print(character_ngram_fscore("ආචාර්ය්‍ය", "ආචාරය්‍යා", n=2))
# Output: 0.3333333333333333
```
