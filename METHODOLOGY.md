# Methodology

## Architecture Overview

The Graphemes++ library is built on a modular architecture with the following processing pipeline:

```
Raw Text Input → Normalization → Grapheme Segmentation → Analysis Operations
                                                              ↓
                                            Composition/Decomposition
                                            Distance Metrics
                                            Evaluation Metrics (CHRF)
```

## System Components

### Normalization Module

#### Purpose
The normalization module ensures consistent text representation by addressing Unicode inconsistencies and language-specific character variations before grapheme segmentation.

#### Methodology

**Step 1: Unicode NFC Normalization**
- Applies Unicode Normalization Form C (Canonical Composition)
- Converts decomposed characters (e.g., base character + combining mark) into their canonical composed forms
- Ensures consistent representation of visually identical characters

```
Input:  ු + ්  (separate code points)
Output: ු් (composed form)
```

**Step 2: Language-Specific Fixups**

**Tamil-Specific Normalization:**
- Character substitution corrections:
  - Standardizes variant representations of characters like 'ோ' (U+0BCB) and 'ொ' (U+0BCA)
  - Fixes malformed sequences such as 'ா्' → 'ர्'
- Reverse vowel order correction:
  - Converts reversed vowel combinations (e.g., 'ാെ' → 'ொ', 'ാേ' → 'ோ')
- Zero-width character removal:
  - Removes Zero-Width Non-Joiner (ZWNJ) characters that may cause segmentation issues
- Contextual character merging:
  - Applies conditional rules for combining dependent vowels, such as 'ெள' → 'ௌ' when not followed by additional vowel markers

**Sinhala-Specific Normalization:**
- Confusion set resolution for visually similar character sequences
- Handles Zero-Width Joiner (ZWJ) sequences used in complex consonant clusters
- Resolves ambiguous vowel modifier combinations

#### Algorithm Pseudocode
```
FUNCTION normalize(text):
    // Step 1: Unicode NFC Normalization
    text ← unicodedata.normalize('NFC', text)
    
    // Step 2: Apply language-specific fixups
    IF text contains Tamil characters:
        text ← apply_tamil_fixups(text)
    ELSE IF text contains Sinhala characters:
        text ← apply_sinhala_fixups(text)
    
    RETURN text
```

### Grapheme Segmentation Module

#### Purpose
Segments normalized text into linguistically meaningful units called grapheme clusters. A grapheme cluster represents a single visual character unit in the script system.

#### Grapheme Definition

For Tamil and Sinhala scripts, a grapheme cluster consists of:
- **Base Consonant** (க், ක්): The root consonant character
- **Vowel Modifier** (ு, ි): Dependent vowel indicating the inherent vowel quality
- **Combining Marks** (Zero-Width Joiner, diacritics): Additional modifiers affecting pronunciation or appearance

#### Segmentation Rules

**Tamil Grapheme Composition:**
- Sequences of consonant + virama (्) + dependent vowel mark are recognized as single graphemes
- Examples:
  - 'ஸ್ரீ' → grapheme cluster
  - 'ம' + 'தி' → two graphemes
  - Space and punctuation are isolated as individual graphemes

**Sinhala Grapheme Composition:**
- Base consonant + vowel modifier combinations form grapheme units
- Zero-Width Joiner (ZWJ) sequences create complex consonant clusters:
  - 'ක්ව්' (ka + virama + va + virama) → treated as a single grapheme
  - 'ර්‍ය' (ra + virama + ZWJ + ya) → ZWJ-based conjunct
- Unicode range detection:
  - Sinhala: U+0D80 to U+0DFF
  - Tamil: U+0B80 to U+0BFF

#### Algorithm Pseudocode
```
FUNCTION split_graphemes(normalized_text):
    graphemes ← []
    i ← 0
    
    WHILE i < length(normalized_text):
        current_char ← normalized_text[i]
        
        // Collect base consonant
        IF is_consonant(current_char):
            grapheme ← current_char
            i ← i + 1
            
            // Collect virama (halant)
            IF i < length(normalized_text) AND is_virama(normalized_text[i]):
                grapheme ← grapheme + normalized_text[i]
                i ← i + 1
            
            // Collect ZWJ and subsequent characters
            WHILE i < length(normalized_text) AND 
                  (is_ZWJ(normalized_text[i]) OR is_combining_mark(normalized_text[i])):
                grapheme ← grapheme + normalized_text[i]
                i ← i + 1
            
            // Collect dependent vowel mark
            IF i < length(normalized_text) AND is_vowel_mark(normalized_text[i]):
                grapheme ← grapheme + normalized_text[i]
                i ← i + 1
            
            graphemes.append(grapheme)
        ELSE IF is_vowel(current_char):
            graphemes.append(current_char)
            i ← i + 1
        ELSE:
            // Whitespace, punctuation
            graphemes.append(current_char)
            i ← i + 1
    
    RETURN graphemes
```

### Character Composition Module

