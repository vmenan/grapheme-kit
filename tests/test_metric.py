import pytest
from graphemes_plusplus.metric import GraphemeCHRF


@pytest.fixture
def chrf():
    return GraphemeCHRF()


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
    
    def test_complex_zwj_and_conjuncts(self, chrf):
        """Complex ZWJ characters in Sinhala and Tamil conjuncts."""
        score_sinhala_sent1 = chrf.corpus_score(["ක්‍රිකට් ක්‍රීඩා"], [["ක්‍රිකට් ක්‍රීඩා"]])
        assert score_sinhala_sent1.score == 100.0
        
        score_sinhala_partial1 = chrf.corpus_score(["ක්‍රීඩාව ජීවිතයේ අනිවාර්ය කොටසකි."], [["ක්‍රිඩාව ජීවිතයේ අනිවාර්ය කොටසකි."]])
        assert 0.0 <= score_sinhala_partial1.score < 100.0
        
        score_tamil_shri2 = chrf.corpus_score(["ஸ்ரீமான் நல்ல மனிதர்"], [["ஸ்ரீமான் நல்ல மனிதர்"]])
        assert score_tamil_shri2.score == 100.0
        
        score_tamil_partial1 = chrf.corpus_score(["ஸ்ரீலங்கா ஒரு அழகான தீவு நாடு."], [["ஶ்ரீலங்கா ஒரு அழகான தீவு நாடு."]])
        assert 0.0 <= score_tamil_partial1.score < 100.0
    
    def test_partial_match(self, chrf):
        """Partial match should be between 0 and 100 for Tamil and Sinhala."""
        score_tamil = chrf.corpus_score(["நல்ல"], [["நல்ல மாணவன்"]])
        assert 0.0 <= score_tamil.score < 100.0
        
        score_sinhala = chrf.corpus_score(["සි"], [["සිංහල"]])
        assert 0.0 <= score_sinhala.score < 100.0
    
    def test_whitespace(self, chrf):
        """Spaces removed before graphemizing for Tamil and Sinhala."""
        score_tamil_1 = chrf.corpus_score(["அவன்பார்த்தான்"], [["அவன்பார்த்தான்"]])
        score_tamil_2 = chrf.corpus_score(["அவன் பார்த்தான்"], [["அவன் பார்த்தான்"]])
        assert score_tamil_1.score == score_tamil_2.score == 100.0
        
        score_sinhala_1 = chrf.corpus_score(["සිංහල"], [["සිංහල"]])
        score_sinhala_2 = chrf.corpus_score(["සි ංහල"], [["සි ංහල"]])
        assert score_sinhala_1.score == score_sinhala_2.score == 100.0
    
    def test_inherits_from_chrf(self):
        """GraphemeCHRF should inherit from CHRF."""
        from sacrebleu.metrics.chrf import CHRF
        chrf = GraphemeCHRF()
        assert isinstance(chrf, CHRF)
        assert callable(chrf.corpus_score)
        assert callable(chrf.sentence_score)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
