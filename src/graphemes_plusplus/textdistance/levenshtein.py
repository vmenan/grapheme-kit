def distance(lst1,ls2):
    def levenshteinDistance(reference, hypothesis,m,n):
    # If reference string is empty
        if m == 0:
            return n
        # If hypothesis string is empty
        if n == 0:
            return m
        # If last characters are same
        if reference[m - 1] == hypothesis[n - 1]:
            return levenshteinDistance(reference, hypothesis, m - 1, n - 1)
        # If last characters are different
        return 1 + min(
            # Insert
            levenshteinDistance(reference, hypothesis, m, n - 1),

            # Remove
            levenshteinDistance(reference, hypothesis, m - 1, n),

            # Replace
            levenshteinDistance(reference, hypothesis, m - 1, n - 1)
        )
    return levenshteinDistance(lst1,ls2,len(lst1),len(ls2))