#### Purpose
The Composer module reconstructs full grapheme clusters from decomposed linguistic components (base consonant and vowel mark).

#### Composition Rules

**Tamil Character Composition:**
- **Input:** Consonant with virama (mei) + Vowel (uyir)
- **Process:**
  - Validates input consonant ends with virama (्)
  - Looks up dependent vowel mark corresponding to input vowel
  - Combines base consonant with appropriate vowel marker

```
Example:
Input:  mei = 'ம्', uyir = 'ி' (vowel)
Output: 'மி'
```

**Sinhala Character Composition:**
- **Input:** Base consonant (with or without virama) + Vowel
- **Process:**
  - Validates vowel is in Sinhala vowel set
  - Removes trailing virama from base if present
  - Appends corresponding vowel modifier or returns bare base for 'අ'

```
Example:
Input:  base = 'ක්', vowel = 'ි'
Output: 'කි'
```

#### Language Detection
```
FUNCTION _is_tamil(chars):
    RETURN all character in chars: '\u0B80' ≤ char ≤ '\u0BFF'

FUNCTION _is_sinhala(chars):
    RETURN all character in chars: '\u0D80' ≤ char ≤ '\u0DFF' OR char == '\u200D'
```

### Character Decomposition Module

#### Purpose
The Decomposer module breaks down grapheme clusters into their constituent linguistic components (base consonant and vowel modifier), reversing the composition process.

#### Decomposition Rules

**Sinhala Character Decomposition:**
- **Independent Vowels:** Kept as-is, paired with empty string
  ```
  'අ' → ['අ', '']
  'ආ' → ['ආ', 'ආ']
  ```

- **Consonant + Single Combining Mark:**
  ```
  'කි' → ['ක්', 'ි']
  ```

- **ZWJ-based Conjuncts:** Recursively decompose after ZWJ marker
  ```
  'ක්‍රම' → ['ක්'] + decompose('ර + ම')
  ```

**Tamil Character Decomposition:**
- Inverse of composition: extracts base consonant (with virama) and vowel marker
- Returns list of base + vowel pairs

#### Algorithm Pseudocode
```
FUNCTION _decompose_sinhala_character(char):
    base_char ← '්'  // virama
    
    IF char IN SINHALA_VOWELS:
        RETURN [char, ""]
    
    IF length(char) == 1:
        RETURN [char + base_char, SINHALA_VOWELS[0]]  // 'අ'
    ELSE IF length(char) == 2 AND char[1] IN SINHALA_ACCENT_SYMBOLS:
        index ← find_index(char[1], SINHALA_ACCENT_SYMBOLS)
        RETURN [char[0] + base_char, SINHALA_VOWELS[index]]
    ELSE IF '\u200D' IN char:  // ZWJ
        zwj_pos ← find_position('\u200D', char)
        new_char ← char[zwj_pos + 1:]
        RETURN [char[0] + base_char] + _decompose_sinhala_character(new_char)
    ELSE:
        RETURN [char]
```

### Distance Metrics Module

#### Grapheme-Aware Levenshtein Distance

**Purpose:** Measure edit distance between two strings at the grapheme level, not character level.

**Algorithm:**
1. Segment both input strings into grapheme clusters using Graphemizer
2. Treat each grapheme as an atomic unit
3. Compute Levenshtein distance on grapheme sequences
4. Operations: insertion, deletion, substitution of a single grapheme

```
Example:
s1 = 'ஸ்ரீ' → ['ஸ்ரீ']  (1 grapheme)
s2 = 'ஸ்ரி' → ['ஸ்ரி']  (1 grapheme)
Distance = 1 (substitution of 'ீ' with 'ி')
```

**Algorithm Pseudocode:**
```
FUNCTION levenshtein(s1, s2):
    graphemes_1 ← Graphemizer(s1).graphemes
    graphemes_2 ← Graphemizer(s2).graphemes
    
    RETURN textdistance.levenshtein.distance(graphemes_1, graphemes_2)
```

#### Grapheme-Aware Hamming Distance

**Purpose:** Measure difference between strings of equal grapheme length.

**Requirements:**
- Both strings must segment into equal number of graphemes
- Counts position-by-position differences

**Algorithm Pseudocode:**
```
FUNCTION hamming(s1, s2):
    graphemes_1 ← Graphemizer(s1).graphemes
    graphemes_2 ← Graphemizer(s2).graphemes
    
    IF length(graphemes_1) ≠ length(graphemes_2):
        RAISE ValueError("Strings must have equal number of graphemes")
    
    RETURN textdistance.hamming.distance(graphemes_1, graphemes_2)
```

### Evaluation Metrics Module

#### Grapheme-Level CHRF Metric

**Purpose:** Extends the sacrebleu CHRF (Character n-gram F-score) metric to operate at the grapheme level for proper evaluation of sequence-to-sequence models on Indic scripts.

**Motivation:**
- Standard CHRF operates on Unicode code points
- For complex scripts, this produces misleading scores because visual characters span multiple code points
- Grapheme-level CHRF provides linguistically meaningful evaluation

