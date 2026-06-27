"""Tests for the graphemes_plusplus command-line interface.

Most tests drive ``cli.main(argv)`` in-process and capture stdout/stderr with
``capsys`` for speed; a couple of subprocess smoke tests exercise the real
``python -m graphemes_plusplus`` entry point and stdin piping.
"""

import io
import json
import subprocess
import sys

import pytest

from graphemes_plusplus.cli import main
from graphemes_plusplus.metric import CER, GraphemeCHRF


def run(argv, capsys, stdin=None, monkeypatch=None):
    """Invoke the CLI in-process and return (exit_code, stdout, stderr)."""
    if stdin is not None:
        monkeypatch.setattr(sys, "stdin", io.StringIO(stdin))
    code = main(argv)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


# --- graphemize --------------------------------------------------------------
class TestGraphemize:
    def test_count_json(self, capsys):
        code, out, _ = run(["graphemize", "ஸ்ரீ", "--format", "json"], capsys)
        data = json.loads(out)
        assert code == 0
        assert data["count"] == 1          # one grapheme cluster
        assert data["codepoint_count"] == 4  # but four Unicode code points

    def test_text_one_per_line(self, capsys):
        code, out, _ = run(["graphemize", "ஸ்ரீ வணக்கம்"], capsys)
        assert code == 0
        # graphemes are printed one per line; the space is its own cluster
        assert "ஸ்ரீ" in out.splitlines()

    def test_no_input_errors(self, capsys, monkeypatch):
        # simulate a non-tty empty stdin so it does not hang
        monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
        code, _, err = run(["graphemize"], capsys)
        assert code == 2
        assert "no input" in err


# --- distance ----------------------------------------------------------------
class TestDistance:
    def test_levenshtein_grapheme_vs_codepoint(self, capsys):
        code, out, _ = run(
            ["distance", "ஸ்ரீ", "ஸ்ரி", "-m", "levenshtein", "-l", "both", "-f", "json"],
            capsys,
        )
        data = json.loads(out)
        assert code == 0
        assert data["grapheme"] == 2     # ஸ்ரீ is 1 grapheme, ஸ்ரி is 2
        assert data["codepoint"] == 1    # naive code-point view understates it

    def test_hamming_unequal_lengths_is_error(self, capsys):
        code, _, err = run(["distance", "ஸ்ரீ", "ஸ்ரி", "-m", "hamming"], capsys)
        assert code == 2
        assert "equal" in err and "hamming" in err

    def test_hamming_equal_lengths_ok(self, capsys):
        code, out, _ = run(["distance", "ஸ்ரீ", "ஸ்ரீ", "-m", "hamming", "-f", "json"], capsys)
        assert code == 0
        assert json.loads(out)["grapheme"] == 0


# --- evaluate ----------------------------------------------------------------
class TestEvaluate:
    def test_chrf_matches_library(self, capsys):
        # CLI evaluate REF HYP computes sentence_score(hyp, [ref]); assert the
        # CLI reproduces the library's own number exactly.
        expected = round(GraphemeCHRF().sentence_score("நல்ல", ["நல்ல மாணவன்"]).score, 4)
        code, out, _ = run(
            ["evaluate", "நல்ல மாணவன்", "நல்ல", "--metric", "chrf", "-f", "json"], capsys
        )
        data = json.loads(out)
        value = next(r["value"] for r in data["metrics"] if r["metric"] == "chrF")
        assert code == 0
        assert value == expected

    def test_cer_matches_library(self, capsys):
        expected = round(CER("கனவ", "கனவா"), 4)  # CER(hyp, ref)
        code, out, _ = run(
            ["evaluate", "கனவா", "கனவ", "--metric", "cer", "-f", "json"], capsys
        )
        value = next(r["value"] for r in json.loads(out)["metrics"] if r["metric"] == "CER")
        assert code == 0
        assert value == expected

    def test_missing_operands_errors(self, capsys):
        code, _, err = run(["evaluate", "onlyref"], capsys)
        assert code == 2
        assert "HYPOTHESIS" in err or "hypothesis" in err


# --- decompose / compose -----------------------------------------------------
class TestDecomposeCompose:
    def test_round_trip_ok(self, capsys):
        code, out, _ = run(["decompose", "வணக்கம்", "--round-trip", "-f", "json"], capsys)
        data = json.loads(out)
        assert code == 0
        assert data["round_trip_ok"] is True

    def test_compose_inverse_of_decompose(self, capsys):
        from graphemes_plusplus import compose, decompose

        text = "வணக்கம்"
        code, out, _ = run(["compose", decompose(text)], capsys)
        assert code == 0
        assert out.strip() == compose(decompose(text))


# --- misc --------------------------------------------------------------------
class TestMisc:
    def test_version(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        assert "graphemes-plusplus" in capsys.readouterr().out

    def test_no_command_errors(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main([])
        assert exc.value.code != 0


# --- subprocess smoke (real entry point + stdin) -----------------------------
class TestEntryPoint:
    def test_module_invocation(self):
        result = subprocess.run(
            [sys.executable, "-m", "graphemes_plusplus", "graphemize", "ஸ்ரீ", "--count"],
            capture_output=True, encoding="utf-8",
        )
        assert result.returncode == 0
        assert "graphemes:   1" in result.stdout
        # the removed debug print must not leak into output
        assert "ආචාර්" not in result.stdout

    def test_stdin_pipe(self):
        result = subprocess.run(
            [sys.executable, "-m", "graphemes_plusplus", "graphemize", "--count"],
            input="ஸ்ரீ", capture_output=True, encoding="utf-8",
        )
        assert result.returncode == 0
        assert "graphemes:   1" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
