import math

import pytest
from graphemes_plusplus.metric import GraphemeCHRF, CER, BPC, character_ngram_fscore


@pytest.fixture
def chrf():
    """Fixture for standard chrF (character/grapheme n-grams only)."""
    return GraphemeCHRF()

@pytest.fixture
def chrf_pp():
    """Fixture for chrF++ (includes word n-grams, typically order 2)."""
    return GraphemeCHRF(word_order=2)


class TestGraphemeCHRF:
    """Core tests for GraphemeCHRF metric"""
    
    def test_perfect_match(self, chrf):
        """Perfect match should score 100"""
        score_tamil = chrf.corpus_score(["வணக்கம்"], [["வணக்கம்"]])
        assert score_tamil.score == 100.0

        score_sinhala = chrf.corpus_score(["ස්වාගතයි"], [["ස්වාගතයි"]])
        assert score_sinhala.score == 100.0
    
    def test_complex_graphemes(self, chrf):
        """Complex conjuncts handled correctly"""
        score_tamil = chrf.corpus_score(["கொண்டுவந்து"], [["கொண்டுவந்து"]])
        assert score_tamil.score == 100.0

        score_sinhala = chrf.corpus_score(["සිංහල"], [["සිංහල"]])
        assert score_sinhala.score == 100.0

    def test_complete_mismatch(self, chrf):
        """Completely different strings sharing no graphemes should score 0."""
        # With proper grapheme-level matching, Tamil strings have no overlap
        score_tamil = chrf.corpus_score(["வணக்கம்"], [["நன்றி"]])
        assert score_tamil.score == 0.0

        # Sinhala strings share ස් and යි graphemes, so non-zero score
        score_sinhala = chrf.corpus_score(["ස්වාගතයි"], [["ස්තූතියි"]])
        assert score_sinhala.score == pytest.approx(11.9048, rel=1e-4)

    def test_empty_strings(self, chrf):
        """Should handle empty strings gracefully without crashing."""
        score_empty_hyp = chrf.corpus_score([""], [["வணக்கம்"]])
        assert score_empty_hyp.score == 0.0
        
        score_empty_ref = chrf.corpus_score(["ස්තූතියි"], [[""]])
        assert score_empty_ref.score == 0.0

    def test_sentence_score_method(self, chrf):
        """Test sentence_score method directly."""
        score_perfect = chrf.sentence_score("සිංහල", ["සිංහල"])
        assert score_perfect.score == 100.0

        score_partial = chrf.sentence_score("நல்ல", ["நல்ல மாணவன்"])
        assert score_partial.score == pytest.approx(37.1051, rel=1e-4)

    def test_complex_zwj_and_conjuncts(self, chrf):
        """Complex ZWJ characters in Sinhala and Tamil conjuncts."""
        score_sinhala_sent1 = chrf.corpus_score(["ක්‍රිකට් ක්‍රීඩා"], [["ක්‍රිකට් ක්‍රීඩා"]])
        assert score_sinhala_sent1.score == 100.0

        score_sinhala_partial1 = chrf.corpus_score(["ක්‍රීඩාව ජීවිතයේ අනිවාර්ය කොටසකි."], [["ක්‍රිඩාව ජීවිතයේ අනිවාර්ය කොටසකි."]])
        assert score_sinhala_partial1.score == pytest.approx(93.0054, rel=1e-4)

        score_tamil_shri2 = chrf.corpus_score(["ஸ்ரீமான் நல்ல மனிதர்"], [["ஸ்ரீமான் நல்ல மனிதர்"]])
        assert score_tamil_shri2.score == 100.0

        score_tamil_partial1 = chrf.corpus_score(["ஸ்ரீலங்கா ஒரு அழகான தீவு நாடு."], [["ஶ்ரீலங்கா ஒரு அழகான தீவு நாடு."]])
        assert score_tamil_partial1.score == pytest.approx(91.8457, rel=1e-4)
    
    def test_partial_match(self, chrf):
        """Partial match should be between 0 and 100 for Tamil and Sinhala."""
        score_tamil = chrf.corpus_score(["நல்ல"], [["நல்ல மாணவன்"]])
        assert score_tamil.score == pytest.approx(37.1051, rel=1e-4)

        # Note: At grapheme level, 'සි' doesn't match 'සිං' - they are different graphemes
        # This correctly scores 0 because there's no grapheme overlap
        score_sinhala = chrf.corpus_score(["සි"], [["සිංහල"]])
        assert score_sinhala.score == 0.0
    
    def test_whitespace(self, chrf):
        """Spaces removed before graphemizing for Tamil and Sinhala."""
        score_tamil_1 = chrf.corpus_score(["அவன்பார்த்தான்"], [["அவன்பார்த்தான்"]])
        score_tamil_2 = chrf.corpus_score(["அவன் பார்த்தான்"], [["அவன் பார்த்தான்"]])
        assert score_tamil_1.score == score_tamil_2.score == 100.0
        
        score_sinhala_1 = chrf.corpus_score(["සිංහල"], [["සිංහල"]])
        score_sinhala_2 = chrf.corpus_score(["සි ංහල"], [["සි ංහල"]])
        assert score_sinhala_1.score == score_sinhala_2.score == 100.0
    
    def test_mixed_scripts_and_punctuation(self, chrf):
        """Should handle strings mixing English, Indic scripts, and punctuation."""
        hyp = "Hello வணக்கம், world!"
        ref = "Hello வணக்கம், world!"
        score = chrf.corpus_score([hyp], [[ref]])
        assert score.score == 100.0

        ref_no_punc = "Hello வணக்கம் world"
        score_punc = chrf.corpus_score([hyp], [[ref_no_punc]])
        assert score_punc.score == pytest.approx(75.3096, rel=1e-4)
    
    def test_inherits_from_chrf(self):
        """GraphemeCHRF should inherit from CHRF."""
        from sacrebleu.metrics.chrf import CHRF
        chrf_instance = GraphemeCHRF()
        assert isinstance(chrf_instance, CHRF)
        assert callable(chrf_instance.corpus_score)
        assert callable(chrf_instance.sentence_score)

    # --- chrF++ Specific Tests ---

    def test_chrf_plusplus_perfect_match(self, chrf_pp):
        """chrF++ should still score 100 for a perfect match."""
        score_tamil = chrf_pp.corpus_score(["வணக்கம் உலகம்"], [["வணக்கம் உலகம்"]])
        assert score_tamil.score == 100.0
        
        score_sinhala = chrf_pp.corpus_score(["සුබ උදෑසනක්"], [["සුබ උදෑසනක්"]])
        assert score_sinhala.score == 100.0

    def test_chrf_plusplus_word_order_matters(self, chrf, chrf_pp):
        """chrF++ includes word n-grams which capture word order information."""
        ref = ["இன்று வானிலை மிகவும் அழகாக இருக்கிறது"]
        hyp = ["இருக்கிறது அழகாக மிகவும் வானிலை இன்று"]

        score_standard = chrf.corpus_score(hyp, [ref])
        score_pp = chrf_pp.corpus_score(hyp, [ref])

        # Both should give meaningful scores for reordered text
        assert score_standard.score == pytest.approx(47.1802, rel=1e-4)
        assert score_pp.score == pytest.approx(47.8852, rel=1e-4)

    def test_chrf_plusplus_partial_word_match(self, chrf_pp):
        """chrF++ should handle partial word/grapheme overlaps correctly."""
        score = chrf_pp.corpus_score(["මෙය නව මාර්ගය වේ"], [["මෙය නව මාර්ග වේ"]])
        assert score.score == pytest.approx(72.6814, rel=1e-4)

    def test_chrf_plusplus_configuration(self, chrf_pp):
        """Ensure the metric correctly registers the word_order parameter."""
        assert hasattr(chrf_pp, 'word_order')
        assert chrf_pp.word_order == 2


