#!/usr/bin/env python3.10
"""Builds infix operators."""
import string

import cson
import lindworm.header
import regex as re


def regexified(items):
    s = "|".join(
        map(
            re.escape,
            sorted(items, key=len, reverse=True),
        ))
    return s


OPERATOR_REGEX = regexified([i for i in lindworm.header.OPERATORS if not set(string.ascii_letters) & set(i)])

print(cson.dumps(OPERATOR_REGEX))
exit()


def main():
    item = {
        "operator_curry": {
            "regex": OPERATOR_CURRY_REGEX,
            "formatter": "lindworm.header.OPERATORS['{ group:operator }']",
        },
    }

    result = cson.dumps(item, indent=4)
    print(result)


if __name__ == '__main__':
    main()
