# Decomposer

The `Decomposer` class handles grapheme decomposition and composition for Sinhala and Tamil text. It encapsulates language-specific phonetic rules, enabling character-level transformations needed for NLP tokenization and metric evaluation.

## Class Definition

```python
class Decomposer
```

**Module:** `graphemes_plusplus.decomposer`

All methods are `@classmethod` — no instantiation required.

## Functions

### `decompose(text: str) → str`

Decomposes Tamil and Sinhala strings into fundamental phonetic sequences. Punctuation and spaces are unaffected.

```python
decompose(text: str) → str
```

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Input text containing Tamil or Sinhala characters |
| **Returns** | `str` | Decomposed phonetic sequence |

```python
>>> from graphemes_plusplus import decompose
>>> decompose("கா")
'க்ஆ'  # consonant base + vowel
```

### `compose(text: str) → str`

Composes a decomposed sequence back into standard grapheme clusters.

```python
compose(text: str) → str
```

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Decomposed phonetic sequence |
| **Returns** | `str` | Recomposed standard text |

```python
>>> from graphemes_plusplus import compose
>>> compose("க்ஆ")
'கா'
```

## How Decomposition Works

### Tamil

Each Tamil grapheme is split into a **mei** (consonant base + pulli) and an **uyir** (vowel):

| Input | → | Mei | Uyir |
|---|---|---|---|
| க | → | க் | அ |
| கா | → | க் | ஆ |
| கி | → | க் | இ |
| கு | → | க் | உ |

### Sinhala

Sinhala graphemes follow a similar pattern with consonant base + hal + vowel:

| Input | → | Base | Vowel |
|---|---|---|---|
| ක | → | ක් | අ |
| කා | → | ක් | ආ |
| කැ | → | ක් | ඇ |

## Language Detection

The `Decomposer` automatically detects the script using Unicode ranges:

| Script | Unicode Range |
|---|---|
| Tamil | `U+0B80` – `U+0BFF` |
| Sinhala | `U+0D80` – `U+0DFF` |

> **Mixed scripts**
> Non-Tamil and non-Sinhala characters (English, punctuation, numbers) pass through unchanged during decomposition.
>
>
## Class Constants

### Tamil Constants

- **`TAMIL_VOWELS`** — 12 Tamil vowels (உயிர் எழுத்துக்கள்): அ, ஆ, இ, ஈ, உ, ஊ, எ, ஏ, ஐ, ஒ, ஓ, ஔ
- **`TAMIL_ACCENT_SYMBOLS`** — 12 Tamil vowel diacritics: (empty), ா, ி, ீ, ு, ூ, ெ, ே, ை, ொ, ோ, ௌ

### Sinhala Constants

- **`SINHALA_VOWELS`** — 18 Sinhala vowels: අ, ආ, ඇ, ඈ, ඉ, ඊ, උ, ඌ, ...
- **`SINHALA_ACCENT_SYMBOLS`** — 18 Sinhala vowel diacritics
- **`ZWJ_CHARS`** — Zero Width Joiner character combinations specific to Sinhala

## See Also

- [Graphemizer](graphemizer.md) — Used internally for initial segmentation
- [Distance](distance.md) — Uses decomposition for distance computation
