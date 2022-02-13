#!/usr/bin/env python3.10
"""Validates Lindworm data before building."""
import pathlib as p
import unittest

import cson

RULE_DIRECTORY = p.Path(__file__).parent.parent / "lindworm/lindworm/data/rules"


class LindwormBuildValidator(unittest.TestCase):
    """Tests the Lindworm build."""

    def test_rules_all_files_valid_cson(self) -> None:
        """Checking that all rules are valid CSON files"""
        for rule_file in RULE_DIRECTORY.iterdir():
            with open(rule_file, "r", encoding="utf-8") as file:
                try:
                    result = cson.load(file)
                except cson.ParseError:
                    result = None

            with self.subTest(path=rule_file):
                self.assertIsNotNone(result)

    def test_rules_order_file_ok(self) -> None:
        """Checking that all rules described in the __order__.cson file exist"""
        order_file = RULE_DIRECTORY / "__order__.cson"
        self.assertTrue(order_file.exists())

        rule_files = RULE_DIRECTORY.iterdir()
        rule_files = (i.stem for i in rule_files)
        rule_files = sorted(rule_files)
        rule_files.remove("__order__")

        with open(order_file) as file:
            contents = sorted(cson.load(file))
            self.assertEqual(rule_files, contents)


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()
