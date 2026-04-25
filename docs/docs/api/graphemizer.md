# Graphemizer

The `Graphemizer` class is the core entry point of `graphemes++`. It takes raw text, applies normalization, and segments it into linguistically correct grapheme clusters.

## Class Definition

```python
class Graphemizer(string: str)
```

**Module:** `graphemes_plusplus.graphemizer`

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `string` | `str` | The input text to segment into graphemes |

### Properties

| Property | Type | Description |
|---|---|---|
| `graphemes` | `list[str]` | The list of segmented grapheme clusters |
| `raw_string` | `str` | The original input string (before normalization) |

### Methods

#### `__len__() → int`

Returns the number of grapheme clusters.

```python
>>> g = Graphemizer("ஸ்ரீ மதி")
>>> len(g)
4
```

#### `__iter__()`

Makes the `Graphemizer` instance iterable over its grapheme clusters.

```python
>>> g = Graphemizer("ஸ்ரீ மதி")
>>> for grapheme in g:
...     print(grapheme)
ஸ்ரீ
 
ம
தி
```

## Processing Pipeline

The `Graphemizer` follows a two-stage pipeline:

```mermaid
graph LR
    A[Raw Text] --> B[Normalizer]
    B --> C[GraphemeSplitter]
    C --> D[List of Graphemes]
    
    style A fill:#7c4dff,color:#fff
    style D fill:#00bfa5,color:#fff
```

1. **Normalize** - Unicode NFC normalization + Tamil/Sinhala-specific character fixups
2. **Split** - Extended grapheme clustering that handles conjuncts and ZWJ sequences

## Examples

### Tamil Segmentation

```python
>>> g = Graphemizer("கொண்டுவந்து")
>>> g.graphemes
['கொ', 'ண்', 'டு', 'வ', 'ந்', 'து']
```

### Sinhala Segmentation

```python
>>> g = Graphemizer("ක්‍රිකට්")
>>> g.graphemes
['ක්‍රි', 'ක', 'ට්']
```

### Mixed Script

```python
>>> g = Graphemizer("Hello வணக்கம்!")
>>> g.graphemes
['H', 'e', 'l', 'l', 'o', ' ', 'வ', 'ண', 'க்', 'க', 'ம்', '!']
```

> **Normalization is automatic**
> The `Graphemizer` automatically normalizes input text before segmentation. You don't need to pre-process your text unless you want explicit control over the normalization step.
>
>
## See Also

- [Decomposer](decomposer.md) - Decompose graphemes into phonetic sequences
- [Composer](composer.md) - Recompose standard graphemes from phonetic sequences
- [Distance Functions](distance.md) - Use graphemes for distance computation
- [Evaluation Metrics](metric.md) - Metrics for NLP evaluation using graphemes
