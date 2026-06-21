"""Parity tests: the API must reproduce the real library's numbers.

The expected values mirror those asserted in the library's own
``tests/test_metric.py``, proving the website surfaces genuine library output
rather than an approximation.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _metric(payload_metrics, key):
    return next(m for m in payload_metrics if m["key"] == key)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_graphemes_tamil_ligature():
    # "ஸ்ரீ" is a single grapheme cluster in our splitter.
    r = client.post("/api/graphemes", json={"text": "ஸ்ரீ மதி"})
    assert r.status_code == 200
    body = r.json()
    assert body["graphemes"] == ["ஸ்ரீ", " ", "ம", "தி"]
    assert body["count"] == 4
    # Code-point view: "ஸ்ரீ" alone is 4 scalars, so the whole string has more
    # code points than graphemes — the contrast the Graphemizer page shows.
    assert body["codepoint_count"] == len(body["codepoints"])
    assert body["codepoint_count"] > body["count"]


def test_metrics_perfect_match_scores_100():
    r = client.post(
        "/api/metrics", json={"reference": "வணக்கம்", "hypothesis": "வணக்கம்"}
    )
    body = r.json()
    assert _metric(body["metrics"], "grapheme_chrf")["value"] == 100.0


def test_metrics_partial_match_matches_library_value():
    # Library test: chrf.sentence_score("நல்ல", ["நல்ல மாணவன்"]) ~= 37.1051
    r = client.post(
        "/api/metrics",
        json={"reference": "நல்ல மாணவன்", "hypothesis": "நல்ல"},
    )
    body = r.json()
    assert _metric(body["metrics"], "grapheme_chrf")["value"] == pytest.approx(
        37.1051, rel=1e-4
    )


def test_metrics_chrf_pp_value():
    # chrf_pp.corpus_score(["මෙය නව මාර්ගය වේ"], [["මෙය නව මාර්ග වේ"]]) ~= 72.6814
    r = client.post(
        "/api/metrics",
        json={"reference": "මෙය නව මාර්ග වේ", "hypothesis": "මෙය නව මාර්ගය වේ"},
    )
    body = r.json()
    assert _metric(body["metrics"], "grapheme_chrf_pp")["value"] == pytest.approx(
        72.6814, rel=1e-4
    )


def test_metrics_cer_one_third():
    # CER("කනවා", "කනව") == 1/3  (hypothesis, reference)
    r = client.post(
        "/api/metrics", json={"reference": "කනව", "hypothesis": "කනවා"}
    )
    body = r.json()
    assert _metric(body["metrics"], "cer")["value"] == pytest.approx(0.3333, rel=1e-3)


def test_no_bleu_and_has_codepoint_cer():
    # BLEU is not part of the library; it was removed. CER is reported at both
    # grapheme and code-point level.
    r = client.post("/api/metrics", json={"reference": "aaa", "hypothesis": "efdscaaa"})
    keys = [m["key"] for m in r.json()["metrics"]]
    assert "bleu" not in keys
    assert "cer" in keys
    assert "cer_codepoint" in keys


def test_distance_grapheme_vs_codepoint():
    # The whole point of the library: grapheme distance != code-point distance.
    # "ஸ்ரீ" is 1 grapheme but "ஸ்ரி" is 2, so the grapheme edit distance is 2,
    # while at the raw Unicode level only the final vowel sign differs (1).
    r = client.post("/api/distance", json={"s1": "ஸ்ரீ", "s2": "ஸ்ரி"})
    body = r.json()
    assert body["grapheme_levenshtein"] == 2
    assert body["codepoint_levenshtein"] == 1


def test_decompose_round_trips():
    r = client.post("/api/decompose", json={"text": "வணக்கம்"})
    body = r.json()
    assert body["round_trip_ok"] is True
    assert body["recomposed"] == "வணக்கம்"


def test_decompose_groups_are_consistent():
    r = client.post("/api/decompose", json={"text": "வணக்கம் உலகம்"})
    body = r.json()
    # One group per source grapheme...
    assert [g["source"] for g in body["groups"]] == body["graphemes"]
    # ...and the units concatenated equal the flat decomposition.
    flat = [u for g in body["groups"] for u in g["units"]]
    assert flat == body["decomposed_graphemes"]
    # "வ" decomposes into two phonetic units (consonant + inherent vowel).
    first = body["groups"][0]
    assert first["source"] == "வ"
    assert len(first["units"]) == 2


def test_corpus_metrics_via_files():
    ref = "வணக்கம்\nநல்ல மாணவன்\n"
    pred = "வணக்கம்\nநல்ல\n"
    files = {
        "reference_file": ("ref.txt", ref.encode("utf-8"), "text/plain"),
        "prediction_file": ("pred.txt", pred.encode("utf-8"), "text/plain"),
    }
    r = client.post("/api/metrics/corpus", files=files)
    assert r.status_code == 200
    body = r.json()
    assert body["line_count"] == 2
    assert body["aligned"] is True
    assert _metric(body["corpus"], "grapheme_chrf")["value"] > 0
