import pytest

from grapheme_kit.distance import hamming, levenshtein, damerau_levenshtein, jaro, jaro_winkler, longest_common_subsequence
from grapheme_kit.metric import charbleu


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
	def test_hamming_complex_conjuncts(self):
		assert hamming("ක්‍රමය", "ක්මය")==1


class TestDamerauLevenshtein:
	def test_damerau_levenshtein_exact_match(self):
		assert damerau_levenshtein("එවන්න", "එවන්න") == 0

	def test_damerau_levenshtein_single_substitution(self):
		assert damerau_levenshtein("එවන්න", "එවම්න") == 1

	def test_damerau_levenshtein_single_transposition(self):
		# Transposition of two adjacent graphemes should cost 1
		assert damerau_levenshtein("ab", "ba") == 1

	def test_damerau_levenshtein_empty_inputs(self):
		assert damerau_levenshtein("", "") == 0
		assert damerau_levenshtein("එවන්න", "") == 4
		assert damerau_levenshtein("", "එවන්න") == 4

	def test_damerau_levenshtein_insertion(self):
		assert damerau_levenshtein("එවන්", "එවන්න") == 1

	def test_damerau_levenshtein_deletion(self):
		assert damerau_levenshtein("එවන්න", "එවන්") == 1

	def test_damerau_levenshtein_grapheme_aware_tamil(self):
		# "ஸ்ரீ" is one grapheme while "ஸ்ரி" splits into two.
		assert damerau_levenshtein("ஸ்ரீ", "ஸ்ரி") == 2

	def test_damerau_levenshtein_grapheme_aware_sinhala(self):
		assert damerau_levenshtein("ක්‍රම", "කම") == 1

	def test_damerau_levenshtein_transposition_sinhala(self):
		# Two adjacent Sinhala graphemes swapped
		assert damerau_levenshtein("කම", "මක") == 1


class TestJaro:
	def test_jaro_exact_match(self):
		assert jaro("එවන්න", "එවන්න") == 1.0

	def test_jaro_empty_strings(self):
		assert jaro("", "") == 1.0

	def test_jaro_one_empty_string(self):
		assert jaro("එවන්න", "") == 0.0
		assert jaro("", "එවන්න") == 0.0

	def test_jaro_single_character_match(self):
		# Completely different single characters have no similarity
		assert jaro("අ", "ඉ") == 0.0

	def test_jaro_identical_grapheme_sequences(self):
		# Sinhala word
		assert jaro("ක්‍රම", "ක්‍රම") == 1.0

	def test_jaro_partial_match_tamil(self):
		# Strings with some shared graphemes should have similarity > 0
		# Using Sinhala since Tamil single words graphemize as single units
		score = jaro("කරණ", "කරම")
		assert score > 0

	def test_jaro_different_strings(self):
		# Completely different strings should have low similarity
		assert jaro("අ", "ඝ") < 0.5

	def test_jaro_transposition_penalty(self):
		# Transposed characters should reduce similarity
		score1 = jaro("abc", "abc")
		score2 = jaro("abc", "bac")
		assert score1 > score2
		assert score1 == 1.0


