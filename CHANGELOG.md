# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-07-07

### Added

#### Grapheme Segmentation Engine
- Introduced `Graphemizer` class for splitting text into correct visual units (grapheme clusters).
- Developed a lookup-based and rule-based pipeline combining standard Unicode segmentation with custom script-specific lookahead rules:
  - **Tamil Conjunct Merging**: Keeps complex multi-codepoint conjuncts (such as `ஸ்ரீ`, `ஶ்ரீ`, and `க்ஷ`) unified as single visual clusters.
  - **Sinhala ZWJ Sequence Preservation**: Correctly handles Zero-Width Joiner (ZWJ, `U+200D`) ligatures (such as `ක්‍ර`), ensuring they are not split.

#### String Distance Metrics
- Implemented a suite of grapheme-aware edit distance algorithms under `grapheme_kit.distance`:
  - **Levenshtein Distance (`levenshtein`)**: Calculates the minimum insertion, deletion, and substitution operations at the grapheme level.
  - **Damerau-Levenshtein Distance (`damerau_levenshtein`)**: Extends Levenshtein to support adjacent grapheme transpositions as a single edit.
  - **Hamming Distance (`hamming`)**: Compares graphemes at matching positions, supporting differing string lengths by counting excess characters as mismatches.
  - **Jaro Similarity (`jaro`)**: Measures the similarity of two strings based on matching graphemes and transpositions within a dynamic proximity window.
  - **Jaro-Winkler Similarity (`jaro_winkler`)**: Applies a prefix scale bonus to Jaro similarity for matching leading graphemes.
  - **Longest Common Subsequence (`longest_common_subsequence`)**: Computes the length of the longest subsequence of common graphemes.

#### Evaluation Metrics (NLP/MT)
- Implemented grapheme-boundary evaluation metrics for machine translation and generation under `grapheme_kit.metric`:
  - **`GraphemeCHRF`**: Subclasses `sacrebleu.metrics.CHRF`. Tokenizes hypothesis and reference texts into graphemes prior to n-gram extraction. Supports standard chrF and chrF++ (by setting `word_order` to capture word n-grams).
  - **`CER` (Character Error Rate)**: Computes the edit distance divided by the total number of reference grapheme clusters.
  - **`charbleu`**: Evaluates BLEU precision over grapheme n-gram matching, applying a brevity penalty based on grapheme count.

#### Phonetic Decomposition & Composition
- Added phonetic utilities for script-level analysis:
  - **`decompose`**: Breaks down complex Indic graphemes (Tamil and Sinhala) into a base consonant (carrying a virama/hal) and its independent base vowel (e.g., `கா` -> `க்` + `ஆ`).
  - **`compose`**: Reconstructs decomposed consonant-vowel sequences back into standard Unicode glyphs.

#### Normalization & Fixups
- Implemented a text `Normalizer` in `grapheme_kit.utils.normalizer`:
  - Enforces Unicode Normalization Form C (NFC).
  - Automatically fixes common typing/ordering bugs in complex scripts (such as misplaced Tamil combining vowel symbols).

#### Command-Line Interface
- Introduced a console application supporting `grapheme-kit` and `gkit` executables.
- Exposes all core features through dedicated subcommands:
  - `graphemize`: Splits text and prints grapheme counts, code point counts, and indexes.
  - `distance`: Computes Levenshtein/Hamming distances at both the grapheme and code-point levels side-by-side.
  - `evaluate`: Runs chrF, chrF++, and CER on sentences or files.
  - `decompose` / `compose`: Performs phonetic translation.
  - `normalize`: Standardizes input text or whole files.
- Supports streaming from stdin, reading/writing files, and generating machine-readable JSON output via `--format json`.

#### Test Suite
- Designed a comprehensive unit testing framework with 152 test cases, covering:
  - Edge cases (empty strings, ASCII-only text, mixed-script inputs).
  - Correctness of distance algorithms against standard reference cases.
  - Verification of Tamil conjunct lookahead and Sinhala ZWJ logic using pre-compiled grapheme tables.
