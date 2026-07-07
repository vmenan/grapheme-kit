# Composer

> Handles the composition of decomposed phonetic sequences back into standard grapheme clusters.

## Import

```python
from grapheme_kit import compose
from grapheme_kit.composer import Composer
```

## API

### `compose(text: str) -> str`

<div class="api-signature">
def compose(text: str) -> str
</div>

A convenience module-level function that wraps `Composer.compose()`. It recomposes a sequence of base consonants and vowels back into properly rendered visual clusters.

**Parameters**:

| Name | Type | Description |
| --- | --- | --- |
| `text` | `str` | The decomposed input text to compose. |

**Returns**: A `str` representing the composed grapheme sequence.

**Example**:

```python
from grapheme_kit import decompose, compose

# Recomposing a decomposed Tamil string
print(compose("க்ஒண்ட்உ"))
# Output: கொண்டு

# Round-trip example
text = "සිංහල"
decomposed = decompose(text)
composed = compose(decomposed)

assert text == composed
```

---

### `Composer.compose(text: str) -> str`

<div class="api-signature">
@classmethod<br>
def compose(cls, text: str) -> str
</div>

The class method that performs the underlying composition logic. It iterates through the decomposed string, matches consonant-vowel pairs, and applies the necessary accent symbols or ZWJ sequences.

**Parameters**: Same as the module-level function.

**Returns**: Same as the module-level function.

**Raises**: 
- `ValueError`: If an invalid base consonant or vowel is encountered during composition that violates the script's phonetic rules.
