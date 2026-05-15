# Segmenting Text

This section walks you through your first grapheme segmentation using `graphemes++`.

## Your First Segmentation

Let's segment a simple Tamil word using the `Graphemizer` class.

```python
from graphemes_plusplus import Graphemizer

# "vanakkam" — hello in Tamil
g = Graphemizer("வணக்கம்")

print(g.graphemes)
# Output: ['வ', 'ண', 'க்', 'க', 'ம்']

print(f"Number of graphemes: {len(g)}")
# Output: Number of graphemes: 5
```

Notice how `க்` is kept together as a single unit rather than being split into `க` and the pulli marker `்`. The `Graphemizer` correctly identifies this as one atomic visual cluster.

## Iterating Over Graphemes

The `Graphemizer` instance is directly iterable. You can loop through each grapheme just like a list:

```python
from graphemes_plusplus import Graphemizer

for grapheme in Graphemizer("வணக்கம்"):
    print(grapheme)

# Output:
# வ
# ண
# க்
# க
# ம்
```

## Accurate Length Counting

Standard `len()` on an Indic string returns the number of code points, not the number of visual characters. Use `len(Graphemizer(...))` for an accurate count:

```python
text = "வணக்கம்"

print(len(text))                # Output: 8  (code points — inaccurate)
print(len(Graphemizer(text)))   # Output: 5  (graphemes — accurate)
```

---

**Next:** [Understanding Conjuncts](conjuncts.md)
