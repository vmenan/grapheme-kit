"""Thin service layer over the ``grapheme_kit`` library.

This module is the *single* boundary between the web API and the library.
Every number the website shows is produced here by calling the real library
(and ``sacrebleu``/``textdistance`` for the code-point baselines), so the
demo is paper-grade.
"""

from __future__ import annotations

from functools import lru_cache

import textdistance
from sacrebleu.metrics import CHRF as StdCHRF

from grapheme_kit import Graphemizer, compose, decompose, hamming, levenshtein
from grapheme_kit.distance import damerau_levenshtein, jaro, jaro_winkler, longest_common_subsequence
from grapheme_kit.metric import CER, GraphemeCHRF, charbleu

# --- Reusable metric instances ------------------------------------------------
# Grapheme-aware (our library) vs. standard code-point (sacrebleu) baselines.
_g_chrf = GraphemeCHRF()
_g_chrf_pp = GraphemeCHRF(word_order=2)
_std_chrf = StdCHRF()
_std_chrf_pp = StdCHRF(word_order=2)


def _round(value: float, ndigits: int = 4) -> float:
    return round(float(value), ndigits)


def _codepoint_cer(hypothesis: str, reference: str) -> float:
    """Code-point-level CER baseline (raw Unicode edit distance / reference
    code-point count), to contrast with the library's grapheme-aware CER."""
    if len(reference) == 0:
        return 0.0 if len(hypothesis) == 0 else 1.0
    return textdistance.levenshtein.distance(hypothesis, reference) / len(reference)


# --- Segmentation -------------------------------------------------------------
def get_graphemes(text: str) -> dict:
    g = Graphemizer(text)
    graphemes = list(g.graphemes)
    return {
        "graphemes": graphemes,
        "count": len(g),
        "codepoints": list(text),
        "codepoint_count": len(text),
    }


# --- Decomposition / composition ---------------------------------------------
def get_decompose(text: str) -> dict:
    decomposed = decompose(text)
    recomposed = compose(decomposed)

    # Group the phonetic units by the original grapheme they came from, so the
    # UI can box "வ் + அ" together as the decomposition of "வ". decompose()
    # processes each grapheme independently, so decomposing one grapheme at a
    # time is consistent with decomposing the whole string.
    source_graphemes = list(Graphemizer(text).graphemes)
    groups = [
        {"source": g, "units": list(Graphemizer(decompose(g)).graphemes)}
        for g in source_graphemes
    ]

    return {
        "input": text,
        "graphemes": source_graphemes,
        "decomposed": decomposed,
        "decomposed_graphemes": list(Graphemizer(decomposed).graphemes),
        "groups": groups,
        "recomposed": recomposed,
        "round_trip_ok": recomposed == text,
    }


def get_compose(text: str) -> dict:
    composed = compose(text)
    composed_graphemes = list(Graphemizer(composed).graphemes)

    # Mirror get_decompose's grouping, in reverse: walk the input's grapheme
    # units and, for each output grapheme, consume however many units its own
    # decomposition would produce. This lets the UI box "the units that merged
    # into this grapheme" exactly like the decomposition view does.
    input_units = list(Graphemizer(text).graphemes)
    groups = []
    idx = 0
    for g in composed_graphemes:
        n_units = len(Graphemizer(decompose(g)).graphemes) or 1
        groups.append({"source": g, "units": input_units[idx : idx + n_units]})
        idx += n_units

    return {
        "input": text,
        "composed": composed,
        "composed_graphemes": composed_graphemes,
        "groups": groups,
    }


# --- Distance -----------------------------------------------------------------
def get_distance(s1: str, s2: str) -> dict:
    g1 = list(Graphemizer(s1).graphemes)
    g2 = list(Graphemizer(s2).graphemes)
    equal_length = len(g1) == len(g2)
    return {
        "grapheme_levenshtein": levenshtein(s1, s2),
        "codepoint_levenshtein": textdistance.levenshtein.distance(s1, s2),
        "grapheme_hamming": hamming(s1, s2) if equal_length else None,
        "grapheme_count_s1": len(g1),
        "grapheme_count_s2": len(g2),
        "equal_grapheme_length": equal_length,
    }


