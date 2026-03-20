from typing import List, Sequence, Optional, Dict, Union
from collections import Counter
from sacrebleu.metrics.chrf import CHRF
from sacrebleu.metrics.helpers import extract_word_ngrams
from graphemes_plusplus.distance import levenshtein
from graphemes_plusplus.graphemizer import Graphemizer


def extract_all_grapheme_ngrams(
    graphemes: List[str], max_order: int, include_whitespace: bool = False) -> List[Counter]:
    """Extracts all grapheme n-grams at once for convenience.

    :param graphemes: A list of grapheme clusters (acting as characters).
    :param max_order: The maximum order of the n-grams.
    :param include_whitespace: If True, keep whitespace graphemes.
    :return: a list of Counter objects containing ngrams and counts.
    """
    counters = []

    if not include_whitespace:
        graphemes = [g for g in graphemes if g.strip() != ""]

    for n in range(1, max_order + 1):
        ngrams = Counter([tuple(graphemes[i:i + n]) for i in range(len(graphemes) - n + 1)])
        counters.append(ngrams)

    return counters


class GraphemeCHRF(CHRF):
    """Computes the chrF(++) metric at the grapheme level.

    Accepts raw text strings and automatically segments them into grapheme
    clusters using Graphemizer before computing n-gram statistics.

    This ensures proper handling of complex scripts like Tamil, Sinhala,
    and other Indic languages where a single visual character may consist
    of multiple Unicode code points.
    """

    def _graphemize(self, text: str) -> List[str]:
        """Convert a text string to a list of grapheme clusters.

        :param text: Input text string.
        :return: List of grapheme clusters.
        """
        return list(Graphemizer(text))

    def _preprocess_segment(self, sent: Union[str, List[str]]) -> List[str]:
        """Given a string or list of graphemes, graphemize if needed and apply optional lowercasing.

        :param sent: Input segment (string or list of graphemes).
        :return: List of grapheme clusters.
        """
        # Convert string to graphemes if needed
        if isinstance(sent, str):
            graphemes = self._graphemize(sent)
        else:
            graphemes = sent

        return [g.lower() for g in graphemes] if self.lowercase else graphemes

    def _remove_punctuation_for_words(self, graphemes: List[str]) -> List[str]:
        """Reconstructs the sentence and separates out punctuations from words."""
        reconstructed_string = "".join(graphemes)
        return super()._remove_punctuation(reconstructed_string)

    def _extract_reference_info(self, refs: Sequence[str]) -> Dict[str, List[List[Counter]]]:
        """Given a list of reference strings, extract the grapheme and word n-grams.

        :param refs: A sequence of reference strings.
        :return: Dictionary containing reference n-grams.
        """
        ngrams = []

        for ref in refs:
            # Preprocess converts string to graphemes
            ref_graphemes = self._preprocess_segment(ref)
            stats = extract_all_grapheme_ngrams(ref_graphemes, self.char_order, self.whitespace)

            if self.word_order > 0:
                ref_words = self._remove_punctuation_for_words(ref_graphemes)
                for n in range(self.word_order):
                    stats.append(extract_word_ngrams(ref_words, n + 1))

            ngrams.append(stats)

        return {'ref_ngrams': ngrams}

    def _compute_segment_statistics(self, hypothesis: str, ref_kwargs: Dict) -> List[int]:
        """Given a hypothesis string and reference n-grams, returns best match statistics.

        :param hypothesis: Hypothesis string.
        :param ref_kwargs: Dictionary with precomputed reference n-grams.
        :return: List of match statistics.
        """
        best_stats = []
        best_f_score = -1.0

        # Preprocess converts string to graphemes
        hyp_graphemes = self._preprocess_segment(hypothesis)
        all_hyp_ngrams = extract_all_grapheme_ngrams(
            hyp_graphemes, self.char_order, self.whitespace)

        if self.word_order > 0:
            hwords = self._remove_punctuation_for_words(hyp_graphemes)
            _range = range(1, self.word_order + 1)
            all_hyp_ngrams.extend([extract_word_ngrams(hwords, n) for n in _range])

        for _ref_ngrams in ref_kwargs['ref_ngrams']:
            stats = []
            for h, r in zip(all_hyp_ngrams, _ref_ngrams):
                stats.extend(self._get_match_statistics(h, r))
            f_score = self._compute_f_score(stats)

            if f_score > best_f_score:
                best_f_score = f_score
                best_stats = stats

        return best_stats

def CER(hypothesis: str, reference: str) -> float:
    """Computes the Character Error Rate (CER) between a hypothesis and reference string.

    CER is defined as the Levenshtein distance at the grapheme level divided by the number of graphemes in the reference.

    :param hypothesis: The hypothesis string.
    :param reference: The reference string.
    :return: The CER value as a float.
    """
    hyp_graphemes = list(Graphemizer(hypothesis))
    ref_graphemes = list(Graphemizer(reference))

    if len(ref_graphemes) == 0:
        return 0.0 if len(hyp_graphemes) == 0 else 1.0

    distance = levenshtein(hypothesis, reference)
    return distance / len(ref_graphemes)