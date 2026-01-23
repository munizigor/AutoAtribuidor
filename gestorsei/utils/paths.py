# gestorsei/utils/paths.py
from pathlib import Path

def base_dir() -> Path:
    # gestorsei/utils/paths.py -> gestorsei/ -> projeto/
    return Path(__file__).resolve().parents[2]

def full_path(relative: str | Path) -> Path:
    relative = Path(relative)
    return (base_dir() / relative).resolve()
