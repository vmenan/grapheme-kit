from grapheme import graphemes
import pytest
import random
import re
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
			("வெள்ளை", 3),
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
			for line in f:
				cleaned = line.strip()
				if cleaned and not cleaned.startswith("--"):
					loaded_graphemes.append(cleaned)

		assert loaded_graphemes, "No graphemes loaded from the provided file."
		selected_graphemes = random.choices(loaded_graphemes, k=word_length)
		random_word = "".join(selected_graphemes)

		# Get graphemes from the word
		result = Graphemizer(random_word)
		selected_graphemes_text = "[" + ", ".join(repr(g) for g in selected_graphemes) + "]"
		loaded_graphemes_text = "[" + ", ".join(repr(g) for g in loaded_graphemes) + "]"

		# Calculate expected length taking into account possible grapheme mergers
		expected = word_length
		tamil_dependent_vowels = ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ', '்']
		
		i = 0
		while i < len(selected_graphemes) - 1:
			current = selected_graphemes[i]
			nxt = selected_graphemes[i+1]
			
			# Case 1: க் + ஷ... -> க்ஷ...
			if current == "க்" and nxt.startswith("ஷ"):
				expected -= 1
				i += 1
			# Case 2: ஸ் + ரீ -> ஸ்ரீ
			elif current == "ஸ்" and nxt == "ரீ":
				expected -= 1
				i += 1
			# Case 3: ஶ் + ரீ -> ஶ்ரீ
			elif current == "ஶ்" and nxt == "ரீ":
				expected -= 1
				i += 1
			# Case 4: ெள -> ௌ
			elif current.endswith("ெ") and nxt.startswith("ள"):
				following_char = ""
				if len(nxt) > 1:
					following_char = nxt[1]
				elif i + 2 < len(selected_graphemes):
					following_char = selected_graphemes[i+2][0]
					
				if following_char not in tamil_dependent_vowels:
					expected -= 1
					i += 1
			i += 1

		assert len(result) == expected, \
			f"Expected {expected} graphemes, got {len(result)} from word: {random_word}. " \
			f"Selected graphemes list: {selected_graphemes_text}. Source file: {file_path}. " \
			f"Loaded graphemes list: {loaded_graphemes_text}"


if __name__ == "__main__":
	pytest.main([__file__, "-v"])
