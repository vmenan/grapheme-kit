from sacrebleu.metrics.chrf import CHRF
from graphemes_plusplus.graphemizer import Graphemizer


class GraphemeCHRF(CHRF):
    """
    Computes the chrF(++) metric at the grapheme level using Graphemizer.
    """
    
    def separate_characters(self, line):
        """
        Replace the default character separation with grapheme extraction.
        """
        clean_line = line.strip().replace(" ", "")
        graphemes = Graphemizer(clean_line)
        return list(graphemes)
 