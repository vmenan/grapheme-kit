import pytest

from graphemes_plusplus.decomposer import Decomposer, decompose


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])