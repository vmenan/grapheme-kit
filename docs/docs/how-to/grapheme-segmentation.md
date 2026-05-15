# Grapheme Segmentation

This guide covers practical patterns for segmenting text using `Graphemizer`.

## Segment a Single String

The most basic use case is passing a string to `Graphemizer` and accessing the `.graphemes` property to get a list of the visual clusters.

```python
from graphemes_plusplus import Graphemizer

g = Graphemizer("வணக்கம்")
print(g.graphemes)
# Output: ['வ', 'ண', 'க்', 'க', 'ம்']
```

## Count Graphemes Accurately

When checking the length of an Indic text string, the built-in `len()` function will often return an inflated number because it counts code points. You can pass the `Graphemizer` object directly to `len()` for an accurate count.

```python
from graphemes_plusplus import Graphemizer

text = "ஸ்ரீ"

print(len(text))
# Output: 4 (Inaccurate visual count)

g = Graphemizer(text)
print(len(g))
# Output: 1 (Accurate visual count)
```

## Iterate Over Graphemes

The `Graphemizer` instance acts as an iterator. You can easily loop through the graphemes using a standard `for` loop.

```python
from graphemes_plusplus import Graphemizer

g = Graphemizer("සිංහල")

for char in g:
    print(char)

# Output:
# සි
# ං
# හ
# ල
```

## Handle Mixed-Script Text

`Graphemizer` is robust enough to handle strings containing multiple scripts seamlessly. Punctuation, spaces, and English characters are passed through correctly without breaking the Indic segmentation logic.

```python
from graphemes_plusplus import Graphemizer

text = "Hello வணக்கம், world!"
g = Graphemizer(text)

print(g.graphemes)
# Output: ['H', 'e', 'l', 'l', 'o', ' ', 'வ', 'ண', 'க்', 'க', 'ம்', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!']
```

## Batch Process Multiple Strings

If you have a list of sentences (e.g., from a dataset), you can use a list comprehension to process them all.

```python
from graphemes_plusplus import Graphemizer

corpus = [
    "வணக்கம்",
    "සිංහල",
    "ஸ்ரீ"
]

segmented_corpus = [Graphemizer(sentence).graphemes for sentence in corpus]

print(segmented_corpus)
# Output: [['வ', 'ண', 'க்', 'க', 'ம்'], ['සි', 'ං', 'හ', 'ල'], ['ஸ்ரீ']]
```

!!! tip "Performance Tip"
    Instantiating `Graphemizer` multiple times in a tight loop is generally fast enough for most workloads. However, if you are processing massive datasets with millions of lines, you might want to instantiate the underlying `Normalizer` and `GraphemeSplitter` classes manually to avoid object creation overhead. Note that these are internal utility classes, so their APIs may change in future versions.
