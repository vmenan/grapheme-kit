import os
from graphemes_plusplus.utils.normalizer import Normalizer
from graphemes_plusplus.utils.graphemes import GraphemeSplitter


class Graphemizer:
    def __init__(self, string: str) -> None:
        self.normalizer = Normalizer()
        self.splitter = GraphemeSplitter()
        self.raw_string = string
        self._graphemes = self._process_text(string)

    @property
    def graphemes(self) -> list[str]:
        return self._graphemes

    def __iter__(self):
        return iter(self._graphemes)

    def __len__(self) -> int:
        return len(self._graphemes)

    def _process_text(self, raw_text: str) -> list[str]:
        """
        Takes raw string -> Normalize -> Split into Graphemes
        Returns: List of Graphemes
        """
        # 1. Normalize
        normalized_text = self.normalizer.normalize(raw_text)

        # 2. Split
        graphemes = self.splitter.split(normalized_text)
        return graphemes