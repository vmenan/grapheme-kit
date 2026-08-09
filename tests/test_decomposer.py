import pytest

from grapheme_kit.decomposer import Decomposer, decompose


class TestDecomposer:
    def test_decompose_tamil_consonant(self):
        assert decompose("க") == "க்அ"

    def test_decompose_tamil_vowel_sign(self):
        assert decompose("கா") == "க்ஆ"

    def test_decompose_sinhala_consonant(self):
        assert Decomposer.decompose("ක") == "ක්අ"

    def test_decompose_sinhala_vowel_sign(self):
        assert Decomposer.decompose("කා") == "ක්ආ"

    def test_decompose_keeps_spaces_and_punctuation(self):
        assert decompose("கா, hello!") == "க்ஆ, hello!"

    @pytest.mark.parametrize(
        "text",
        ["க", "கா", "ක", "කා", "hello 123"],
    )
    def test_decompose_round_trip_input_stays_segmentable(self, text):
        assert isinstance(decompose(text), str)

    def test_decompose_preserves_ascii(self):
        assert decompose("hello 123") == "hello 123"

    @pytest.mark.parametrize(
        "char",
        [
            "ஃ",   # U+0B83 aytham -- neither uyir nor mei
            "ௐ",   # U+0BD0 om
            "௧",   # U+0BE7 digit one
            "௯",   # U+0BEF digit nine
            "௰",   # U+0BF0 number ten
            "௹",   # U+0BF9 rupee sign
            "௺",   # U+0BFA number sign
        ],
    )
    def test_decompose_tamil_non_consonant_gives_itself(self, char):
        """Anything in the Tamil block that is not a consonant has no
        mei + uyir split, so decomposition must leave it untouched."""
        assert decompose(char) == char

    @pytest.mark.parametrize(
        "text,expected",
        [
            ("ஃபு", "ஃப்உ"),
            ("அஃது", "அஃத்உ"),
            ("எஃகு", "எஃக்உ"),
        ],
    )
    def test_decompose_aytham_in_word(self, text, expected):
        assert decompose(text) == expected

    def test_decompose_tamil_consonant_still_splits(self):
        """The guard must not stop real consonants from decomposing."""
        assert decompose("க") == "க்அ"
        assert decompose("ஷ") == "ஷ்அ"
        assert decompose("ஹ") == "ஹ்அ"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])