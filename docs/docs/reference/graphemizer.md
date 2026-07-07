# Graphemizer

> The core class for segmenting Indic text strings into visual grapheme clusters.

## Import

```python
from grapheme_kit import Graphemizer
```

## API

### `Graphemizer(string: str)`

<div class="api-signature">
class Graphemizer(string: str)
</div>

The constructor takes a raw text string, normalizes it, and splits it into graphemes. The processing happens immediately upon instantiation.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `string` | `str` | The raw input text to segment. |

**Properties**:

- **`graphemes`** (`list[str]`): A list containing the segmented grapheme clusters.
- **`raw_string`** (`str`): The original unmodified string passed to the constructor.

**Dunder Methods**:

- **`__iter__`**: Allows iterating directly over the graphemes.
- **`__len__`**: Returns the count of visual graphemes (accurate length).

!!! info "Internal Pipeline"
    When you instantiate a `Graphemizer`, the text is first passed through an internal `Normalizer` (which fixes vowel marker orders and applies Unicode NFC), and then through a `GraphemeSplitter` (which applies look-ahead rules for conjuncts and ZWJ). You do not need to call these utilities manually.

**Example**:

```python
from grapheme_kit import Graphemizer

# Tamil conjunct and space
g_tamil = Graphemizer("ஸ்ரீ மதி")
print(g_tamil.graphemes)
# Output: ['ஸ்ரீ', ' ', 'ம', 'தி']

# Sinhala ZWJ sequence
g_sinhala = Graphemizer("ක්‍රමය")
print(g_sinhala.graphemes)
# Output: ['ක්‍ර', 'ම', 'ය']

# Edge case: Empty string
g_empty = Graphemizer("")
print(g_empty.graphemes)
# Output: []
print(len(g_empty))
# Output: 0
```
