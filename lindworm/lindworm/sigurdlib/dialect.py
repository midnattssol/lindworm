#!/usr/bin/env python3.10
import dataclasses as dc
import datetime as dt
import io
import itertools as it
import pathlib as p
import sys
import tokenize
import typing as t

import cson
import mako
import mako.template

from .constants import constants
from .rule import Rule
from .token import SimpleToken


@dc.dataclass
class PythonDialectTokenization:
    """A tokenization of a file written in a Python dialect."""

    tokens: t.List[SimpleToken]
    source: str

    # Workaround so that this moves along with stdout
    logger: io.StringIO = dc.field(default_factory=lambda: sys.stdout)

    def to_python(self) -> str:
        return NotImplemented

    @classmethod
    def from_path(cls, path: p.Path, *args, **kwargs):
        with open(path, "rb") as file:
            return cls.from_bytes(file.read(), *args, **kwargs)

    @classmethod
    def from_bytes(cls, item: bytes, *args, **kwargs):
        tokens = SimpleToken.tokenize(item)
        item = cls(list(tokens), item.decode("utf-8"), *args, **kwargs)
        item.rebuild_source(0)
        return item

    @classmethod
    def load_rules(cls) -> list:
        subitems = {}
        order = None

        for filename in cls.rules_dir.iterdir():
            if filename.suffix != ".cson":
                raise ValueError(
                    f"Unexpected file '{filename}' in rules directory '{cls.rules_dir}' (expected extension '.cson'.)"
                )

            if filename.stem == "__order__":
                with open(filename) as file:
                    order = cson.load(file)
                continue

            with open(filename) as file:
                subitems[filename.stem] = cson.load(file)

        # Finds all rules.
        rules = []
        for file_stem in order:
            item = subitems[file_stem]
            rules += [
                Rule(k, **v, priority=constants.priority_of(constants.LPAR))  # -i
                for k, v in item.items()
            ]

        return rules

    def rebuild_source(self, indent=0):
        """Rebuilds the source attribute from tokens."""
        self.source = ""

        for token in self.tokens:
            self.source += token.string

            # Add indentation.
            if token.exact_type in {constants.NEWLINE, constants.NL}:
                self.source += " " * indent * token.indent

        return self

    def __iter__(self):
        return iter(self.tokens)
