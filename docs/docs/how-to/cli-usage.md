# Command Line Usage

Installing `graphemes_plusplus` also installs a `gpp` command (long form: `graphemes-plusplus` -- both run the exact same code). Every command reads a positional `TEXT` argument, `--input FILE`, or stdin, and writes to stdout (or `--output FILE`) as text or, with `--format json`, machine-readable JSON.

## graphemize -- segment text

```bash
gpp graphemize "ஸ்ரீ வணக்கம்" --count
```

**Output:**
```
graphemes:   7
code points: 12

ஸ்ரீ
 
வ
ண
க்
க
ம்
```

`--count` also prints the code-point count alongside the grapheme count, for a quick before/after comparison. `--codepoints` additionally lists the raw code points. `--format json` returns `{text, graphemes, count, codepoints, codepoint_count}`.

## decompose / compose -- Tamil & Sinhala phonetic canonicalization

```bash
gpp decompose "ශ්‍රී" --round-trip
```

**Output:**
```
ශ්ර්ඊ

recomposed: ශ්‍රී
round-trip: OK
```

`--round-trip` recomposes the decomposed output and reports whether it matches the original. `gpp compose` reverses a decomposed string back into grapheme clusters.

## distance -- grapheme-aware edit distance

```bash
gpp distance "ஸ்ரீ" "ஸ்ரி" --measure levenshtein --level both
```

**Output:**
```
levenshtein (grapheme): 2
levenshtein (codepoint): 1
```

`--measure` selects `levenshtein` (default) or `hamming` (`hamming` requires equal grapheme/code-point counts between the two inputs and raises a CLI error otherwise). `--level` selects `grapheme` (default), `codepoint`, or `both` -- `both` prints the grapheme-level and code-point-level numbers side by side, which is the clearest way to *show* the divergence this whole library is about.

## evaluate -- grapheme-aware chrF / chrF++ / CER

```bash
gpp evaluate "நல்ல மாணவன்" "நல்ல" --metric chrf
```

**Output:**
```
chrF (grapheme): 37.1051
```

`--metric` selects `chrf`, `chrf++`, `cer`, or `all` (default). `--level` works the same as `distance` (`grapheme` / `codepoint` / `both`). Corpus mode: pass `--reference-file FILE --hypothesis-file FILE` (one sentence per line) instead of the positional strings, to score an entire dataset at once.

## normalize -- NFC + script-specific typing fixups

```bash
gpp normalize "ொ"
```

Applies the same Tamil/Sinhala vowel-reordering and NFC normalization that `Graphemizer` runs internally, without segmenting. Useful for cleaning a dataset before further processing. `--input FILE --output FILE` streams a whole file through normalization.

## Every command supports

- `-f, --format {text,json}` -- machine-readable output for piping into other tools.
- `-o, --output FILE` -- write to a file instead of stdout.
- Reading input from a positional argument, `-i/--input FILE`, or stdin (so `cat file.txt | gpp graphemize` works).

Run `gpp --help` or `gpp <command> --help` for the complete, current list of flags.
