from grapheme_kit.graphemizer import Graphemizer


class Composer:
    """
    A class to handle the grapheme composition for Sinhala and Tamil text.
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
    def _compose_tamil_character(cls, mei: str, uyir: str) -> str:
        if not mei or mei[-1] != '்':
            raise ValueError("Error! Not a valid mei character!")

        if uyir in cls.TAMIL_VOWELS:
            return mei[0] + cls.TAMIL_ACCENT_SYMBOLS[cls.TAMIL_VOWELS.index(uyir)]
        raise ValueError("Error! Cant be merged!")

    @classmethod
    def _compose_sinhala_character(cls, base: str, vowel: str) -> str:
        if vowel not in cls.SINHALA_VOWELS:
            raise ValueError("Error! Not a valid Sinhala vowel!")

        base_clean = base[:-1] if base.endswith('්') else base
        if vowel == 'අ':
            return base_clean
        return base_clean + cls.SINHALA_ACCENT_SYMBOLS[cls.SINHALA_VOWELS.index(vowel)]

    @classmethod
    def compose(cls, text: str) -> str:
        """
        Composes a decomposed sequence of Sinhala or Tamil characters
        back into standard grapheme clusters.
        """
        gr = list(Graphemizer(text))
        new_string = ""
        i = 0

        while i < len(gr):
            current_grapheme = gr[i]

            if cls._is_tamil(current_grapheme):
                if current_grapheme[-1] == '்' and i + 1 < len(gr) and gr[i + 1] in cls.TAMIL_VOWELS:
                    new_string += cls._compose_tamil_character(current_grapheme, gr[i + 1])
                    i += 2
                else:
                    new_string += current_grapheme
                    i += 1

            elif cls._is_sinhala(current_grapheme):
                if current_grapheme in cls.SINHALA_VOWELS:
                    new_string += current_grapheme
                    i += 1
                    continue

                while i + 1 < len(gr) and cls._is_sinhala(gr[i + 1]) and (
                    gr[i] + '\u200d' + gr[i + 1] in cls.ZWJ_CHARS or gr[i + 1] in cls.ZWJ_CHARS
                ):
                    new_string += gr[i] + '\u200d'
                    i += 1

                if i + 1 < len(gr) and gr[i + 1] in cls.SINHALA_VOWELS:
                    new_string += cls._compose_sinhala_character(gr[i], gr[i + 1])
                    i += 2
                else:
                    new_string += gr[i]
                    i += 1

            else:
                new_string += current_grapheme
                i += 1

        return new_string


def compose(text: str) -> str:
    return Composer.compose(text)