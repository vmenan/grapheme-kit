import pytest

from grapheme_kit.decomposer import decompose
from grapheme_kit.composer import Composer, compose


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

    def test_compose_aytham_unchanged(self):
        assert compose("ஃ") == "ஃ"

    @pytest.mark.parametrize("text", ["ஃ", "ஃபு", "அஃது", "எஃகு"])
    def test_aytham_round_trip(self, text):
        assert compose(decompose(text)) == text

    def test_compose_keeps_multi_codepoint_conjunct(self):
        """க்ஷ் is a two-consonant conjunct; composing it with a vowel must keep
        the whole cluster, not just its first code point."""
        assert compose("க்ஷ்அ") == "க்ஷ"
        assert compose("க்ஷ்ஆ") == "க்ஷா"

    @pytest.mark.parametrize(
        "text",
        ["க்ஷ", "க்ஷா", "க்ஷி", "க்ஷு", "ஸ்ரீ", "ஶ்ரீ", "ஸ்ரீதர்"],
    )
    def test_conjunct_round_trip(self, text):
        assert compose(decompose(text)) == text

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