"""Load data for Akkadian translation."""

from pathlib import Path


def load_data(path: str):
    """Load dataset from path."""
    p = Path(path)
    return p.read_text(encoding="utf-8").splitlines()
