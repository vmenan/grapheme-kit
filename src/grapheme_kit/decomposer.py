import re
from grapheme_kit.graphemizer import Graphemizer
from grapheme import graphemes

class Decomposer:
    """
    A class to handle the grapheme decomposition and composition for Sinhala and Tamil text.
    It encapsulates language-specific phonetic rules, allowing for proper character-level
    transformations needed for NLP tokenization and metric evaluation.
    """

    SINHALA_VOWELS = [
        'අ', 'ආ', 'ඇ', 'ඈ', 'ඉ', 'ඊ', 'උ', 'ඌ',
        'ඍ', 'ඎ', 'එ', 'ඒ', 'ඓ', 'ඔ', 'ඕ', 'ඖ',
        'අං', 'අඃ',
    ]

    SINHALA_ACCENT_SYMBOLS = [
        '', 'ා', 'ැ', 'ෑ', 'ի', 'ී', 'ු', 'ූ', 'ෘ',
        'ෲ', 'ෙ', 'ේ', 'ෛ', 'ො', 'ෝ', 'ෞ',
        'ං', 'ඃ'
    ]

    # specifc for sinhala
    ZWJ_CHARS = ['ක්ව්', 'ක්ෂ්', 'ග්ධ්', 'ට්ඨ්', 'ත්ව්', 'ත්ථ්', 'ද්ධ්', 'න්ථ්', 'න්ද්', 'න්ධ්', 'ර්', 'ය්']

    TAMIL_VOWELS = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
    TAMIL_ACCENT_SYMBOLS = ["", "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ"]

    # Tamil consonants (mei) occupy U+0B95 (க) .. U+0BB9 (ஹ). Everything else
    # in the Tamil block is not a consonant -- the aytham ஃ, the digits ௦-௯,
    # the numeric signs ௰-௺, ௐ, and any combining sign standing on its own --
    # so it has no mei + uyir split and decomposes to itself.
    TAMIL_CONSONANT_FIRST = "க"
    TAMIL_CONSONANT_LAST = "ஹ"

    @classmethod
    def _is_tamil_consonant(cls, char: str) -> bool:
        """True if the grapheme is built on a Tamil consonant (mei)."""
        return bool(char) and (
            cls.TAMIL_CONSONANT_FIRST <= char[0] <= cls.TAMIL_CONSONANT_LAST
        )

    @staticmethod
    def _is_sinhala(chars: str) -> bool:
        """Check if all characters in the string are Sinhala characters or ZWJ based on Unicode range."""
        if not chars:
            return False
        return all('\u0D80' <= c <= '\u0DFF' or c == '\u200d' for c in chars)

    @staticmethod
    def _is_tamil(chars: str) -> bool:
        """Check if all characters in the string are Tamil characters or ZWJ based on Unicode range."""
        if not chars:
            return False
        return all('\u0B80' <= c <= '\u0BFF' or c == '\u200d' for c in chars)


    @classmethod
    def _decompose_sinhala_character(cls, char: str) -> list[str]:
        base_char = '්'

        if char in cls.SINHALA_VOWELS:
            return [char, ""]

        if len(char) == 1:
            return [char + base_char, cls.SINHALA_VOWELS[0]]
        elif len(char) == 2 and char[1] in cls.SINHALA_ACCENT_SYMBOLS:
            return [char[0] + base_char, cls.SINHALA_VOWELS[cls.SINHALA_ACCENT_SYMBOLS.index(char[1])]]
        elif '\u200d' in char:
            newchar = char[char.find('\u200d') + 1:]
            return [char[0] + base_char] + cls._decompose_sinhala_character(newchar)
        else:
            return [char]

    @classmethod
    def _decompose_tamil_character(cls, char: str) -> list[str]:
        base_char = '்'

        if char in cls.TAMIL_VOWELS:
            return [char, ""]

        # Already a complete grapheme with no consonant to split off: leave it be.
        if not cls._is_tamil_consonant(char):
            return [char]

        if len(char) == 1:
            return [char + base_char, cls.TAMIL_VOWELS[0]]
        elif len(char) == 2 and char[1] == base_char:
            return [char]
        elif len(char) == 2 and char[1] in cls.TAMIL_ACCENT_SYMBOLS:
            return [char[0] + base_char, cls.TAMIL_VOWELS[cls.TAMIL_ACCENT_SYMBOLS.index(char[1])]]
        else:
            gr = list(graphemes(char))
            if len(gr) == 2:
                return cls._decompose_tamil_character(gr[0]) + cls._decompose_tamil_character(gr[1])
            raise ValueError("Not a valid single Tamil character grapheme!")

    @classmethod
    def decompose(cls, text: str) -> str:
        """
        Decomposes Sinhala and Tamil strings into fundamental phonetic sequences.
        Punctuations and spaces are unaffected.
        """
        gr = list(Graphemizer(text))
        new_string = ""
        for each_char in gr:
            if cls._is_sinhala(each_char):
                new_string += "".join(cls._decompose_sinhala_character(each_char))
            elif cls._is_tamil(each_char):
                new_string += "".join(cls._decompose_tamil_character(each_char))
            else:
                new_string += each_char

        return new_string


# For backward compatibility / ease of use directly from the module
def decompose(text: str) -> str:
    return Decomposer.decompose(text)
