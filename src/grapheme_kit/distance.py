import textdistance

from grapheme_kit.graphemizer import Graphemizer


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


def damerau_levenshtein(s1: str, s2: str) -> int:
    """
    Grapheme-aware Damerau-Levenshtein distance between two strings.
    
    This metric accounts for insertions, deletions, substitutions, and 
    transpositions (swapping adjacent graphemes) as single edit operations.
    """
    return textdistance.damerau_levenshtein.distance(list(Graphemizer(s1)), list(Graphemizer(s2)))


def jaro(s1: str, s2: str) -> float:
    """
    Grapheme-aware Jaro similarity between two strings.
    
    Returns a similarity score between 0 and 1, where 1 indicates identical strings.
    The Jaro similarity measures the proportion of matching characters and 
    penalizes transpositions.
    """
    return textdistance.jaro.similarity(list(Graphemizer(s1)), list(Graphemizer(s2)))


def jaro_winkler(s1: str, s2: str) -> float:
    """
    Grapheme-aware Jaro-Winkler similarity between two strings.
    
    Returns a similarity score between 0 and 1, where 1 indicates identical strings.
    Jaro-Winkler is a variant of Jaro that gives more weight to matching prefixes,
    making it particularly useful for typo detection in names and short strings.
    """
    return textdistance.jaro_winkler.similarity(list(Graphemizer(s1)), list(Graphemizer(s2)))


def longest_common_subsequence(s1: str, s2: str) -> int:
    """
    Grapheme-aware Longest Common Subsequence (LCS) length between two strings.
    
    Returns the length of the longest subsequence that appears in both strings
    in the same order, but not necessarily consecutively. A subsequence is 
    obtained by deleting some (or no) elements from a sequence without changing 
    the order of the remaining elements.
    
    This function counts the number of matching graphemes, not Unicode characters.
    """
    g1 = list(Graphemizer(s1))
    g2 = list(Graphemizer(s2))
    
    # Since graphemes can be multi-character strings, we need to ensure
    # we're counting graphemes, not characters. We do this by using indices.
    # Create indexed tuples: [(0, grapheme), (1, grapheme), ...]
    indexed_g1 = [(i, g) for i, g in enumerate(g1)]
    indexed_g2 = [(i, g) for i, g in enumerate(g2)]
    
    lcs = textdistance.LCSSeq()
    
    # We need to compare based on the grapheme content, not the index
    # So we create a custom comparison using just the graphemes
    # Actually, let's use a simpler approach: compare grapheme by grapheme
    # and build the LCS manually
    
    # Use dynamic programming to compute LCS length
    m, n = len(g1), len(g2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if g1[i - 1] == g2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


if __name__ == "__main__":
    print(levenshtein("ஸ்ரீ", "ஸ்ரி"))
    print(hamming("ஸ்ரீ", "ஸ்ரீ"))
    print(hamming("රැ", "රැහ"))
    print(levenshtein("ක්‍රම", "කම"))

