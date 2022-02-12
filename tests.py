#!/usr/bin/env python3.10
"""Compiles and runs all tests in the `tests` directory."""
import contextlib as ctx

import subprocess
import unittest
import argparse
import lindworm
import pathlib as p


class LindwormTester(unittest.TestCase):
    ...


def main():
    parser = argparse.ArgumentParser(description='Compile Lindworm code to Python.')
    parser.add_argument('--tests', dest='tests', nargs="+", help='run the following tests (default: all)')
    args = parser.parse_args()

    # Build tests.
    subprocess.call(["sigurd", "--dir", "tests", "--force-recompile"])
    subprocess.call(["python", "pybuild/build.py", "pybuild.cson"], stdout=open("/dev/null", "w"))

    # Add tests.
    import tests

    for name in dir(tests):
        item = getattr(tests, name)
        if (
            name.startswith("test_") and callable(item)
            and (args.tests is None or name.removeprefix("test_") in args.tests)
        ):
            setattr(LindwormTester, name, item)

    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()