# --- Metrics (single sentence pair) ------------------------------------------
def _metric_rows_sentence(reference: str, hypothesis: str) -> list[dict]:
    """Build the comparison table for one (reference, hypothesis) pair.

    ``higher_better`` lets the UI colour/sort sensibly. chrF/chrF++/Jaro/
    Jaro-Winkler/LCS/CharBLEU are higher-is-better; CER and the edit distances
    are lower-is-better error counts.
    """
    rows = [
        {
            "key": "grapheme_chrf",
            "label": "chrF",
            "family": "chrF",
            "level": "grapheme",
            "value": _round(_g_chrf.sentence_score(hypothesis, [reference]).score),
            "higher_better": True,
        },
        {
            "key": "std_chrf",
            "label": "chrF",
            "family": "chrF",
            "level": "codepoint",
            "value": _round(_std_chrf.sentence_score(hypothesis, [reference]).score),
            "higher_better": True,
        },
        {
            "key": "grapheme_chrf_pp",
            "label": "chrF++",
            "family": "chrF++",
            "level": "grapheme",
            "value": _round(_g_chrf_pp.sentence_score(hypothesis, [reference]).score),
            "higher_better": True,
        },
        {
            "key": "std_chrf_pp",
            "label": "chrF++",
            "family": "chrF++",
            "level": "codepoint",
            "value": _round(_std_chrf_pp.sentence_score(hypothesis, [reference]).score),
            "higher_better": True,
        },
        {
            "key": "cer",
            "label": "CER",
            "family": "CER",
            "level": "grapheme",
            "value": _round(CER(hypothesis, reference)),
            "higher_better": False,
        },
        {
            "key": "cer_codepoint",
            "label": "CER",
            "family": "CER",
            "level": "codepoint",
            "value": _round(_codepoint_cer(hypothesis, reference)),
            "higher_better": False,
        },
        {
            "key": "grapheme_levenshtein",
            "label": "Levenshtein",
            "family": "Levenshtein",
            "level": "grapheme",
            "value": levenshtein(reference, hypothesis),
            "higher_better": False,
        },
        {
            "key": "codepoint_levenshtein",
            "label": "Levenshtein",
            "family": "Levenshtein",
            "level": "codepoint",
            "value": textdistance.levenshtein.distance(reference, hypothesis),
            "higher_better": False,
        },
        {
            "key": "grapheme_damerau_levenshtein",
            "label": "Damerau-Levenshtein",
            "family": "Damerau-Levenshtein",
            "level": "grapheme",
            "value": damerau_levenshtein(reference, hypothesis),
            "higher_better": False,
        },
        {
            "key": "codepoint_damerau_levenshtein",
            "label": "Damerau-Levenshtein",
            "family": "Damerau-Levenshtein",
            "level": "codepoint",
            "value": textdistance.damerau_levenshtein.distance(reference, hypothesis),
            "higher_better": False,
        },
        {
            "key": "grapheme_jaro",
            "label": "Jaro",
            "family": "Jaro",
            "level": "grapheme",
            "value": _round(jaro(reference, hypothesis)),
            "higher_better": True,
        },
        {
            "key": "codepoint_jaro",
            "label": "Jaro",
            "family": "Jaro",
            "level": "codepoint",
            "value": _round(textdistance.jaro.normalized_similarity(reference, hypothesis)),
            "higher_better": True,
        },
        {
            "key": "grapheme_jaro_winkler",
            "label": "Jaro-Winkler",
            "family": "Jaro-Winkler",
            "level": "grapheme",
            "value": _round(jaro_winkler(reference, hypothesis)),
            "higher_better": True,
        },
        {
            "key": "codepoint_jaro_winkler",
            "label": "Jaro-Winkler",
            "family": "Jaro-Winkler",
            "level": "codepoint",
            "value": _round(
                textdistance.jaro_winkler.normalized_similarity(reference, hypothesis)
            ),
            "higher_better": True,
        },
        {
            "key": "grapheme_lcs",
            "label": "Longest Common Subsequence",
            "family": "LCS",
            "level": "grapheme",
            "value": longest_common_subsequence(reference, hypothesis),
            "higher_better": True,
        },
        {
            "key": "codepoint_lcs",
            "label": "Longest Common Subsequence",
            "family": "LCS",
            "level": "codepoint",
            "value": textdistance.lcsseq.similarity(reference, hypothesis),
            "higher_better": True,
        },
        {
            "key": "grapheme_charbleu",
            "label": "CharBLEU",
            "family": "CharBLEU",
            "level": "grapheme",
            "value": _round(charbleu(reference, hypothesis)),
            "higher_better": True,
        },
    ]
    return rows


