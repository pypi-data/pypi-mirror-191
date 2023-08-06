import re
from .types import Result


class SeqFinder:
    def __init__(self, debug: bool):
        self.debug = debug

    def find_sequence(
        self,
        text: str,
        sequence: str,
        file_name: str,
        before: int = 50,
        after: int = 50,
    ) -> list[Result]:
        found_sequences = []
        x = re.finditer(sequence, text)

        for m in x:
            start = m.start() - before
            end = m.end() + after
            if start < 0:
                start = 0
            if end > len(text):
                end = len(text) - 1

            result = Result(
                sequence=sequence,
                matchResult=text[m.start() : m.end()],
                start=start,
                end=end,
                file_name=file_name,
                match_type=m.lastgroup,
            )
            found_sequences.append(result)

            if self.debug:
                print(f"{m.span()} with sequence {text[start:end]}")

        return found_sequences
