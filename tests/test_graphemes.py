import pytest

from graphemes_plusplus.graphemizer import Graphemizer


class TestGraphemizer:
	def test_empty_string(self):
		g = Graphemizer("")
		assert g.graphemes == []
		assert len(g) == 0
		assert list(g) == []

	def test_ascii_text(self):
		g = Graphemizer("ක්‍රමය")
		assert g.graphemes == ["ක්‍ර", "ම", "ය"]
		assert len(g) == 3

	def test_tamil_special_cluster_merges(self):
		assert list(Graphemizer("க்ஷ")) == ["க்ஷ"]
		assert list(Graphemizer("ஸ்" + "ரீ")) == ["ஸ்ரீ"]
		assert list(Graphemizer("ஶ்" + "ரீ")) == ["ஶ்ரீ"]

	def test_tamil_split_variant(self):
		assert list(Graphemizer("ஸ்ரி")) == ["ஸ்", "ரி"]

	

	def test_sinhala_zwj_sequence_handling(self):
		assert list(Graphemizer("ක්‍රමය")) == ["ක්‍ර", "ම", "ය"]

	@pytest.mark.parametrize(
		"text, expected_len",
		[
			("வணக்கம்", 5),
			("සිංහල", 3),
			("ஸ்ரீ", 1),
		],
	)
	def test_len_matches_grapheme_count(self, text, expected_len):
		assert len(Graphemizer(text)) == expected_len


if __name__ == "__main__":
	pytest.main([__file__, "-v"])