class TestJaroWinkler:
	def test_jaro_winkler_exact_match(self):
		assert jaro_winkler("එවන්න", "එවන්න") == 1.0

	def test_jaro_winkler_empty_strings(self):
		assert jaro_winkler("", "") == 1.0

	def test_jaro_winkler_one_empty_string(self):
		assert jaro_winkler("එවන්න", "") == 0.0
		assert jaro_winkler("", "එවන්න") == 0.0

	def test_jaro_winkler_single_character_match(self):
		# Completely different single characters have no similarity
		assert jaro_winkler("අ", "ඉ") == 0.0

	def test_jaro_winkler_prefix_bonus(self):
		# Strings with matching prefixes should have higher Jaro-Winkler
		# than plain Jaro similarity
		s1 = "කරණ"
		s2 = "කරම"
		jaro_score = jaro(s1, s2)
		jaro_winkler_score = jaro_winkler(s1, s2)
		assert jaro_winkler_score >= jaro_score

	def test_jaro_winkler_identical_grapheme_sequences(self):
		# Sinhala word
		assert jaro_winkler("ක්‍රම", "ක්‍රම") == 1.0

	def test_jaro_winkler_partial_match_tamil(self):
		# Strings with some shared graphemes should have similarity > 0
		# Using Sinhala since Tamil single words graphemize as single units
		score = jaro_winkler("කරණ", "කරම")
		assert score > 0

	def test_jaro_winkler_different_strings(self):
		# Completely different strings should have low similarity
		assert jaro_winkler("අ", "ඝ") < 0.5

	def test_jaro_winkler_matching_prefix_bonus(self):
		# Matching first grapheme should increase score compared to no match
		score_matching = jaro_winkler("කරණ", "කරම")
		score_different = jaro_winkler("අරණ", "බරම")
		assert score_matching > score_different



class TestLongestCommonSubsequence:
	def test_lcs_exact_match(self):
		# Identical strings have LCS equal to their grapheme count
		result = longest_common_subsequence("එවන්න", "එවන්න")
		assert result == 4

	def test_lcs_empty_strings(self):
		assert longest_common_subsequence("", "") == 0

	def test_lcs_one_empty_string(self):
		# LCS with empty string is 0
		assert longest_common_subsequence("එවන්න", "") == 0
		assert longest_common_subsequence("", "එවන්න") == 0

	def test_lcs_no_common_subsequence(self):
		# Completely different single graphemes have LCS of 0
		assert longest_common_subsequence("අ", "ඉ") == 0

	def test_lcs_partial_subsequence(self):
		# "abc" and "ac" share "ac" as common subsequence (2 graphemes)
		assert longest_common_subsequence("abc", "ac") == 2

	def test_lcs_sinhala_subsequence(self):
		# "කරණ" (3 graphemes) vs "කරම" (3 graphemes)
		# Common subsequence is "කර" (2 graphemes)
		lcs_length = longest_common_subsequence("කරණ", "කරම")
		assert lcs_length == 2

	def test_lcs_sinhala_insertion(self):
		# "කරණ" vs "කරණල" - shares "කරණ" (3 graphemes)
		lcs_length = longest_common_subsequence("කරණ", "කරණල")
		assert lcs_length == 3

	def test_lcs_sinhala_deletion(self):
		# "කරණල" vs "කරණ" - shares "කරණ" (3 graphemes)
		lcs_length = longest_common_subsequence("කරණල", "කරණ")
		assert lcs_length == 3

	def test_lcs_grapheme_aware_tamil(self):
		# "ஸ்ரீ" (1 grapheme) vs "ரீ" (1 grapheme) - no common graphemes
		lcs_length = longest_common_subsequence("ஸ்ரீ", "ரீ")
		assert lcs_length == 0

	def test_lcs_grapheme_aware_sinhala_complex(self):
		# Complex Sinhala with conjuncts
		# "ක්‍රම" (2 graphemes) vs "කම" (2 graphemes) - share "ම" (1 grapheme)
		lcs_length = longest_common_subsequence("ක්‍රම", "කම")
		assert lcs_length == 1

	def test_lcs_longer_sequence(self):
		# "abcdef" and "fbdamn" share "bd" (2 graphemes)
		assert longest_common_subsequence("abcdef", "fbdamn") == 2

	def test_lcs_single_grapheme_match(self):
		# "කතා" (3 graphemes) and "කරම" (3 graphemes) share "ක" (1 grapheme)
		lcs_length = longest_common_subsequence("කතා", "කරම")
		assert lcs_length == 1

	def test_lcs_all_different(self):
		# Strings with no common graphemes
		lcs_length = longest_common_subsequence("අඉඋ", "එඔඕ")
		assert lcs_length == 0


