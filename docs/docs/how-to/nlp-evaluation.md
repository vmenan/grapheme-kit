# NLP Evaluation

This guide demonstrates how to integrate `graphemes++` metrics into your NLP evaluation pipelines to accurately score model outputs.

## Compute GraphemeCHRF

The `GraphemeCHRF` class inherits from `sacrebleu`'s `CHRF` but overrides the tokenization to operate on grapheme boundaries.

You can compute a single score across an entire corpus using `corpus_score`. The method expects a list of hypothesis strings and a list of lists of reference strings.

```python
from graphemes_plusplus.metric import GraphemeCHRF

hypotheses = ["வணக்கம்"]
references = [["வணக்கம்"]]

metric = GraphemeCHRF()
score = metric.corpus_score(hypotheses, references)

print(score.score)
# Output: 100.0
```

### Sentence-level Scoring

If you need the score for a single prediction against its references, use `sentence_score`.

```python
from graphemes_plusplus.metric import GraphemeCHRF

metric = GraphemeCHRF()
score = metric.sentence_score("நல்ல", ["நல்ல மாணவன்"])

# A partial match gives a score > 0 but < 100
print(f"{score.score:.2f}")
# Output: 37.11
```

## Use chrF++ (with word n-grams)

Standard chrF calculates n-grams at the character (or grapheme) level. **chrF++** improves this by also incorporating word-level n-grams, which helps capture word order information.

To enable chrF++, simply pass the `word_order` parameter when initializing the metric. Usually, a word order of `2` (bigrams) is the standard.

```python
from graphemes_plusplus.metric import GraphemeCHRF

hypotheses = ["இருக்கிறது அழகாக மிகவும் வானிலை இன்று"]
references = [["இன்று வானிலை மிகவும் அழகாக இருக்கிறது"]]

# Standard chrF (grapheme n-grams only)
metric_chrf = GraphemeCHRF()
print(f"chrF: {metric_chrf.corpus_score(hypotheses, references).score:.2f}")
# Output: 47.18

# chrF++ (includes word bigrams)
metric_chrf_pp = GraphemeCHRF(word_order=2)
print(f"chrF++: {metric_chrf_pp.corpus_score(hypotheses, references).score:.2f}")
# Output: 47.89
```

## Compute Character Error Rate (CER)

The Character Error Rate is defined as the Levenshtein edit distance between the hypothesis and reference, divided by the total number of characters in the reference.

Our `CER` function computes this strictly on graphemes.

```python
from graphemes_plusplus.metric import CER

hypothesis = "කනවා"
reference = "කනව"

# The reference has 3 graphemes. 1 substitution is required.
# CER = 1 / 3 = 0.3333
error_rate = CER(hypothesis, reference)
print(f"{error_rate:.4f}")
# Output: 0.3333
```

## Compute Character N-gram F-score

You can calculate the F-score specifically for a particular n-gram size using `character_ngram_fscore`. By default, it calculates bigrams (`n=2`).

```python
from graphemes_plusplus.metric import character_ngram_fscore

hypothesis = "ආචාර්ය්ය"
reference = "ආචාරය්යා"

f_score = character_ngram_fscore(hypothesis, reference, n=2)
print(f"{f_score:.4f}")
# Output: 0.3333
```

## End-to-End Metric Comparison

Here is how you can run all the metrics on the same hypothesis-reference pair to compare the results:

```python
from graphemes_plusplus.metric import GraphemeCHRF, CER, character_ngram_fscore

hyp = "ஸ்ரீலங்கா ஒரு அழகான தீவு நாடு."
ref = "ஶ்ரீலங்கா ஒரு அழகான தீவு நாடு."

# 1. GraphemeCHRF
chrf = GraphemeCHRF().sentence_score(hyp, [ref]).score
print(f"GraphemeCHRF: {chrf:.2f}")

# 2. CER
cer = CER(hyp, ref)
print(f"CER:          {cer:.4f}")

# 3. N-gram F-score (bigrams)
ngram_f = character_ngram_fscore(hyp, ref, n=2)
print(f"N-gram F1:    {ngram_f:.4f}")

# Output:
# GraphemeCHRF: 91.85
# CER:          0.0588
# N-gram F1:    0.8750
```
