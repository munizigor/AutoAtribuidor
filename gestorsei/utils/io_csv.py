# gestorsei/utils/io_csv.py
import csv
from pathlib import Path
from typing import Iterable

def read_csv_rows(csv_path: Path) -> Iterable[list[str]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            yield row

def write_csv(csv_path: Path, header: list[str], rows: Iterable[list[str]]):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
