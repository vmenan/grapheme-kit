# Decomposer

> Handles the decomposition of Sinhala and Tamil strings into fundamental phonetic sequences.

## Import

```python
from grapheme_kit import decompose
from grapheme_kit.decomposer import Decomposer
```

## API

### `decompose(text: str) -> str`

<div class="api-signature">
def decompose(text: str) -> str
</div>

A convenience module-level function that wraps `Decomposer.decompose()`. It breaks down clusters into base consonants with hal/virama, followed by the base vowel. Punctuations and spaces are unaffected.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `text` | `str` | The input text to decompose. |

**Returns**: A `str` representing the decomposed phonetic sequence.

**Example**:

```python
from grapheme_kit import decompose

print(decompose("கொண்டு"))
# Output: க்ஒண்ட்உ

print(decompose("සිංහල"))
# Output: ස්ඉංහ්අල්අ

print(decompose("Hello! வணக்கம்"))
# Output: Hello! வ்அண்அக்க்அம்
```

---

### `Decomposer.decompose(text: str) -> str`

<div class="api-signature">
@classmethod<br>
def decompose(cls, text: str) -> str
</div>

The class method that performs the underlying decomposition logic.

**Parameters**: Same as the module-level function.

**Returns**: Same as the module-level function.

---

### Class Constants

The `Decomposer` class uses several internal constants mapping vowels to their corresponding accent symbols. These can be useful for reference.

#### Tamil
- **`TAMIL_VOWELS`**: `["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]`
- **`TAMIL_ACCENT_SYMBOLS`**: `["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]`

#### Sinhala
- **`SINHALA_VOWELS`**: `['අ', 'ආ', 'ඇ', 'ඈ', 'ඉ', 'ඊ', 'උ', 'ඌ', 'ඍ', 'ඎ', 'එ', 'ඒ', 'ඓ', 'ඔ', 'ඕ', 'ඖ', 'අං', 'අඃ']`
- **`SINHALA_ACCENT_SYMBOLS`**: `['', 'ා', 'ැ', 'ෑ', 'ි', 'ී', 'ු', 'ූ', 'ෘ', 'ෲ', 'ෙ', 'ේ', 'ෛ', 'ො', 'ෝ', 'ෞ', 'ං', 'ඃ']`
- **`ZWJ_CHARS`**: `['ක්ව්', 'ක්ෂ්', 'ග්ධ්', 'ට්ඨ්', 'ත්ව්', 'ත්ථ්', 'ද්ධ්', 'න්ථ්', 'න්ද්', 'න්ධ්', 'ර්', 'ය්']`
