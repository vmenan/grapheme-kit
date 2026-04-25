# Utilities

Internal utility modules that power the `Graphemizer` pipeline. These can also be used directly for fine-grained control.

**Module:** `graphemes_plusplus.utils`

## Normalizer

Handles Unicode standardization and script-specific character fixups.

```python
class Normalizer
```

### `normalize(text: str) → str`

Main normalization entry point. Applies:

1. **Unicode NFC** - Canonical Composition normalization
2. **Tamil fixups** - Corrects common encoding issues:
    - Reversed vowel orders (`ாெ` → `ொ`, `ாே` → `ோ`)
    - Incorrect character sequences (`ா்` → `ர்`)
    - Zero Width Non-Joiner removal
    - Conditional vowel merging (`ெள` → `ௌ`)
3. **Sinhala fixups** - Corrects confusable character combinations:
    - Multiple variant encodings of `ෝ`, `ෞ`, `ෛ`, etc.

```python
>>> from graphemes_plusplus.utils import Normalizer
>>> n = Normalizer()
>>> n.normalize("text with encoding issues")
'corrected text'
```

### `sandhi_remover(word: str) → str`

Removes Tamil sandhi (euphonic) suffixes (`க்`, `த்`, `ப்`, `ச்`) from word endings.

```python
>>> n = Normalizer()
>>> n.sandhi_remover("வந்தான்க்")
'வந்தான்'
```

### Tamil Validation Methods

#### `check_starting_letter(word: str) → bool`

Validates whether a Tamil word starts with a grammatically valid letter according to Nanool rules.

#### `check_ending_letter(word: str) → bool`

Validates whether a Tamil word ends with a grammatically valid letter.

#### `check_meimmayakkam(word: str) → bool`

Validates consonant doubling (meimmayakkam) rules in Tamil grammar.

> **Validation methods**
> These methods implement Tamil grammatical rules from Nanool (நன்னூல்) and can be used for linguistic validation tasks.
>
>
---

## GraphemeSplitter

The core splitting engine that extends the `grapheme` library with Tamil and Sinhala-specific merge rules.

```python
class GraphemeSplitter
```

### `split(string: str) → list[str]`

Splits a string into grapheme clusters with enhanced handling for:

| Case | Input Split | Merged Output |
|---|---|---|
| Tamil க்ஷ | `க்` + `ஷ...` | `க்ஷ...` |
| Tamil ஸ்ரீ | `ஸ்` + `ரீ` | `ஸ்ரீ` |
| Tamil ஶ்ரீ | `ஶ்` + `ரீ` | `ஶ்ரீ` |
| Sinhala ZWJ | Split at ZWJ | Merged across ZWJ |

```python
>>> from graphemes_plusplus.utils import GraphemeSplitter
>>> s = GraphemeSplitter()
>>> s.split("ஸ்ரீலங்கா")
['ஸ்ரீ', 'ல', 'ங்', 'கா']
```

> **Internal use**
> The `GraphemeSplitter` is used internally by `Graphemizer`. You only need to use it directly if you want to skip the normalization step.
>
>
---

## `normalize_file`

Batch file normalization utility.

```python
normalize_file(input_path: str, output_path: str | None = None) → str
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `input_path` | `str` | *(required)* | Path to the input text file |
| `output_path" | `str \| None` | `None` | Output file path. If `None`, generates `<input>_normalized.<ext>` |
| **Returns** | `str` | | Path to the output file |

```python
>>> from graphemes_plusplus.utils import normalize_file
>>> normalize_file("data/input.txt")
'data/input_normalized.txt'

>>> normalize_file("data/input.txt", "data/clean.txt")
'data/clean.txt'
```

## See Also

- [Graphemizer](graphemizer.md) - Uses `Normalizer` and `GraphemeSplitter` internally
