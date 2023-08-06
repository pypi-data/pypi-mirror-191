from pathlib import Path
from typing import List


def read_fixture(path: str) -> List[str]:
    fixture_path = Path(__file__).parent / f"fixtures/{path}"
    return fixture_path.read_text().splitlines()
