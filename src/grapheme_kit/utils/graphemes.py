import grapheme



class GraphemeSplitter:
    """
    Standardized Grapheme Clustering class.
    Extends 'grapheme' library to handle "க்ஷ", "ஸ்ரீ", "ஶ்ரீ" and sinhala ZWJ.
    """
    @staticmethod
    def split(string: str) -> list[str]:
        """
        Returns a list of grapheme clusters from the given string.
        """


        if not string:
            return []

        # Optimization: Only run merge logic if problematic clusters exist
        #if not ("க்ஷ" in string or "ஸ்ரீ" in string or "ஶ்ரீ" in string):
        #    return list(grapheme.graphemes(string))

        original_clusters = list(grapheme.graphemes(string))
        result = []
        i = 0
        while i < len(original_clusters):
            current = original_clusters[i]

            # Look ahead for merging opportunities
            if i < len(original_clusters) - 1:
                next_cluster = original_clusters[i + 1]

                # Case 1: க் + ஷ... -> க்ஷ...
                if current == "க்" and next_cluster.startswith("ஷ"):
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Case 2: ஸ் + ரீ -> ஸ்ரீ
                if current == "ஸ்" and next_cluster == "ரீ":
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # Case 3: ஶ் + ரீ -> ஶ்ரீ
                if current == "ஶ்" and next_cluster == "ரீ":
                    result.append(current + next_cluster)
                    i += 2
                    continue

                # for sinhala graphemes

                if "\u200d" in current:
                  if current == "ර්\u200d":
                    current='ර්'
                    original_clusters[i] = current
                  i+=1
                  x=current

                  while "\u200d" in original_clusters[i-1]:
                    x+=original_clusters[i]
                    i+=1
                  result.append(x)
                  continue

            # No merge opportunity, add the current cluster
            if i == len(original_clusters)-1 and "\u200d" in current:
              new=current.replace("\u200d","")
              result.append(new)
            else:
              result.append(current)
            i += 1

        return result