#### CHRF Calculation Process

**Step 1: Graphemization**
```
hypothesis_text → Graphemizer → grapheme_sequence_1
reference_text → Graphemizer → grapheme_sequence_2
```

**Step 2: N-gram Extraction**
- For each n from 1 to max_order:
  - Extract all n-grams from both sequences
  - Count occurrence frequency

```
graphemes = ['ஸ்ரீ', ' ', 'ம', 'தி']
max_order = 2

1-grams: [('ஸ்ரீ',), (' ',), ('ம',), ('தி',)]
2-grams: [('ஸ்ரீ', ' '), (' ', 'ம'), ('ம', 'தி')]
```

**Step 3: Precision and Recall Calculation**
- Count matching n-grams between hypothesis and reference
- Precision = matching n-grams / total n-grams in hypothesis
- Recall = matching n-grams / total n-grams in reference

**Step 4: F-score Computation**
- Weighted average of precisions and recalls across n-gram orders:
$$\text{CHRF} = \frac{1}{n} \sum_{i=1}^{n} \text{F}_i$$

where $\text{F}_i$ is the F-score for n-gram order $i$

#### Algorithm Pseudocode
```
FUNCTION extract_all_grapheme_ngrams(graphemes, max_order, include_whitespace):
    counters ← []
    
    IF NOT include_whitespace:
        graphemes ← [g for g in graphemes if g.strip() ≠ ""]
    
    FOR n FROM 1 TO max_order:
        ngrams ← Counter()
        FOR i FROM 0 TO length(graphemes) - n:
            ngram ← tuple(graphemes[i:i+n])
            ngrams[ngram] ← ngrams[ngram] + 1
        counters.append(ngrams)
    
    RETURN counters

CLASS GraphemeCHRF:
    FUNCTION _graphemize(text):
        RETURN list(Graphemizer(text))
    
    FUNCTION score(hypothesis, reference):
        hyp_ngrams ← extract_all_grapheme_ngrams(
            _graphemize(hypothesis), 
            max_order, 
            include_whitespace)
        
        ref_ngrams ← extract_all_grapheme_ngrams(
            _graphemize(reference), 
            max_order, 
            include_whitespace)
        
        RETURN compute_chrf_from_ngrams(hyp_ngrams, ref_ngrams)
```

## Processing Pipeline

### Main Graphemizer Class

The `Graphemizer` class orchestrates the entire normalization and segmentation pipeline:

```
FUNCTION __init__(string):
    normalizer ← Normalizer()
    splitter ← GraphemeSplitter()
    raw_string ← string
    _graphemes ← _process_text(string)

FUNCTION _process_text(raw_text):
    // Step 1: Normalize
    normalized_text ← normalizer.normalize(raw_text)
    
    // Step 2: Split into Graphemes
    graphemes ← splitter.split(normalized_text)
    
    RETURN graphemes
```

### Example Processing Flow

**Input:** `"ஸ்ரீ மதி"`

**Step 1 - Normalization:**
```
Input:  ஸ்ரீ மதி
Output: ஸ்ரீ மதி (after NFC and Tamil-specific fixes)
```

**Step 2 - Grapheme Segmentation:**
```
Input:  ஸ்ரீ மதி
Split:  ['ஸ்ரீ', ' ', 'ம', 'தி']
Count:  4 graphemes
```

## Data Structures

### Vowel and Accent Symbol Mappings

**Tamil System:**
```
VOWELS:          ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
ACCENT_SYMBOLS:  ["", "ா", "ி", "ீ", "ु", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]
```

**Sinhala System:**
```
VOWELS:           ['අ', 'ආ', 'ඇ', 'ඈ', 'ඉ', ..., 'අං', 'අඃ']
ACCENT_SYMBOLS:   ['', 'ා', 'ැ', 'ෑ', 'ි', 'ී ', 'ු', 'ූ', 'ෘ', ...]
ZWJ_CHARS:        ['ක්ව්', 'ක්ෂ්', 'ග්ධ්', ...]
```

## Technical Specifications

### Language Support

| Language | Unicode Range | Special Features |
|----------|--------------|-----------------|
| Tamil | U+0B80 - U+0BFF | Dependent vowels, virama combinations |
| Sinhala | U+0D80 - U+0DFF | ZWJ-based conjuncts, complex vowels |

### Character Categories

- **Base Consonants:** Fundamental sound units
- **Vowels:** Independent vowels standing alone
- **Dependent Vowel Marks:** Modifiers indicating inherent vowel
- **Virama (Halant):** Indicates consonant cluster formation
- **Zero-Width Joiner (ZWJ):** Connects consonants in clusters
- **Combining Marks:** Diacritics and additional modifiers

### Unicode Normalization Forms

- **NFC (Canonical Composition):** Default normalization form used
- **Properties:** Combines related characters (e.g., base + combining accent)
- **Idempotent:** Applying NFC multiple times produces same result


