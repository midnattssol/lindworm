import sys
import cson
import dataclasses as dc
import io
import itertools as it
import pathlib as p
import typing as t
import tokenize
import datetime as dt

import mako
import mako.template

from .constants import constants
from .token import SimpleToken
from .rule import Rule


@dc.dataclass
class PythonDialectTokenization():
    """A tokenization of a file written in a Python dialect."""
    tokens: t.List[SimpleToken]
    source: str

    # Workaround so that this moves along with stdout
    logger: io.StringIO = dc.field(default_factory=lambda: sys.stdout)

    def to_python(self):
        return NotImplemented

    @classmethod
    def from_path(cls, path: p.Path, *args, **kwargs):
        with open(path, "rb") as file:
            return cls.from_bytes(file.read(), *args, **kwargs)

    @classmethod
    def from_bytes(cls, s, *args, **kwargs):
        tokens = SimpleToken.tokenize(s)
        item = cls(list(tokens), s.decode("utf-8"), *args, **kwargs)
        item.rebuild_source(0)
        return item

    @classmethod
    def load_rules(cls) -> list:
        with open(cls.rules_path) as file:
            items = cson.load(file)
            rules = [Rule(k, **v, priority=constants.priority_of(constants.LPAR) - i) for i, (k, v) in enumerate(items.items())]
        return rules

    def __iter__(self):
        return iter(self.tokens)

    def rebuild_source(self, indent=0):
        """Rebuilds the source attribute from tokens."""
        self.source = ""

        for token in self.tokens:
            self.source += token.string

            # Add indentation.
            if token.exact_type in {constants.NEWLINE, constants.NL}:
                self.source += (" " * indent * token.indent)

        return self