class TestCER:
    """Tests for grapheme-aware Character Error Rate."""

    def test_cer_perfect_match(self):
        """Identical strings should have zero CER."""
        assert CER("வணக்கம்", "வணக்கம்") == 0.0
        assert CER("සිංහල", "සිංහල") == 0.0

    def test_cer_single_substitution(self):
        """One substitution over three reference graphemes gives CER 1/3."""
        assert CER("කනවා", "කනව") == pytest.approx(1 / 3, rel=1e-9)

    def test_cer_empty_reference_cases(self):
        """Edge behavior when reference is empty should be well-defined."""
        assert CER("", "") == 0.0
        assert CER("ක", "") == 1.0

    def test_cer_grapheme_aware(self):
        """Tamil ligatures should be compared by graphemes, not code points."""
        # "ஸ்ரீ" is 1 grapheme and "ஸ்ரி" is 2 graphemes; distance is 2 over 2 refs.
        assert CER("ஸ்ரீ", "ஸ்ரி") == pytest.approx(1.0, rel=1e-9)

    def test_cer_complex_conjuncts(self):
        """Complex Sinhala conjuncts should be handled correctly."""
        assert CER("ක්‍රි", "ක්‍රි") == 0.0
        assert CER("ක්‍රමය", "ක්මය") == pytest.approx(1 / 3, rel=1e-9)

    


if __name__ == "__main__":
    pytest.main([__file__, "-v"])