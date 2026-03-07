import textdistance

from graphemes_plusplus.graphemizer import Graphemizer


def levenshtein(s1: str, s2: str) -> int:
    """
    Grapheme-aware Levenshtein distance between two strings.
    """
    return textdistance.levenshtein.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))


def hamming(s1: str, s2: str) -> int:
    """
    Grapheme-aware Hamming distance between two strings.
    Strings must have equal number of graphemes.
    """
    return textdistance.hamming.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))



if __name__ == "__main__":
    print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
    print(hamming("ஸ்ரீ", "ஸ்ரீ"))