import json
import dataclasses as dc
import typing as t
import more_itertools as mit

import regex as re

from .constants import constants
from utils import *

FORMAT_REGEX = re.compile(r"\{([^{}:]*):(-?[^{}\-:]*)(?>->([^{}]*))?\}")


@dc.dataclass(eq=True, unsafe_hash=True)
class Rule:
    name: str
    regex: re.Pattern
    formatter: str
    tags: list
    priority: int = constants.priority_of(constants.LPAR)

    def __repr__(self):
        return f"<{type(self).__qualname__} {self.name!r}>"

    def __lt__(self, o):
        return self.priority < o.priority

    def __init__(self, name, regex, tags=None, formatter=None, *, consumed=None, delimiters=None, priority=constants.priority_of(constants.LPAR)):
        self.name = name
        self.regex = re.compile(regex, re.W | re.M | re.X)
        # self.formatter = Replacer(regex, formatter)
        self.formatter = formatter
        self.consumed = consumed
        self.tags = tuple(tags) if tags else tuple()
        self.priority = self.priority

        if self.consumed is None:
            # Automatically find consumed groups from the formatter.
            items = re.finditer(FORMAT_REGEX, formatter)
            items = [i.group(2) for i in items if i.group(1) == "token"]
            formatters = mit.unique_everseen(items)
            self.consumed = list(map(int, formatters))

        self.delimiters = delimiters if delimiters is not None else {}
