import operator as op

import more_itertools

from .functions import *

OPERATORS = {
    "+": op.add,
    "in": op.contains,
    "/": op.truediv,
    "//": op.floordiv,
    "&": op.and_,
    "^": op.xor,
    "~": op.invert,
    "|": op.or_,
    "**": op.pow,
    "is": op.is_,
    "<<": op.lshift,
    "%": op.mod,
    "*": op.mul,
    "@": op.matmul,
    "not": op.not_,
    ">>": op.rshift,
    "-": op.sub,
    "<": op.lt,
    "<=": op.le,
    "==": op.eq,
    "!=": op.ne,
    ">=": op.ge,
    ">": op.gt,
}


# New operators
OPERATORS |= {
    "xor": lambda a, b: bool(a) ^ bool(b),
    "isnt": op.is_not,
    "over": map,
    "contains": lambda a, b: b in a,

    "$": curry,
    "::": it.chain,
    "::*": lambda a, b: it.chain(a, *b),
    ":::": lambda a, b: it.chain(more_itertools.always_iterable(a), more_itertools.always_iterable(b)),
    "??": lambda a, b: a if a is not None else b,
    "..>": lambda f, g: compose(f, g, False, 0),
    "..*>": lambda f, g: compose(f, g, False, 1),
    "..**>": lambda f, g: compose(f, g, False, 2),
    "..": lambda f, g: compose(f, g, False, 0),
    "..*": lambda f, g: compose(f, g, False, 1),
    "..**": lambda f, g: compose(f, g, False, 2),
    "<..": lambda f, g: compose(f, g, True, 0),
    "<*..": lambda f, g: compose(f, g, True, 1),
    "<**..": lambda f, g: compose(f, g, True, 2),
    "|>": lambda a, b: b(a),
    "|*>": lambda a, b: b(*a),
    "|**>": lambda a, b: b(**a),
    "<|": lambda a, b: a(b),
    "<*|": lambda a, b: a(*b),
    "<**|": lambda a, b: a(**b),
}
