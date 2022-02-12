#!/usr/bin/env python3.10
"""Builds infix operators."""
import cson
import lindworm
import regex as re


OPERATOR_REGEX = "|".join(
    map(
        re.escape,
        sorted(lindworm.OPERATORS.keys(), key=len, reverse=True),
    ))

OPERATOR_CURRY_REGEX = f"(?<operator>{OPERATOR_REGEX})\\$"


def main():
    item = {
        "operator_curry": {
            "regex": OPERATOR_CURRY_REGEX,
            "formatter": "OPERATORS['{ group:operator }']",
        },
    }

    result = cson.dumps(item, indent=4)
    print(result)


if __name__ == '__main__':
    main()