# Phonetic Decomposition

The decomposition and composition utilities allow you to break down graphemes into their underlying phonetic components (consonant + vowel) and reassemble them. This is particularly useful for transliteration, spell-checking, or phonetic analysis.

## Decompose Text

To decompose text, you can use the `decompose` function. It breaks down clusters and replaces the attached vowel markers with their base vowel forms, leaving a standard hal/virama on the consonant.

### Tamil Example

```python
from graphemes_plusplus import decompose

decomposed = decompose("கொண்டு")
print(decomposed)
# Output: க்ஒண்ட்உ
```

### Sinhala Example

```python
from graphemes_plusplus import decompose

decomposed = decompose("සිංහල")
print(decomposed)
# Output: ස්ඉංහ්අල්අ
```

## Compose Text

You can pass the decomposed phonetic sequences back into the `compose` function to recreate the visual clusters.

```python
from graphemes_plusplus import compose

composed = compose("க்ஒண்ட்உ")
print(composed)
# Output: கொண்டு
```

## Round-Trip Proof

Applying decomposition and then composition will always yield the original string.

```python
from graphemes_plusplus import decompose, compose

text = "ஸ்ரீ மதி"
assert compose(decompose(text)) == text
print("Round-trip successful!")
# Output: Round-trip successful!
```

## Class API vs Function API

For convenience, `grapheme-kit` provides `decompose` and `compose` as module-level functions. However, if you prefer object-oriented patterns, you can use the class methods directly:

```python
from graphemes_plusplus.decomposer import Decomposer, Composer

# These behave exactly the same as the module-level functions
d = Decomposer.decompose("வணக்கம்")
c = Composer.compose(d)

print(c)
# Output: வணக்கம்
```

## Practical Use-Case: Vowel Substitution

Let's say you want to programmatically change the vowel attached to a consonant. You can achieve this by decomposing the cluster, replacing the vowel, and composing it back.

```python
from graphemes_plusplus import decompose, compose

def change_vowel(grapheme, new_vowel):
    decomposed = decompose(grapheme)
    # The decomposed form is always (Consonant + Hal) + (Base Vowel)
    # E.g., 'கா' -> 'க்ஆ'
    
    # Separate the consonant part from the old vowel
    # The consonant part is the first two code points (Letter + Hal)
    consonant_part = decomposed[:2] 
    
    # Construct the new sequence
    modified = consonant_part + new_vowel
    
    return compose(modified)

original = "கா"
# Change the vowel 'ஆ' to 'இ'
new_grapheme = change_vowel(original, "இ")

print(f"{original} -> {new_grapheme}")
# Output: கா -> கி
```
