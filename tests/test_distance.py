import pytest

from graphemes_plusplus.distance import hamming, levenshtein


class TestLevenshtein:
	def test_levenshtein_exact_match(self):
		assert levenshtein("එවන්න", "එවන්න") == 0

	def test_levenshtein_single_edit(self):
		assert levenshtein("එවන්න", "එවන්") == 1

	def test_levenshtein_empty_inputs(self):
		assert levenshtein("", "") == 0
		assert levenshtein("එවන්න", "") == 4
		assert levenshtein("", "එවන්න") == 4

	def test_levenshtein_grapheme_aware_tamil(self):
		# "ஸ்ரீ" is one grapheme while "ஸ்ரி" splits into two.
		assert levenshtein("ஸ்ரீ", "ஸ்ரி") == 2

	def test_levenshtein_grapheme_aware_sinhala(self):
		assert levenshtein("ක්‍රම", "කම") == 1


class TestHamming:
	def test_hamming_exact_match(self):
		assert hamming("එවන්න", "එවන්න") == 0

	def test_hamming_single_mismatch(self):
		assert hamming("එවන්න", "එවන්") == 1

	def test_hamming_grapheme_aware(self):
		assert hamming("රැ", "රැහ") == 1

	def test_hamming_empty_inputs(self):
		assert hamming("", "") == 0

	def test_hamming_unequal_grapheme_lengths(self):
		assert hamming("එවන්න", "") == 4


if __name__ == "__main__":
	pytest.main([__file__, "-v"])
