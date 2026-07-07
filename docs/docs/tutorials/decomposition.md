# Phonetic Decomposition

This section demonstrates how to break graphemes down to their phonetic building blocks and rebuild them.

## What is Decomposition?

Every Indic grapheme cluster is built from a **consonant** (the base shape) and a **vowel** (which determines how the consonant sounds). For example:

- `கா` = consonant `க` + vowel `ஆ`
- `கி` = consonant `க` + vowel `இ`

Decomposition splits a grapheme into these two parts, represented as:
- The consonant with a **hal/virama** marker (the silent consonant form)
- The **base independent vowel**

For example: `கா` decomposes into `க்` + `ஆ`.

## Decomposing Tamil Text

```python
from graphemes_plusplus import decompose

# "ka" with the "aa" vowel
print(decompose("கா"))
# Output: க்ஆ

# A full word — vowels are separated from their consonants
print(decompose("வணக்கம்"))
# Output: வ்அண்அக்க்அம்
```

## Decomposing Sinhala Text

```python
from graphemes_plusplus import decompose

print(decompose("සිංහල"))
# Output: ස්ඉංහ්අල්අ
```

## Composing Back

Applying `compose()` to a decomposed string will reconstruct the original grapheme clusters.

```python
from graphemes_plusplus import decompose, compose

original = "வணக்கம்"
decomposed = decompose(original)
restored = compose(decomposed)

print(restored)           # Output: வணக்கம்
assert original == restored  # Always true
```

## Practical Use: Changing a Vowel

Decomposition is particularly useful when you want to programmatically change the vowel of a consonant.

```python
from graphemes_plusplus import decompose, compose

# Original: "ka" (க + ஆ)
# Goal: change the vowel to "இ" to get "ki" (கி)

decomposed = decompose("கா")
# decomposed is now "க்ஆ"

# Replace the vowel part manually
modified = "க்இ"

result = compose(modified)
print(result)
# Output: கி
```

## Summary

You have completed the tutorial series. Here is what you covered:

1. The difference between code points and graphemes, and why it matters for evaluation.
2. Why grapheme-aware metrics complement -- rather than replace -- chrF, chrF++, CER, and CharBLEU, and produce identical results for scripts where code points and graphemes already coincide.
3. How the `Graphemizer` pipeline works internally.
4. How to segment Tamil conjuncts and Sinhala ZWJ sequences correctly.
5. How to decompose and compose graphemes for phonetic manipulation.

**Continue to:** [NLP Evaluation](../how-to/nlp-evaluation.md) for practical task-specific recipes.
