#!/usr/bin/env python3.10
"""Compiles and runs all tests in the `tests` directory."""
import argparse
import pathlib as p
import subprocess
import unittest

import lindworm


class LindwormTester(unittest.TestCase):
    """Runs the test suite for Lindworm."""

    ...


def main():
    parser = argparse.ArgumentParser(description="Run Lindworm tests.")
    parser.add_argument(
        "--tests",
        dest="tests",
        nargs="+",
        help="run the following tests (default: all)",
    )
    args = parser.parse_args()

    def _relative_to_file_(path):
        return str(p.Path(__file__).parent / path)

    # Build and add tests.
    code = subprocess.call(
        ["sigurd", "--dir", _relative_to_file_("tests"), "--force-recompile"]
    )
    if code:
        exit(code)
    import tests

    for name in dir(tests):
        item = getattr(tests, name)
        if (
            name.startswith("test_")
            and callable(item)
            and (args.tests is None or name.removeprefix("test_") in args.tests)
        ):
            setattr(LindwormTester, name, item)

    unittest.main(verbosity=4)


if __name__ == "__main__":
    main()