def get_metrics(reference: str, hypothesis: str) -> dict:
    reference = reference or ""
    hypothesis = hypothesis or ""
    return {
        "reference_graphemes": list(Graphemizer(reference).graphemes),
        "hypothesis_graphemes": list(Graphemizer(hypothesis).graphemes),
        "metrics": _metric_rows_sentence(reference, hypothesis),
    }


# --- Metrics (corpus / file pair) --------------------------------------------
def _split_lines(raw: str) -> list[str]:
    # Keep line alignment; drop a single trailing newline's empty entry.
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def get_corpus_metrics(
    reference_text: str, prediction_text: str, max_rows: int = 200
) -> dict:
    refs_all = _split_lines(reference_text)
    hyps_all = _split_lines(prediction_text)
    n = min(len(refs_all), len(hyps_all))
    refs = refs_all[:n]
    hyps = hyps_all[:n]

    if n == 0:
        return {
            "line_count": 0,
            "reference_lines": len(refs_all),
            "prediction_lines": len(hyps_all),
            "aligned": len(refs_all) == len(hyps_all),
            "corpus": [],
            "rows": [],
        }

    # Mean of per-line error metrics (CER / Levenshtein).
    cer_vals = [CER(h, r) for h, r in zip(hyps, refs)]
    cp_cer_vals = [_codepoint_cer(h, r) for h, r in zip(hyps, refs)]
    g_lev_vals = [levenshtein(r, h) for r, h in zip(refs, hyps)]
    cp_lev_vals = [textdistance.levenshtein.distance(r, h) for r, h in zip(refs, hyps)]

    corpus = [
        {
            "key": "grapheme_chrf",
            "label": "chrF",
            "family": "chrF",
            "level": "grapheme",
            "value": _round(_g_chrf.corpus_score(hyps, [refs]).score),
            "higher_better": True,
        },
        {
            "key": "std_chrf",
            "label": "chrF",
            "family": "chrF",
            "level": "codepoint",
            "value": _round(_std_chrf.corpus_score(hyps, [refs]).score),
            "higher_better": True,
        },
        {
            "key": "grapheme_chrf_pp",
            "label": "chrF++",
            "family": "chrF++",
            "level": "grapheme",
            "value": _round(_g_chrf_pp.corpus_score(hyps, [refs]).score),
            "higher_better": True,
        },
        {
            "key": "std_chrf_pp",
            "label": "chrF++",
            "family": "chrF++",
            "level": "codepoint",
            "value": _round(_std_chrf_pp.corpus_score(hyps, [refs]).score),
            "higher_better": True,
        },
        {
            "key": "cer",
            "label": "CER (mean)",
            "family": "CER",
            "level": "grapheme",
            "value": _round(sum(cer_vals) / n),
            "higher_better": False,
        },
        {
            "key": "cer_codepoint",
            "label": "CER (mean)",
            "family": "CER",
            "level": "codepoint",
            "value": _round(sum(cp_cer_vals) / n),
            "higher_better": False,
        },
        {
            "key": "grapheme_levenshtein",
            "label": "Levenshtein (mean)",
            "family": "Levenshtein",
            "level": "grapheme",
            "value": _round(sum(g_lev_vals) / n),
            "higher_better": False,
        },
        {
            "key": "codepoint_levenshtein",
            "label": "Levenshtein (mean)",
            "family": "Levenshtein",
            "level": "codepoint",
            "value": _round(sum(cp_lev_vals) / n),
            "higher_better": False,
        },
    ]

    rows = [
        {
            "index": i,
            "reference": refs[i],
            "prediction": hyps[i],
            "grapheme_chrf": _round(_g_chrf.sentence_score(hyps[i], [refs[i]]).score),
            "std_chrf": _round(_std_chrf.sentence_score(hyps[i], [refs[i]]).score),
            "cer": _round(cer_vals[i]),
            "grapheme_levenshtein": g_lev_vals[i],
            "codepoint_levenshtein": cp_lev_vals[i],
        }
        for i in range(min(n, max_rows))
    ]

    return {
        "line_count": n,
        "reference_lines": len(refs_all),
        "prediction_lines": len(hyps_all),
        "aligned": len(refs_all) == len(hyps_all),
        "truncated_rows": n > max_rows,
        "corpus": corpus,
        "rows": rows,
    }


@lru_cache(maxsize=1)
def library_version() -> str:
    try:
        from importlib.metadata import version

        return version("grapheme-kit")
    except Exception:  # pragma: no cover - best effort only
        return "unknown"
