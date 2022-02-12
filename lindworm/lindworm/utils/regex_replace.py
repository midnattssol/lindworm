import more_itertools as mit
import itertools as it
import regex as re
import dataclasses as dc
import typing as t


ReplacerString = t.TypeVar("RegexReplacementStr", str, bytes)


CASE_SHORTHANDS = {
    "CF": str.casefold,
    "C": str.capitalize,
    "L": str.lower,
    "T": str.title,
    "U": str.upper,
    "S": str.swapcase,
}

MISC_SHORTHANDS = {
    "ju-l": str.ljust,
    "ju-r": str.rjust,
    "st-l": str.lstrip,
    "st-r": str.rstrip,
    "rm-p": str.removeprefix,
    "rm-s": str.removesuffix,
    "cen": str.center,
    "exp": str.expandtabs,
    "rep": str.replace,
    "st": str.strip,
    "tra": str.translate,
    "zfi": str.zfill,
    "len": lambda s: str(len(s)),
    "??": lambda s, r: r if s else s,
}

SHORTHANDS = {**CASE_SHORTHANDS, **MISC_SHORTHANDS}

FORMAT_REGEX = re.compile(r"\{([^{}:]*):(\s*-?[^{}\-:]*)(?>->([^{}]*))?\}")
SUBFORMAT_REGEX = re.compile(r"(\s*\[[^][]+\])|([^:]+)\s*:?")
SUBSUBFORMAT_REGEX = re.compile(r"(\S+)")


# ===| Functions |===


@dc.dataclass
class Replacer:
    regex: re.Regex
    fmtstr: ReplacerString

    def format(self, arg: str, args=None) -> str:
        return self.format_match(re.match(self.regex, arg), args)

    def format_match(self, match: re.match, args=None) -> str:
        return advanced_format(self.fmtstr, match, args)

    # @classmethod
    # def single_formatter(cls, formatter, token_string):
    #     match = re.match(FORMAT_REGEX, formatter)
    #     assert match
    #
    #     # magic: replaces the index with 0
    #     formatter = formatter.replace(match.group(1), "group")
    #     formatter = formatter.replace(match.group(2), "0")
    #     formatter = cls("(.*)", formatter)
    #     return formatter.format(token_string)


def advanced_format(fmtstr: ReplacerString, item: re.Match, subargs=None) -> str:
    # Logging
    print("item:   ", item)
    print("fmtstr:  ", fmtstr)

    subargs = {} if subargs is None else subargs

    if item is None:
        raise ValueError("Expected a match but got None.")

    item_groups = {str(i): v for i, v in enumerate(item.groups())}
    item_groups |= item.groupdict()

    # does not account for double backslashing, but at least it allows escape sequences here
    unescaped_fmtstr = fmtstr.replace(r"\}", "").replace(r"\{", "")
    matches = re.finditer(FORMAT_REGEX, unescaped_fmtstr)
    matches = mit.unique_everseen(matches)

    mapping = {}
    output = fmtstr

    for match in matches:
        origin = match.group(0)

        k = match.group(1).strip()
        lookup_closure = subargs[k] if k != "group" else item_groups
        target = _advanced_format_single(match, fmtstr, item_groups)
        # # Logging
        # print("match:   ", match)
        # print("output:  ", output)
        # print("origin:  ", origin)
        # print("target:  ", target)
        output = output.replace(origin, target)

    return output


def _advanced_format_single(match: re.Match, fmtstr: str, item_groups: dict) -> str:
    """Regex transformation thing."""

    match_groups = [
        str.strip(i) if i is not None else None for i in match.groups()]

    if match_groups[1] not in item_groups:
        raise ValueError(
            f"No group named {match_groups[1]!r} could be found (valid groups: {sorted(item_groups.keys())}).")

    # print(match_groups)
    # print(item_groups)

    output = item_groups[match_groups[1]]
    formatting_descriptor = match_groups[2]

    if formatting_descriptor:
        instructions = re.finditer(SUBFORMAT_REGEX, formatting_descriptor)
        instructions = [i.group(0) for i in instructions]

        instructions = [
            [j.removesuffix(":") for j in re.findall(SUBSUBFORMAT_REGEX, i)] for i in instructions
        ]

        for instruction in instructions:
            instruction = list(filter(None, instruction))
            command = instruction[0].strip()
            arguments = instruction[1:]

            # Calls a method.
            for k, v in SHORTHANDS.items():
                if command == k:
                    command = v
                    print(output)
                    output = v(output, *arguments)
                    print(output)
                    break
            else:
                # Uses normal string formatting.
                assert not arguments
                metaformatter = "{0" + command + "}"

                output = metaformatter.format(
                    _StrSlicer(output)
                )
            continue

    return output


# ===| Utilities |===

@dc.dataclass
class _StrSlicer:
    """Utility class that implements __getitem__ such that it accepts a string version of its normal input.

    Useful for string formatting.

    Examples
    ========
    >>> item = list(range(30))
    >>> _StrSlicer(item)["10: 15"] # Spaces work fine with this as well
    [10, 11, 12, 13, 14]
    >>> "The numbers in range are {0[10:15]}.".format(_StrSlicer(item))
    "The numbers in range are [10, 11, 12, 13, 14]."
    """

    item: t.Any

    def __getitem__(self, i):
        return self.item[_parse_slice(i)]


def _parse_slice(item: str) -> slice:
    """Parses a slice representation into a slice.

    Examples
    ========
    >>> _parse_slice("10:20:-1")
    slice(10, 20, -1)
    """
    # https://stackoverflow.com/a/51105983
    if ":" not in item:
        return int(item)

    return slice(*map(lambda x: int(x.strip()) if x.strip() else None, item.split(':')))
