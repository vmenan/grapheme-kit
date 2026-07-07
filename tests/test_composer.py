import pytest

from graphemes_plusplus.decomposer import decompose
from graphemes_plusplus.composer import Composer, compose


class TestComposer:
    def test_compose_tamil_consonant(self):
        assert compose("க்அ") == "க"

    def test_compose_tamil_standalone_vowel(self):
        assert compose("அ") == "அ"

    def test_compose_tamil_vowel_sign(self):
        assert compose("க்ஆ") == "கா"

    def test_compose_tamil_short_vowel_sign(self):
        assert compose("க்இ") == "கி"

    def test_compose_sinhala_consonant(self):
        assert Composer.compose("ක්අ") == "ක"

    def test_compose_sinhala_standalone_vowel(self):
        assert Composer.compose("අ") == "අ"

    def test_compose_sinhala_vowel_sign(self):
        assert Composer.compose("ක්ආ") == "කා"

    def test_compose_sinhala_short_vowel_sign(self):
        assert Composer.compose("ක්උ") == "කු"

    def test_compose_preserves_ascii(self):
        assert compose("hello 123") == "hello 123"

    def test_compose_preserves_tamil_punctuation(self):
        assert compose("க்இ, உலகம்!") == "கி, உலகம்!"

    def test_compose_keeps_spaces_and_punctuation(self):
        assert compose("க்ஆ, hello!") == "கா, hello!"

    @pytest.mark.parametrize(
        "text",
        ["க", "கா", "கி", "අ", "ಕ", "ක", "කා", "කි", "hello 123"],
    )
    def test_compose_after_decompose_round_trip(self, text):
        assert compose(decompose(text)) == text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])