class TestCharBLEU:
	def test_charbleu_exact_match(self):
		# Identical strings should have CharBLEU of 1.0
		score = charbleu("එවන්න", "එවන්න")
		assert score == 1.0

	def test_charbleu_empty_strings(self):
		# Both empty strings are identical
		score = charbleu("", "")
		assert score == 1.0

	def test_charbleu_empty_reference(self):
		# Empty reference with non-empty hypothesis
		score = charbleu("", "එවන්න")
		assert score == 0.0

	def test_charbleu_empty_hypothesis(self):
		# Non-empty reference with empty hypothesis
		score = charbleu("එවන්න", "")
		assert score == 0.0

	def test_charbleu_single_grapheme_match(self):
		# Single matching grapheme
		score = charbleu("ක", "ක")
		assert score == 1.0

	def test_charbleu_no_match(self):
		# Completely different graphemes
		score = charbleu("අ", "ඉ")
		assert score == 0.0

	def test_charbleu_partial_match(self):
		# Strings with some matching graphemes
		# "කරණ" vs "කරම" - first two graphemes match
		score = charbleu("කරණ", "කරම")
		assert 0 < score < 1

	def test_charbleu_substring_match(self):
		# Hypothesis is substring of reference - scores high since it's a perfect substring match
		score = charbleu("කරණල", "කරණ")
		assert 0 < score <= 1

	def test_charbleu_longer_hypothesis(self):
		# Hypothesis longer than reference
		score = charbleu("කරණ", "කරණල")
		assert 0 < score < 1

	def test_charbleu_sinhala_text(self):
		# Test with longer Sinhala text
		ref = "කරණල"
		hyp = "කරමල"
		score = charbleu(ref, hyp)
		assert 0 < score < 1

	def test_charbleu_tamil_text(self):
		# Test with Tamil text
		score = charbleu("ஸ்ரீ", "ஸ்ரீ")
		assert score == 1.0

	def test_charbleu_tamil_partial_match(self):
		# Tamil with no common graphemes returns 0
		score = charbleu("ஸ்ரீ", "ரீ")
		assert score == 0.0

	def test_charbleu_single_character_change(self):
		# Single character difference
		score = charbleu("abc", "abd")
		assert 0 < score < 1

	def test_charbleu_transposition(self):
		# Characters transposed - unigram precision is still 1.0 since same characters
		# but bigram and trigram precisions are lower, affecting overall score
		score1 = charbleu("abc", "abc")
		score2 = charbleu("abc", "bac")
		# Both should have high scores since all unigrams match, but exact match should be >= transposition
		assert score1 >= score2

	

	def test_charbleu_weights_parameter(self):
		# Test with custom weights
		ref = "අබ"
		hyp = "අ"
		# Uniform weights (default)
		score1 = charbleu(ref, hyp)
		# Emphasize unigrams
		score2 = charbleu(ref, hyp, weights=[1.0, 0.0, 0.0, 0.0])
		assert score1 is not None and score2 is not None

	def test_charbleu_max_n_parameter(self):
		# Test with different max_n values
		ref = "hello"
		hyp = "hello"
		score2 = charbleu(ref, hyp, max_n=2)
		score4 = charbleu(ref, hyp, max_n=4)
		# Both should be 1.0 for exact match regardless of max_n
		assert score2 == 1.0 and score4 == 1.0

	def test_charbleu_similarity_property(self):
		# CharBLEU should be symmetric-like for same strings
		ref = "කරණ"
		hyp = "කරණ"
		assert charbleu(ref, hyp) == charbleu(hyp, ref)

	def test_charbleu_bounded(self):
		# CharBLEU should always be between 0 and 1
		test_cases = [
			("abc", "xyz"),
			("කරණ", "ම"),
			("hello", "hallo"),
			("ஸ்ரீ", "ஸ्ری"),
		]
		for ref, hyp in test_cases:
			score = charbleu(ref, hyp)
			assert 0 <= score <= 1, f"CharBLEU out of bounds for {ref} vs {hyp}: {score}"


if __name__ == "__main__":
	pytest.main([__file__, "-v"])
