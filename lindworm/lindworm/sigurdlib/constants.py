#!/usr/bin/env python3.10
"""Token constants."""
import tokenize


_IOTA = 0


def iota():
    global _IOTA
    _IOTA += 1
    return _IOTA


class constants:
    ENDMARKER = iota()
    NAME = iota()
    NUMBER = iota()
    STRING = iota()
    NEWLINE = iota()
    INDENT = iota()
    DEDENT = iota()
    LPAR = iota()
    RPAR = iota()
    LSQB = iota()
    RSQB = iota()
    COLON = iota()
    COMMA = iota()
    SEMI = iota()
    PLUS = iota()
    MINUS = iota()
    STAR = iota()
    SLASH = iota()
    VBAR = iota()
    AMPER = iota()
    LESS = iota()
    GREATER = iota()
    EQUAL = iota()
    DOT = iota()
    PERCENT = iota()
    LBRACE = iota()
    RBRACE = iota()
    EQEQUAL = iota()
    NOTEQUAL = iota()
    LESSEQUAL = iota()
    GREATEREQUAL = iota()
    TILDE = iota()
    CIRCUMFLEX = iota()
    LEFTSHIFT = iota()
    RIGHTSHIFT = iota()
    DOUBLESTAR = iota()
    PLUSEQUAL = iota()
    MINEQUAL = iota()
    STAREQUAL = iota()
    SLASHEQUAL = iota()
    PERCENTEQUAL = iota()
    AMPEREQUAL = iota()
    VBAREQUAL = iota()
    CIRCUMFLEXEQUAL = iota()
    LEFTSHIFTEQUAL = iota()
    RIGHTSHIFTEQUAL = iota()
    DOUBLESTAREQUAL = iota()
    DOUBLESLASH = iota()
    DOUBLESLASHEQUAL = iota()
    AT = iota()
    ATEQUAL = iota()
    RARROW = iota()
    ELLIPSIS = iota()
    COLONEQUAL = iota()
    OP = iota()
    AWAIT = iota()
    ASYNC = iota()
    TYPE_IGNORE = iota()
    TYPE_COMMENT = iota()
    SOFT_KEYWORD = iota()
    ERRORTOKEN = iota()
    COMMENT = iota()
    NL = iota()
    ENCODING = iota()
    WHITESPACE = iota()

    tok_name = {
        value: name
        for name, value in locals().items()
        if isinstance(value, int) and not name.startswith("_")
    }

    EXACT_TOKEN_TYPES = {
        "!=": NOTEQUAL,
        "%": PERCENT,
        "%=": PERCENTEQUAL,
        "&": AMPER,
        "&=": AMPEREQUAL,
        "(": LPAR,
        ")": RPAR,
        "*": STAR,
        "**": DOUBLESTAR,
        "**=": DOUBLESTAREQUAL,
        "*=": STAREQUAL,
        "+": PLUS,
        "+=": PLUSEQUAL,
        ",": COMMA,
        "-": MINUS,
        "-=": MINEQUAL,
        "->": RARROW,
        ".": DOT,
        "...": ELLIPSIS,
        "/": SLASH,
        "//": DOUBLESLASH,
        "//=": DOUBLESLASHEQUAL,
        "/=": SLASHEQUAL,
        ":": COLON,
        ":=": COLONEQUAL,
        ";": SEMI,
        "<": LESS,
        "<<": LEFTSHIFT,
        "<<=": LEFTSHIFTEQUAL,
        "<=": LESSEQUAL,
        "=": EQUAL,
        "==": EQEQUAL,
        ">": GREATER,
        ">=": GREATEREQUAL,
        ">>": RIGHTSHIFT,
        ">>=": RIGHTSHIFTEQUAL,
        "@": AT,
        "@=": ATEQUAL,
        "[": LSQB,
        "]": RSQB,
        "^": CIRCUMFLEX,
        "^=": CIRCUMFLEXEQUAL,
        "{": LBRACE,
        "|": VBAR,
        "|=": VBAREQUAL,
        "}": RBRACE,
        "~": TILDE,
    }

    # https://docs.python.org/3/reference/expressions.html#operator-precedence
    PRIORITY_DICT = dict(
        enumerate(
            (
                [LPAR, RPAR, LSQB, RSQB],
                [DOT],
                [DOUBLESTAR, TILDE],
                [PLUS, MINUS, STAR, SLASH, LEFTSHIFT, RIGHTSHIFT],
                [AMPER, CIRCUMFLEX, VBAR],
                [GREATER, GREATEREQUAL, LESS, LESSEQUAL],
            )
        )
    )

    # ===| Functions |===

    @classmethod
    def from_tokenize(cls, i: int) -> int:
        name = tokenize.tok_name[i]
        rename = {"NL": "NEWLINE"}
        return getattr(cls, rename.get(name, name))

    @classmethod
    def priority_of(cls, i: int) -> int:
        for k, v in cls.PRIORITY_DICT.items():
            if i in v:
                return k

        return -float("inf")
