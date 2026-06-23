# Graphemizer

## Why It Exists

Graphemes are the basic units of a writing system. In complex scripts like Tamil and Sinhala, multiple Unicode characters combine to form a single grapheme. `Graphemizer` breaks text into these meaningful units correctly.

**Example:** "ஸ்ரீ" appears as 3 characters but is 1 grapheme.

## How It Works

```
Raw Text  →  Normalize (Unicode fix + script-specific rules)  →  Split into Graphemes
```

The class:
1. **Normalizes** the text (Unicode NFC + Tamil/Sinhala fixups)
2. **Splits** into grapheme clusters (handles complex conjuncts like "க்ஷ")
3. **Returns** a list of graphemes

## Usage Examples

### Basic Usage

```python
from graphemes_plusplus import Graphemizer

g = Graphemizer("ஸ்ரீ மதி")
print(g.graphemes)  # ['ஸ்ரீ', ' ', 'ம', 'தி']
```

### Iteration

```python
g = Graphemizer("தமிழ்")
for grapheme in g:
    print(grapheme)
```

### Get Length

```python
g = Graphemizer("ஸ்ரீ")
print(len(g))  # 1
```

### Sinhala Text

```python
g = Graphemizer("ශ්‍රී ලංකාවේ")
print(g.graphemes)  # Properly handles ZWJ sequences
```

## API Reference

### Constructor

```python
Graphemizer(string: str)
```

Creates a new instance and immediately processes the text.

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `graphemes` | `list[str]` | Returns processed grapheme list |
| `raw_string` | `str` | Original unprocessed input |

### Methods

| Method | Description |
|--------|-------------|
| `__len__()` | Returns number of graphemes |
| `__iter__()` | Enables iteration over graphemes |

## More Examples

### Compare Grapheme Count

```python
# Character count vs Grapheme count
text = "ஸ்ரீ"
print(len(text))              # 3 (characters)
print(len(Graphemizer(text)))  # 1 (grapheme)
```

### Process Multiple Strings

```python
texts = ["தமிழ்", "ஸ்ரீ", "மதி"]
for text in texts:
    g = Graphemizer(text)
    print(f"{text}: {g.graphemes}")
```

### Check if Text Contains Grapheme

```python
g = Graphemizer("தமிழ் மதி")
if "ம" in g.graphemes:
    print("Found!")
```

### Convert to String with Separators

```python
g = Graphemizer("தமிழ்")
print(" | ".join(g.graphemes))  # த | மி | ழ்
```

## Integration with Other Classes

- **Normalizer**: Handles text normalization internally
- **GraphemeSplitter**: Handles grapheme clustering internally
- **Composer**: Reverse operation - builds text from graphemes
- **Distance**: Calculate differences between graphemized texts

## Common Use Cases

1. **Text Segmentation**: Break text into meaningful units for NLP
2. **String Comparison**: Compare grapheme-by-grapheme instead of character-by-character
3. **Text Metrics**: Count graphemes (not characters) accurately
4. **Spelling Correction**: Work at grapheme level for accuracy
5. **Text Normalization**: Standardize input before processing
