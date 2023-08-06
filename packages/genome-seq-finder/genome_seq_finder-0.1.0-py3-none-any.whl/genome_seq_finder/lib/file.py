from Bio import SeqIO
from os import path, makedirs
import duckdb
import pandas as pd

from .types import Result, WriteMode


class File:
    def read_text(self, file_path: str) -> list[str]:
        with open(file_path, "r") as f:
            return f.readlines()

    def parse_fasta_file(self, file_path: str) -> str:
        for seq_record in SeqIO.parse(file_path, "fasta"):
            return seq_record.seq.__str__()

    def write(
        self,
        writePath: str,
        file_name: str,
        content: list[Result],
        write_mode: WriteMode,
    ):
        if len(content) == 0:
            print("No results to save")
            return

        if not path.exists(writePath):
            makedirs(writePath)

        match write_mode.name:
            case WriteMode.Text.name:
                self.write_text(
                    file_name=f"{writePath}/{file_name}.txt", content=content
                )
            case WriteMode.CSV.name:
                self.write_csv(file_name=f"{writePath}{file_name}.csv", content=content)
            case WriteMode.duckdb.name:
                self.write_duckdb(
                    file_name=f"{writePath}results.duckdb", content=content
                )

    def write_csv(self, file_name, content):
        output = pd.DataFrame(content)
        output.to_csv(file_name, index=False)

    def write_duckdb(self, file_name, content):
        output = pd.DataFrame(content)
        with duckdb.connect(database=file_name, read_only=False) as con:
            if len(con.execute("show tables").fetchall()) == 0:
                con.execute("CREATE TABLE results AS SELECT *, now() as create_date FROM output")
            else:
                con.execute("INSERT INTO results SELECT *, now() as create_date FROM output")

    def write_text(self, file_name, content):
        with open(file_name, "w") as f:
            for line in content:
                f.write(f"{str(line)}\n")
