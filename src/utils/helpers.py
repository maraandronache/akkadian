"""Misc helper functions."""

def ensure_dir(path):
    from pathlib import Path
    Path(path).mkdir(parents=True, exist_ok=True)
