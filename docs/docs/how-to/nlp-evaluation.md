# NLP Evaluation

This guide demonstrates how to integrate `grapheme-kit` metrics into your NLP evaluation pipelines to accurately score model outputs -- on any language, with the deepest corrections available for Tamil and Sinhala.

## Compute GraphemeCHRF (chrF)

The `GraphemeCHRF` class inherits from `sacrebleu`'s `CHRF` but overrides the tokenization to operate on grapheme boundaries.

You can compute a single score across an entire corpus using `corpus_score`. The method expects a list of hypothesis strings and a list of lists of reference strings.

```python
from grapheme_kit.metric import GraphemeCHRF

hypotheses = ["Good morning, how are you?"]
references = [["Good morning, how are you today?"]]

metric = GraphemeCHRF()
score = metric.corpus_score(hypotheses, references)
print(score.score)
# Output: 79.25462666195415
```

### Sentence-level Scoring

```python
from grapheme_kit.metric import GraphemeCHRF

metric = GraphemeCHRF()
score = metric.sentence_score("Guten Morgen", ["Guten Morgen zusammen"])
print(score.score)
# Output: 56.5271353532257
```

## Use chrF++ (with word n-grams)

Standard chrF calculates n-grams at the character (or grapheme) level. **chrF++** improves this by also incorporating word-level n-grams, which helps capture word order information. Pass `word_order=2` (bigrams is the standard) to enable it.

```python
from grapheme_kit.metric import GraphemeCHRF

hypotheses = ["The weather is very nice today"]
references = [["Today the weather is very nice"]]

metric_chrf = GraphemeCHRF()
print("chrF:  ", metric_chrf.corpus_score(hypotheses, references).score)
# Output: chrF:   81.46833239224543

metric_chrf_pp = GraphemeCHRF(word_order=2)
print("chrF++:", metric_chrf_pp.corpus_score(hypotheses, references).score)
# Output: chrF++: 76.93458262751741
```

## Compute Character Error Rate (CER)

`CER(hypothesis: str, reference: str) -> float` is the Levenshtein edit distance between the hypothesis and reference, divided by the number of graphemes in the reference.

```python
from grapheme_kit.metric import CER

# Sinhala: one substitution.
print(CER("කනවා", "කනව"))
# Output: 0.3333333333333333
```

## Compute CharBLEU

`charbleu(reference: str, hypothesis: str, max_n: int = 4, weights=None) -> float` computes a BLEU-style n-gram precision score at the grapheme level. Note the argument order is *(reference, hypothesis)*.

```python
from grapheme_kit.metric import charbleu

print(charbleu("Xin chào các bạn", "Xin chào bạn"))
# Output: 0.9146912192286945
```

## End-to-End Metric Comparison

Run all four metrics on the same hypothesis-reference pair to compare results:

```python
from grapheme_kit.metric import GraphemeCHRF, CER, charbleu

hyp = "안녕하세요, 만나서 반갑습니다"
ref = "안녕하세요, 만나서 반갑습니다요"

chrf = GraphemeCHRF().sentence_score(hyp, [ref]).score
cer = CER(hyp, ref)
cb = charbleu(ref, hyp)

print("GraphemeCHRF:", chrf)
# Output: GraphemeCHRF: 93.36837027445603
print("CER:         ", cer)
# Output: CER:          0.058823529411764705
print("CharBLEU:    ", cb)
# Output: CharBLEU:     1.0
```
