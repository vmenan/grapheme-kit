from grapheme import graphemes
import pytest
import random
from pathlib import Path
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

	@pytest.mark.parametrize("word_length", [3, 4, 5, 6, 7])
	@pytest.mark.parametrize(
		"grapheme_file",
		["tests/Sinhala_graphemes.txt", "tests/Tamil_graphemes.txt"],
	)
	def test_grapheme_count_matches_generated_word_length(self, word_length, grapheme_file):
		# Load newline-delimited graphemes from the provided file.
		loaded_graphemes = []
		project_root = Path(__file__).resolve().parents[1]
		file_path = Path(grapheme_file)
		if not file_path.is_absolute():
			file_path = project_root / file_path

		if not file_path.exists():
			pytest.skip(f"Grapheme file not found: {file_path}")

		with file_path.open("r", encoding="utf-8") as f:
			loaded_graphemes.extend(line.strip() for line in f if line.strip())

		assert loaded_graphemes, "No graphemes loaded from the provided file."
		selected_graphemes = random.choices(loaded_graphemes, k=word_length)
		random_word = "".join(selected_graphemes)

		# Get graphemes from the word
		result = Graphemizer(random_word)
		selected_graphemes_text = "[" + ", ".join(repr(g) for g in selected_graphemes) + "]"
		loaded_graphemes_text = "[" + ", ".join(repr(g) for g in loaded_graphemes) + "]"

		# Assert the list size matches expected length
		assert len(result) == word_length, \
			f"Expected {word_length} graphemes, got {len(result)} from word: {random_word}. " \
			f"Selected graphemes list: {selected_graphemes_text}. Source file: {file_path}. " \
			f"Loaded graphemes list: {loaded_graphemes_text}"


if __name__ == "__main__":
	pytest.main([__file__, "-v"])
