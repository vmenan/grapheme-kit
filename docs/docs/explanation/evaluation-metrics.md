# Evaluation Metrics

This page provides the mathematical foundations behind the NLP evaluation metrics included in `graphemes++` and explains why grapheme-aware scaling is critical for Indic scripts.

## Why Grapheme-Level Metrics?

When evaluating Natural Language Processing (NLP) models, such as Machine Translation or Automatic Speech Recognition (ASR), we compare the model's hypothesis against a human reference.

Standard Python libraries compute metrics based on **Unicode code points**. For English, 1 visual character = 1 code point, so the math works perfectly. 

For Indic scripts, 1 visual character can equal 3 or 4 code points. If a model misses a single vowel marker (e.g., generating `க` instead of `கா`), standard metrics will penalize the model for missing the `ா` code point, altering the denominator and skewing the error rate disproportionately compared to English.

### Code-Point vs. Grapheme CER Comparison

Let's look at a concrete example using the Tamil word for "Shri" (`ஸ்ரீ`).

- **Reference**: `ஸ்ரீ` (4 code points: `ஸ` + `்` + `ர` + `ீ`, but **1 grapheme**)
- **Hypothesis**: `ஸ்ரி` (4 code points: `ஸ` + `்` + `ர` + `ி`, but **2 graphemes**)

**Standard Code-Point CER:**
The edit distance between the code points is 1 (swapping `ீ` for `ி`).
The reference length is 4 code points.
CER = 1 / 4 = **0.25 (25% error)**

**Grapheme-Aware CER (`graphemes++`):**
The edit distance between the graphemes (`['ஸ்ரீ']` vs `['ஸ்', 'ரி']`) is 2.
The reference length is 1 grapheme.
CER = 2 / 1 = **2.0 (200% error)**

The grapheme-aware CER correctly reflects that the visual output is entirely broken and incorrect, whereas the code-point CER suggests it is 75% correct!

---

## Character Error Rate (CER)

CER is typically used in Speech Recognition and Optical Character Recognition (OCR).

The formula is defined as the Levenshtein edit distance between the hypothesis ($H$) and reference ($R$), divided by the total number of items in the reference.

$$ \text{CER} = \frac{\text{Levenshtein}(H, R)}{|R|} $$

In `graphemes++`, both the Levenshtein distance and $|R|$ are computed strictly over grapheme clusters.

---

## chrF and chrF++

chrF (Character n-gram F-score) is widely used in Machine Translation evaluation. It calculates the precision and recall of n-grams between the hypothesis and reference.

For a given n-gram length $n$:

$$ \text{Precision}_n = \frac{\text{matching n-grams}}{\text{total n-grams in Hypothesis}} $$

$$ \text{Recall}_n = \frac{\text{matching n-grams}}{\text{total n-grams in Reference}} $$

The F-score for n-grams up to max order $N$ (usually 6) is combined using a $\beta$ parameter (usually 2.0, which favors recall):

$$ \text{chrF} = \frac{(1 + \beta^2) \cdot \text{Precision} \cdot \text{Recall}}{\beta^2 \cdot \text{Precision} + \text{Recall}} $$

### What is chrF++?

chrF calculates n-grams only at the character (or grapheme) level. **chrF++** (Popović, 2017) improves upon this by also extracting n-grams at the *word* level. Including word n-grams (usually bigrams, `word_order=2`) helps the metric account for word order, which character n-grams alone can sometimes miss.

`graphemes++` implements `GraphemeCHRF` by extending `sacrebleu`'s robust implementation, but forcing the extraction loop to tokenize by graphemes instead of code points.

---

## Character N-gram F-score

This is a simpler, more direct calculation of the F1-score for a specific n-gram length (default 2, bigrams). It does not average across multiple lengths like chrF does.

$$ F = \frac{2 \cdot P \cdot R}{P + R} $$

Use this metric when you want fine-grained analysis of how well specific grapheme sequences are being modeled, rather than a broad corpus-level translation score.
