from .lib.seq_finder import SeqFinder
from .lib.file import File
from .lib.types import Result, WriteMode
from pathlib import Path
import typer
from time import time, asctime
import concurrent.futures as cf
from concurrent.futures import ProcessPoolExecutor

app = typer.Typer()
fileProcessor = File()
MAXCORES = 10


# TODO: Allow to parallelize the work between cores
def run_parallel(max_workers, func, lines):
    """
    For each line runs the process_line function yielding a future.
    When completed it yields the result of the process_line
    Can set the max number of process that can run simultaneosly with num_workers
    """
    with ProcessPoolExecutor(max_workers=max_workers) as p:
        futures = {p.submit(func, line) for line in lines}
        for future in cf.as_completed(futures):
            yield future.result()


# TODO: Command to accept with 1 or more permutations


@app.command("generate")
def generate_mutations(
    patternFile: str = typer.Option(
        "patterns.txt", "--patternFile", case_sensitive=False
    ),
    debug: bool = typer.Option(False, "--debug"),
):
    """
    TODO: Given a list of patterns generate list with all single letter mutations
    """
    mutations = []
    letters = ["A", "C", "T", "G"]
    patterns = fileProcessor.read_text(patternFile)
    for pattern in patterns:
        print(pattern)
        clean_pattern = pattern.strip()
        for index, gene in enumerate(clean_pattern):
            if gene in letters:
                for letter in letters:
                    new_pattern = (
                        f"{clean_pattern[:index]}{letter}{clean_pattern[index +1:]}"
                    )
                    mutations.append(new_pattern)

                    if debug:
                        print(new_pattern)

    fileProcessor.write("results/", "patterns", mutations, WriteMode.Text)


@app.command()
def find(
    dir: str = typer.Option("data", "--dir"),
    patternFile: str = typer.Option(
        "patterns.txt", "--patternFile", case_sensitive=False
    ),
    write_mode: WriteMode = typer.Option(
        WriteMode.Nothing, "--output", case_sensitive=False
    ),
    debug: bool = typer.Option(False, "--debug"),
):
    """
    Given some patterns and a folder with the FNA files it checks for the pattern.
    The output can be written to a file if necessary
    """
    seq_finder = SeqFinder(debug)
    dirList = [x for x in Path(dir).glob("**/*.fna")]

    patterns = fileProcessor.read_text(patternFile)

    for pattern in patterns:
        start = time()
        results: list[Result] = []
        for file in dirList:
            file_results = process_file(pattern.strip(), seq_finder, file)

            results.extend(file_results)

        fileProcessor.write("results/", asctime(), results, write_mode)
        diff = time() - start
        print(f"Run for pattern {pattern} in {diff}s")


def process_file(pattern, seq_finder, file):
    print(f"Searching on file {file}")
    seq = fileProcessor.parse_fasta_file(file)
    start = time()
    file_results = seq_finder.find_sequence(seq, pattern, file_name=file)
    diff = time() - start
    print(f"Run for {file} in {diff}s")
    return file_results


if __name__ == "__main__":
    app()
