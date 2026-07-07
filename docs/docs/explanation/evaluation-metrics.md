# Evaluation Metrics

This page explains the reasoning behind `grapheme-kit`'s evaluation metrics: not as a Tamil/Sinhala-specific fix, but as a more general definition of what a character-level metric should measure.

## The Problem: Two Different Definitions of "Character"

Character-level NLP metrics — chrF, CER, CharBLEU, and others — are built on an implicit assumption: that a Unicode **code point** is the same thing as a **grapheme**, the single visual unit a human reads as "one character."

For English and most Latin-script languages, that assumption is true. A code point and a grapheme are the same thing, so it never comes up as a problem, and standard metrics are already correct.

For Tamil, Sinhala, and other scripts that combine consonants, vowel signs, and joiners into a single visual cluster, the assumption is false. One grapheme can be built from two, three, or four code points. A metric computed on code points is measuring something the reader never actually perceives: it is counting encoding units, not visual units.

`grapheme-kit` does not introduce a Tamil/Sinhala-specific metric. It defines each metric at the grapheme level everywhere, which is a strictly more general and more correct definition. Where code points and graphemes coincide (English, German, ...), the grapheme-level score matches the code-point score exactly, so nothing regresses. Where they diverge (Tamil, Sinhala, ...), the grapheme-level score is the one that reflects what a person actually reads.

**We frame this as a complement to existing metrics, not a replacement.** A code-point metric like chrF tells you about local, per-symbol changes. A grapheme-level metric tells you about the reader-perceived, global picture. Reporting both gives a fuller view than either alone.

### Code-Point vs. Grapheme CER Comparison

Let's look at a concrete example using the Tamil word for "Shri" (`ஸ்ரீ`).

- **Reference**: `ஸ்ரீ` (4 code points: `ஸ` + `்` + `ர` + `ee` (`ீ`), but **1 grapheme**)
- **Hypothesis**: `ஸ்ரி` (4 code points: `ஸ` + `்` + `ர` + `i` (`ி`), but **2 graphemes**)

**Standard Code-Point CER:**
The edit distance between the code points is 1 (swapping `ீ` for `ி`).
The reference length is 4 code points.
CER = 1 / 4 = **0.25 (25% error)**

**Grapheme-Aware CER (`grapheme-kit`):**
The edit distance between the graphemes (`['ஸ்ரீ']` vs `['ஸ்', 'ரி']`) is 2.
The reference length is 1 grapheme.
CER = 2 / 1 = **2.0 (200% error)**

The grapheme-aware CER correctly reflects that the visual output is entirely broken and incorrect, whereas the code-point CER suggests it is 75% correct. Note that if the reference and hypothesis had instead been in English, this entire distinction disappears — code points and graphemes are the same thing, and both formulas produce identical numbers.

---

## Character Error Rate (CER)

CER is typically used in Speech Recognition and Optical Character Recognition (OCR).

The formula is defined as the Levenshtein edit distance between the hypothesis ($H$) and reference ($R$), divided by the total number of graphemes in the reference.

$$ \text{CER} = \frac{\text{Levenshtein}(H, R)}{|R|} $$

In `grapheme-kit`, both the Levenshtein distance and $|R|$ are computed strictly over grapheme clusters — for every language, not only Tamil and Sinhala. Signature: `CER(hypothesis: str, reference: str) -> float`.

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

`grapheme-kit` implements both through one class, `GraphemeCHRF`, by extending `sacrebleu`'s robust `CHRF` implementation and forcing the extraction loop to tokenize by graphemes instead of code points — for any input language, not only Tamil and Sinhala. Pass `word_order=2` for chrF++; the default (`word_order=0`) gives plain chrF.

---

## CharBLEU

CharBLEU is a character-level adaptation of BLEU: it computes n-gram precision at the grapheme level (up to `max_n`, default 4) and combines the precisions with a geometric mean, applying a brevity penalty when the hypothesis is shorter than the reference. Signature: `charbleu(reference: str, hypothesis: str, max_n: int = 4, weights: list[float] | None = None) -> float` — note the argument order is *(reference, hypothesis)*, the reverse of `CER`'s *(hypothesis, reference)*; check the signature when switching between metrics.

Use CharBLEU when you want a BLEU-style precision-weighted score at the grapheme level rather than chrF's precision/recall balance.

---

## Where This Matters Most

The metric definitions above apply uniformly to any language. In practice, the numbers only *change* for scripts where graphemes and code points diverge — which is exactly where Tamil and Sinhala live, and why `grapheme-kit` invests in [Tamil](tamil-script-rules.md) and [Sinhala](sinhala-script-rules.md) script-specific segmentation rules: a metric is only as correct as the grapheme splitting underneath it.
