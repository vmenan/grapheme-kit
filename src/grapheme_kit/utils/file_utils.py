import os
from grapheme_kit.utils.normalizer import Normalizer


def normalize_file(input_path: str, output_path: str | None = None) -> str:
    """
    Reads input file, normalizes line by line, writes to output file.
    If output_path is not provided, saves as <input>_normalized<ext>.
    """
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_normalized{ext}"

    normalizer = Normalizer()

    with open(input_path, "rt", encoding="utf-8") as fin, \
         open(output_path, "wt", encoding="utf-8") as fout:

        count = 0
        for line in fin:
            fout.write(normalizer.normalize(line))
            count += 1

    return output_path
