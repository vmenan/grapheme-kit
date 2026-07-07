"""Command-line interface for ``graphemes_plusplus``.

Exposes the library's grapheme-aware tools as a small, dependency-free subcommand
CLI built on :mod:`argparse`. Every number it prints comes straight from the
library (with ``sacrebleu`` / ``textdistance`` for the code-point baselines, both
already library dependencies), so the CLI has parity with the demo website.

Examples
--------
    graphemes-plusplus graphemize "ஸ்ரீ வணக்கம்" --count
    graphemes-plusplus decompose "வணக்கம்" --round-trip
    graphemes-plusplus distance "ஸ்ரீ" "ஸ்ரி" --measure levenshtein --level both
    graphemes-plusplus evaluate "நல்ல மாணவன்" "நல்ல" --metric chrf
    graphemes-plusplus normalize --input raw.txt --output clean.txt

Every command reads from a positional ``TEXT`` argument, ``--input FILE`` or
stdin, and writes to stdout (or ``--output FILE``) as human-readable text or, with
``--format json``, machine-readable JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Optional, Sequence

import textdistance
from sacrebleu.metrics import CHRF as StdCHRF

from graphemes_plusplus import Graphemizer, compose, decompose, hamming, levenshtein
from graphemes_plusplus.metric import CER, GraphemeCHRF
from graphemes_plusplus.utils.file_utils import normalize_file
from graphemes_plusplus.utils.normalizer import Normalizer

PROG = "graphemes-plusplus"


class CLIError(Exception):
    """A user-facing error: printed cleanly to stderr with exit code 2 (no traceback)."""


# --- helpers -----------------------------------------------------------------
def _version() -> str:
    try:
        from importlib.metadata import version

        return version("graphemes-plusplus")
    except Exception:  # pragma: no cover - best effort only
        return "0.1.0"


def _force_utf8() -> None:
    """Make stdin/stdout/stderr speak UTF-8 regardless of platform.

    Indic text on a Windows ``cp1252`` console would otherwise raise
    ``UnicodeEncodeError``; this removes the need for a ``PYTHONUTF8`` env var.
    """
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except Exception:  # pragma: no cover - stream may not support it
                pass


def _resolve_text(args: argparse.Namespace) -> str:
    """Resolve a single text input from TEXT arg, --input FILE, or stdin."""
    if getattr(args, "text", None) is not None:
        return args.text
    if getattr(args, "input", None):
        with open(args.input, "r", encoding="utf-8") as fh:
            return fh.read().rstrip("\n")
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip("\n")
    raise CLIError("no input: provide TEXT, --input FILE, or pipe text via stdin")


def _emit(args: argparse.Namespace, text: str) -> None:
    """Write ``text`` to --output FILE or stdout, always with a trailing newline."""
    payload = text if text.endswith("\n") else text + "\n"
    if getattr(args, "output", None):
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
    else:
        sys.stdout.write(payload)


def _emit_json(args: argparse.Namespace, obj: object) -> None:
    _emit(args, json.dumps(obj, ensure_ascii=False, indent=2))


def _read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return lines


# --- graphemize --------------------------------------------------------------
def _cmd_graphemize(args: argparse.Namespace) -> int:
    text = _resolve_text(args)
    graphemes = list(Graphemizer(text).graphemes)
    codepoints = list(text)

    if args.format == "json":
        _emit_json(
            args,
            {
                "text": text,
                "graphemes": graphemes,
                "count": len(graphemes),
                "codepoints": codepoints,
                "codepoint_count": len(codepoints),
            },
        )
        return 0

    lines: list[str] = []
    if args.count:
        lines.append(f"graphemes:   {len(graphemes)}")
        lines.append(f"code points: {len(codepoints)}")
        lines.append("")
    lines.extend(graphemes)
    if args.codepoints:
        lines.append("")
        lines.append("# code points")
        lines.extend(codepoints)
    _emit(args, "\n".join(lines))
    return 0


# --- decompose / compose -----------------------------------------------------
def _cmd_decompose(args: argparse.Namespace) -> int:
    text = _resolve_text(args)
    decomposed = decompose(text)

    if args.format == "json":
        obj = {
            "input": text,
            "decomposed": decomposed,
            "decomposed_graphemes": list(Graphemizer(decomposed).graphemes),
        }
        if args.round_trip:
            recomposed = compose(decomposed)
            obj["recomposed"] = recomposed
            obj["round_trip_ok"] = recomposed == text
        _emit_json(args, obj)
        return 0

    if args.round_trip:
        recomposed = compose(decomposed)
        ok = recomposed == text
        _emit(
            args,
            "\n".join(
                [
                    decomposed,
                    "",
                    f"recomposed: {recomposed}",
                    f"round-trip: {'OK' if ok else 'MISMATCH'}",
                ]
            ),
        )
    else:
        _emit(args, decomposed)
    return 0


def _cmd_compose(args: argparse.Namespace) -> int:
    text = _resolve_text(args)
    try:
        composed = compose(text)
    except ValueError as exc:
        raise CLIError(f"compose failed: {exc}")

    if args.format == "json":
        _emit_json(args, {"input": text, "composed": composed})
    else:
        _emit(args, composed)
    return 0


# --- distance ----------------------------------------------------------------
def _grapheme_count(text: str) -> int:
    return len(Graphemizer(text).graphemes)


def _distance_value(ref: str, hyp: str, measure: str, level: str) -> int:
    if measure == "levenshtein":
        if level == "grapheme":
            return levenshtein(ref, hyp)
        return textdistance.levenshtein.distance(ref, hyp)

    # hamming: enforce equal-length contract (matches the paper and demo, which
    # treat differing lengths as undefined rather than padding silently).
    if level == "grapheme":
        n_ref, n_hyp = _grapheme_count(ref), _grapheme_count(hyp)
        unit = "grapheme"
    else:
        n_ref, n_hyp = len(ref), len(hyp)
        unit = "code-point"
    if n_ref != n_hyp:
        raise CLIError(
            f"hamming distance requires equal {unit} counts "
            f"({n_ref} vs {n_hyp}); use --measure levenshtein for unequal lengths."
        )
    if level == "grapheme":
        return hamming(ref, hyp)
    return textdistance.hamming.distance(ref, hyp)


def _cmd_distance(args: argparse.Namespace) -> int:
    ref, hyp = args.reference, args.hypothesis
    levels = ["grapheme", "codepoint"] if args.level == "both" else [args.level]
    values = {lv: _distance_value(ref, hyp, args.measure, lv) for lv in levels}

    if args.format == "json":
        _emit_json(
            args,
            {
                "measure": args.measure,
                "reference": ref,
                "hypothesis": hyp,
                "reference_graphemes": _grapheme_count(ref),
                "hypothesis_graphemes": _grapheme_count(hyp),
                **values,
            },
        )
        return 0

    lines = [f"{args.measure} ({lv}): {values[lv]}" for lv in levels]
    _emit(args, "\n".join(lines))
    return 0


# --- evaluate ----------------------------------------------------------------
def _chrf_score(ref: str, hyp: str, level: str, plus_plus: bool) -> float:
    if level == "grapheme":
        metric = GraphemeCHRF(word_order=2) if plus_plus else GraphemeCHRF()
    else:
        metric = StdCHRF(word_order=2) if plus_plus else StdCHRF()
    return round(metric.sentence_score(hyp, [ref]).score, 4)


def _cer_score(ref: str, hyp: str, level: str) -> float:
    if level == "grapheme":
        return round(CER(hyp, ref), 4)
    if len(ref) == 0:
        return 0.0 if len(hyp) == 0 else 1.0
    return round(textdistance.levenshtein.distance(hyp, ref) / len(ref), 4)


def _sentence_rows(ref: str, hyp: str, metric: str, level: str) -> list[dict]:
    want = {"chrf", "chrf++", "cer"} if metric == "all" else {metric}
    levels = ["grapheme", "codepoint"] if level == "both" else [level]
    rows: list[dict] = []
    for lv in levels:
        if "chrf" in want:
            rows.append({"metric": "chrF", "level": lv, "value": _chrf_score(ref, hyp, lv, False)})
        if "chrf++" in want:
            rows.append({"metric": "chrF++", "level": lv, "value": _chrf_score(ref, hyp, lv, True)})
        if "cer" in want:
            rows.append({"metric": "CER", "level": lv, "value": _cer_score(ref, hyp, lv)})
    return rows


def _corpus_rows(refs: list[str], hyps: list[str], metric: str, level: str) -> list[dict]:
    want = {"chrf", "chrf++", "cer"} if metric == "all" else {metric}
    levels = ["grapheme", "codepoint"] if level == "both" else [level]
    n = len(refs)
    rows: list[dict] = []
    for lv in levels:
        if "chrf" in want:
            score = (GraphemeCHRF() if lv == "grapheme" else StdCHRF()).corpus_score(hyps, [refs]).score
            rows.append({"metric": "chrF", "level": lv, "value": round(score, 4)})
        if "chrf++" in want:
            obj = GraphemeCHRF(word_order=2) if lv == "grapheme" else StdCHRF(word_order=2)
            rows.append({"metric": "chrF++", "level": lv, "value": round(obj.corpus_score(hyps, [refs]).score, 4)})
        if "cer" in want:
            mean = sum(_cer_score(r, h, lv) for r, h in zip(refs, hyps)) / n
            rows.append({"metric": "CER (mean)", "level": lv, "value": round(mean, 4)})
    return rows


def _cmd_evaluate(args: argparse.Namespace) -> int:
    corpus_mode = bool(args.reference_file or args.hypothesis_file)

    if corpus_mode:
        if not (args.reference_file and args.hypothesis_file):
            raise CLIError("corpus mode needs both --reference-file and --hypothesis-file")
        refs_all = _read_lines(args.reference_file)
        hyps_all = _read_lines(args.hypothesis_file)
        n = min(len(refs_all), len(hyps_all))
        if n == 0:
            raise CLIError("no aligned lines to evaluate (one or both files are empty)")
        refs, hyps = refs_all[:n], hyps_all[:n]
        rows = _corpus_rows(refs, hyps, args.metric, args.level)
        meta = {
            "mode": "corpus",
            "line_count": n,
            "reference_lines": len(refs_all),
            "prediction_lines": len(hyps_all),
            "aligned": len(refs_all) == len(hyps_all),
        }
    else:
        if args.reference is None or args.hypothesis is None:
            raise CLIError(
                "provide REFERENCE and HYPOTHESIS, or use --reference-file/--hypothesis-file"
            )
        rows = _sentence_rows(args.reference, args.hypothesis, args.metric, args.level)
        meta = {"mode": "sentence", "reference": args.reference, "hypothesis": args.hypothesis}

    if args.format == "json":
        _emit_json(args, {**meta, "metrics": rows})
        return 0

    lines: list[str] = []
    if corpus_mode:
        if not meta["aligned"]:
            lines.append(
                f"# files differ in length ({meta['reference_lines']} vs "
                f"{meta['prediction_lines']}); compared first {meta['line_count']} lines"
            )
        else:
            lines.append(f"# {meta['line_count']} line(s)")
    for row in rows:
        lines.append(f"{row['metric']} ({row['level']}): {row['value']}")
    _emit(args, "\n".join(lines))
    return 0


# --- normalize ---------------------------------------------------------------
def _cmd_normalize(args: argparse.Namespace) -> int:
    # File mode: stream a file through normalize_file (line by line).
    if args.input:
        out_path = normalize_file(args.input, args.output)
        if args.format == "json":
            _emit_json(args, {"input": args.input, "output": out_path})
        else:
            sys.stderr.write(f"normalized -> {out_path}\n")
        return 0

    # Text mode: normalize a single string.
    text = _resolve_text(args)
    normalized = Normalizer().normalize(text)
    if args.format == "json":
        _emit_json(args, {"input": text, "normalized": normalized})
    else:
        _emit(args, normalized)
    return 0


# --- parser ------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Grapheme-aware toolkit for Tamil and Sinhala: segmentation, "
        "decomposition/composition, distance and evaluation metrics.",
        epilog=(
            "examples:\n"
            f"  {PROG} graphemize \"ஸ்ரீ வணக்கம்\" --count\n"
            f"  {PROG} graphemize \"ශ්‍රී ලංකාව\" --count\n"
            f"  {PROG} distance \"ஸ்ரீ\" \"ஸ்ரி\" --level both\n"
            f"  {PROG} evaluate \"நல்ல மாணவன்\" \"நல்ல\" --metric chrf\n"
            f"  echo \"ශ්‍රී\" | {PROG} decompose --round-trip\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"{PROG} {_version()}"
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # Shared output options (every command).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-f", "--format", choices=["text", "json"], default="text",
        help="output format (default: text)",
    )
    common.add_argument(
        "-o", "--output", metavar="FILE",
        help="write output to FILE instead of stdout",
    )

    # Shared single-text input (graphemize/decompose/compose/normalize).
    text_in = argparse.ArgumentParser(add_help=False)
    text_in.add_argument(
        "text", nargs="?",
        help="input text; if omitted, read from --input FILE or stdin",
    )
    text_in.add_argument(
        "-i", "--input", metavar="FILE", help="read input from FILE",
    )

    p_graph = sub.add_parser(
        "graphemize", parents=[text_in, common],
        help="segment text into grapheme clusters",
    )
    p_graph.add_argument("--count", action="store_true", help="show grapheme / code-point counts")
    p_graph.add_argument("--codepoints", action="store_true", help="also list raw Unicode code points")
    p_graph.set_defaults(func=_cmd_graphemize)

    p_dec = sub.add_parser(
        "decompose", parents=[text_in, common],
        help="decompose grapheme clusters into phonetic units",
    )
    p_dec.add_argument("--round-trip", action="store_true", help="recompose and report round-trip status")
    p_dec.set_defaults(func=_cmd_decompose)

    p_com = sub.add_parser(
        "compose", parents=[text_in, common],
        help="recompose phonetic units into grapheme clusters",
    )
    p_com.set_defaults(func=_cmd_compose)

    p_dist = sub.add_parser(
        "distance", parents=[common],
        help="grapheme-aware edit distance between two strings",
    )
    p_dist.add_argument("reference", help="reference / first string")
    p_dist.add_argument("hypothesis", help="hypothesis / second string")
    p_dist.add_argument(
        "-m", "--measure", choices=["levenshtein", "hamming"], default="levenshtein",
        help="distance measure (default: levenshtein)",
    )
    p_dist.add_argument(
        "-l", "--level", choices=["grapheme", "codepoint", "both"], default="grapheme",
        help="compare at grapheme level, code-point level, or both (default: grapheme)",
    )
    p_dist.set_defaults(func=_cmd_distance)

    p_eval = sub.add_parser(
        "evaluate", parents=[common],
        help="grapheme-aware evaluation metrics (chrF / chrF++ / CER)",
    )
    p_eval.add_argument("reference", nargs="?", help="reference / gold string")
    p_eval.add_argument("hypothesis", nargs="?", help="hypothesis / predicted string")
    p_eval.add_argument("--reference-file", metavar="FILE", help="corpus mode: reference lines")
    p_eval.add_argument("--hypothesis-file", metavar="FILE", help="corpus mode: prediction lines")
    p_eval.add_argument(
        "--metric", choices=["chrf", "chrf++", "cer", "all"], default="all",
        help="metric to report (default: all)",
    )
    p_eval.add_argument(
        "-l", "--level", choices=["grapheme", "codepoint", "both"], default="grapheme",
        help="grapheme level, code-point baseline, or both (default: grapheme)",
    )
    p_eval.set_defaults(func=_cmd_evaluate)

    p_norm = sub.add_parser(
        "normalize", parents=[text_in, common],
        help="normalize text (NFC + Tamil/Sinhala fixups); --input for a file",
    )
    p_norm.set_defaults(func=_cmd_normalize)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point. Returns a process exit code (0 ok, 2 user error)."""
    _force_utf8()
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except CLIError as exc:
        print(f"{PROG}: error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"{PROG}: error: file not found: {exc.filename}", file=sys.stderr)
        return 2
    except BrokenPipeError:  # piped into head/less etc.
        return 0
    except KeyboardInterrupt:  # pragma: no cover
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
