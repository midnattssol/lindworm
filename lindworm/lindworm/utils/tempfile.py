#!/usr/bin/env python3.10
""""""
import pathlib as p


def tempfile():
    """Gets a temporary unused filename."""
    base_path = p.Path("/tmp/")
    filename = None
    i = 0

    while True:
        i += 1
        filename = base_path / f"tempfile_{i}"
        if not filename.exists():
            break

    return filename
