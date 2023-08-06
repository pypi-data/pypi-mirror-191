from dataclasses import dataclass
from enum import Enum


@dataclass
class Result:
    sequence: str
    matchResult: str
    match_type: str
    start: int
    end: float
    file_name: str


@dataclass
class WriteMode(Enum):
    Text = "text"
    CSV = "csv"
    duckdb = "duckdb"
    Nothing = "none"
