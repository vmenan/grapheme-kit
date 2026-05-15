# Measuring Quality with Metrics

This final section shows how to evaluate NLP model output using grapheme-aware metrics.

## Why Standard Metrics Fall Short

If you use standard string-based metrics to evaluate an Indic NLP model, you will get misleading results.

Consider the Tamil word for "Shri" written as `ஸ்ரீ`. A standard code-point CER calculation treats it as 4 separate characters. If a model produces the slightly wrong form `ஸ்ரி`, a standard metric counts only 1 error out of 4 characters (25% error rate). But visually, the word is entirely wrong — it should be 1 error out of 1 grapheme (100% error rate).

`graphemes++` corrects this by evaluating all metrics at the grapheme boundary.

## Character Error Rate (CER)

CER measures the proportion of graphemes that need to be corrected to turn the hypothesis into the reference.

```python
from graphemes_plusplus.metric import CER

hypothesis = "කනවා"
reference  = "කනව"

# The reference has 3 graphemes. 1 grapheme is wrong.
# CER = 1 / 3 = 0.333
error_rate = CER(hypothesis, reference)
print(f"{error_rate:.4f}")
# Output: 0.3333
```

## GraphemeCHRF

GraphemeCHRF is a corpus-level metric that measures the overlap of grapheme n-grams between hypothesis and reference. A score of 100.0 means a perfect match.

```python
from graphemes_plusplus.metric import GraphemeCHRF

metric = GraphemeCHRF()

# Perfect match
score = metric.corpus_score(["வணக்கம்"], [["வணக்கம்"]])
print(score.score)
# Output: 100.0

# Partial match
score = metric.corpus_score(["நல்ல"], [["நல்ல மாணவன்"]])
print(f"{score.score:.2f}")
# Output: 37.11
```

## Summary

You have completed the tutorial series. Here is what you covered:

1. The difference between code points and graphemes.
2. How the `Graphemizer` pipeline works internally.
3. How to segment Tamil conjuncts and Sinhala ZWJ sequences correctly.
4. How to decompose and compose graphemes for phonetic manipulation.
5. Why grapheme-aware evaluation metrics produce more accurate and fair results.

**Continue to:** [How-To Guides](../how-to/grapheme-segmentation.md) for practical task-specific recipes.
