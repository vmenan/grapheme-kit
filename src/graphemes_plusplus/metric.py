from typing import List, Sequence, Optional, Dict
from collections import Counter
from sacrebleu.metrics.chrf import CHRF
from sacrebleu.metrics.helpers import extract_word_ngrams


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
    """Computes the chrF(++) metric given hypotheses and references at the grapheme level.
    Instead of passing strings, you must pass Lists of Strings where each string
    is a grapheme cluster.
    """
    
    def _check_sentence_score_args(self, hyp: List[str], refs: Sequence[List[str]]):
        prefix = self.__class__.__name__
        err_msg = None

        if not isinstance(hyp, list):
            err_msg = "The argument `hyp` should be a list of grapheme strings."
        elif not isinstance(refs, Sequence):
            err_msg = "The argument `refs` should be a sequence of lists of graphemes."

        if err_msg:
            raise TypeError(f"{prefix}: {err_msg}")

    def _check_corpus_score_args(self, hyps: Sequence[List[str]], refs: Optional[Sequence[Sequence[List[str]]]]):
        """Bypass the strict string check to allow sequences of lists of graphemes."""
        prefix = self.__class__.__name__
        err_msg = None

        if not isinstance(hyps, Sequence):
            err_msg = "`hyps` should be a sequence of lists of graphemes."
        
        if refs is not None and not isinstance(refs, Sequence):
            err_msg = "`refs` should be a sequence of sequence of lists of graphemes."

        if err_msg:
            raise TypeError(f"{prefix}: {err_msg}")

    def _preprocess_segment(self, sent: List[str]) -> List[str]:
        """Given a list of graphemes, apply optional lowercasing."""
        return [g.lower() for g in sent] if self.lowercase else sent

    def _remove_punctuation_for_words(self, sent: List[str]) -> List[str]:
        """Reconstructs the sentence and separates out punctuations from words."""
        reconstructed_string = "".join(sent)
        return super()._remove_punctuation(reconstructed_string)

    def _extract_reference_info(self, refs: Sequence[List[str]]) -> Dict[str, List[List[Counter]]]:
        """Given a list of reference grapheme lists, extract the grapheme and word n-grams."""
        ngrams = []

        for ref in refs:
            stats = extract_all_grapheme_ngrams(ref, self.char_order, self.whitespace)

            if self.word_order > 0:
                ref_words = self._remove_punctuation_for_words(ref)
                for n in range(self.word_order):
                    stats.append(extract_word_ngrams(ref_words, n + 1))

            ngrams.append(stats)

        return {'ref_ngrams': ngrams}

    def _compute_segment_statistics(self, hypothesis: List[str], ref_kwargs: Dict) -> List[int]:
        """Given a hypothesis grapheme list and reference n-grams, returns best match."""
        best_stats = []
        best_f_score = -1.0

        all_hyp_ngrams = extract_all_grapheme_ngrams(
            hypothesis, self.char_order, self.whitespace)

        if self.word_order > 0:
            hwords = self._remove_punctuation_for_words(hypothesis)
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
 