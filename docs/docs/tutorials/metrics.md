# Measuring Quality with Metrics

This section shows how to evaluate NLP model output using grapheme-aware metrics — the core reason `grapheme-kit` exists.

## Why Standard Metrics Fall Short

Character-level metrics assume that one code point is one visually-perceived character. For English, that's true, so nothing here changes the numbers you already get. For scripts like Tamil and Sinhala, where several code points can render as a single visual grapheme, that assumption breaks down.

Consider the Tamil word for "Shri" written as `ஸ்ரீ`. A standard code-point CER calculation treats it as 4 separate characters. If a model produces the slightly wrong form `ஸ்ரி`, a standard metric counts only 1 error out of 4 characters (25% error rate). But visually, the word is entirely wrong — it should be 1 error out of 1 grapheme (100% error rate).

`grapheme-kit` corrects this by evaluating all metrics at the grapheme boundary — for any language you throw at it. This is not a replacement for chrF, chrF++, or CER; it's the same metrics, computed on the unit a reader actually perceives. Where that unit already matches a code point, as it does in English or German, the score doesn't change at all.

## Character Error Rate (CER)

```python
from graphemes_plusplus.metric import CER

# English: code point and grapheme are the same thing here, so this
# matches a standard character-level CER exactly.
print(CER("anwer", "answer"))
# Output: 0.16666666666666666

# Sinhala: one dropped vowel sign changes the whole visual unit.
print(CER("කනවා", "කනව"))
# Output: 0.3333333333333333
```

## GraphemeCHRF (chrF and chrF++)

```python
from graphemes_plusplus.metric import GraphemeCHRF

metric = GraphemeCHRF()

# German -- a small word-order slip
print(metric.corpus_score(["Das Wetter ist heute sehr schoen"], [["Heute ist das Wetter sehr schoen"]]).score)
# Output: 62.561731210281934

# Tamil -- partial match
print(metric.corpus_score(["நல்ல"], [["நல்ல மாணவன்"]]).score)
# Output: 37.10506980161646
```

## CharBLEU

```python
from graphemes_plusplus.metric import charbleu

# note argument order: (reference, hypothesis)
print(charbleu("Good morning everyone", "Good morning everybody"))
# Output: 0.8151678595510183
```

---

**Next:** [Segmenting Text](segmentation.md)
