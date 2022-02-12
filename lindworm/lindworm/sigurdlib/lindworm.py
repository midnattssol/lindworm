import sys
import os
import subprocess
import cson
import dataclasses as dc
import hashlib
import io
import itertools as it
import pathlib as p
import tokenize
import datetime as dt
import typing as t

import numpy as np
import autopep8
import mako
import mako.template
import more_itertools as mit
import regex as re

from ..utils import *
from .constants import constants
from .dialect import PythonDialectTokenization
from .rule import Rule, FORMAT_REGEX
from .token import SimpleToken

__version__ = "0.1.0"

# ===| Globals |===

TMP_DIR = p.Path("/tmp")

METADATA_BEGIN = "===| BEGIN LINDWORM METADATA |==="
METADATA_FINAL = "===| END LINDWORM METADATA |==="
PARENT_DIR = p.Path(__file__).parent

BALANCED_TOKENS = {
    constants.LPAR: constants.RPAR,
    constants.LSQB: constants.RSQB,
}

# ===| Classes |===


class LindwormTokenization(PythonDialectTokenization):
    """A tokenization of a file written in the Lindworm Python dialect."""
    template_dir = PARENT_DIR / "../data/templates"
    rules_dir = PARENT_DIR / "../data/rules"

    def generate_metadata(self):
        origin_digest = hashlib.md5((self.source + __version__).encode("utf-8")).hexdigest()
        metadata = {
            "uid": origin_digest,
            "compiler": {"name": "sigurd", "version": __version__},
            "compilation_time": dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "dialect": "lindworm"
        }

        return metadata

    def parse_file_metadata(self, filename: str) -> str:
        """Parse file metadata from a filename. Returns None if the metadata is invalid."""
        with open(filename) as file:
            return self.parse_metadata(file.read())

    def parse_metadata(self, string: str) -> t.Optional[dict]:
        """Parse file metadata from string contents. Returns None if the metadata is invalid."""
        metadata_block = string.split("# " + METADATA_BEGIN)[1].split("# " + METADATA_FINAL)[0]
        metadata_block = (i.removeprefix("# ") for i in metadata_block.splitlines(True))
        try:
            return cson.loads("".join(metadata_block))
        except cson.ParseError:
            return None

    def to_python(self, *, beautifier="none"):
        self.logger.write(f"INFO | Compiling self.\n")
        metadata = self.generate_metadata()
        self.compile_tokens()
        template = load_template(self.template_dir / "default.py.mako")

        metadata_lines = cson.dumps(metadata, indent=4).splitlines()
        metadata_lines.insert(0, METADATA_BEGIN)
        metadata_lines.append(METADATA_FINAL)

        metadata_str = "\n".join(map("# ".__add__, metadata_lines))

        compiled = template.render(
            source=self.source,
            metadata=metadata_str
        )

        if beautifier == "autopep8":
            compiled = autopep8.fix_code(compiled, {'aggressive': 3})

        self.logger.write(f"INFO | Compilation done!.\n")

        return compiled

    def compile_tokens(self):
        pointer = 0
        rules = self.load_rules()
        ignored = {constants.STRING, constants.COMMENT}

        matches_table = []
        maxloop = 128
        maxloop_inner = None

        # TODO: get memoization working right with returning the affecte ranges

        while rules and maxloop:
            maxloop_inner = 20
            maxloop -= 1

            # Try to find a new target to search and replace.
            while rules and not matches_table:
                maxloop_inner -= 1
                if not maxloop_inner:
                    raise ValueError("Stuck in infloop")
                pointer = 0
                first_matches = []
                self.logger.write(f"RULES | {rules}\n")

                # Get matches for one rule at a time.
                for rule in rules.copy():
                    for result in re.finditer(rule.regex, self.source):
                        first_matches.append((rule, result))

                    first_matches = [
                        (k, v) for k, v in first_matches
                        if v is not None
                        and self.exact_type_at(v.span()[0]) not in ignored
                    ]

                    first_matches = sorted(
                        first_matches,
                        key=lambda x: (x[1].span()[0], - x[1].span()[1]),
                        reverse=True
                    )

                    if first_matches:
                        break
                    rules.pop(0)

                matches_table = first_matches[:1]

            # Since no new ones were found, we're done!
            if not rules:
                break

            match = matches_table.pop(-1)
            pointer = match[1].span()[0]

            # Remove matches that will get moved around due to the overlapping windows.
            matches_table = [(k, v) for k, v in matches_table if v.span()[1] < pointer]
            self.logger.write(f"MATCHESTABLE | {matches_table}\n")
            self.logger.write(f"MATCH | {match}\n")
            # self.logger.write(repr(match) + "\n" + repr(match.groups()))

            # Pointers on either side of the match.
            low = self.source2token_idx(match[1].span()[0])
            high = self.source2token_idx(match[1].span()[1])

            self.logger.write(f"RULE | Match found between {(range(low, high))}\n")
            rule = match[0]
            mapping, consumed = self.get_replacement(rule, match, range(low, high))
            self.logger.write(f"RULE | {mapping, consumed}\n")
            self.logger.write(f"TOKENS | {min(consumed)} and up: {self.tokens[min(consumed):max(consumed)]}\n")

            new_item = rule.formatter
            for key, value in mapping.items():
                if key not in new_item:
                    raise ValueError("Something's very odd here")
                new_item = new_item.replace(key, value)

            self.logger.write(f"RULE | Formatted {rule.formatter!r} -> {new_item!r}\n")

            # Removes the old items and adds the replacements.
            token_dict = dict(enumerate(self.tokens))
            token_dict = {k: [v] for k, v in token_dict.items() if k not in consumed}

            tokenization_of_subgroup = list(SimpleToken.tokenize(new_item.encode("utf-8")))
            token_dict[low] = tokenization_of_subgroup

            self.tokens = [i[1] for i in sorted(token_dict.items())]
            self.tokens = list(mit.flatten(self.tokens))
            self.rebuild_source()

            self.logger.write(f"SOURCE | {self.source!r}\n")

        else:
            raise ValueError("Entered infinite loop.")

        self.rebuild_source(4)
        return self

    def neighbouring_tokengroup(self, pointer: int, direction: int, rule) -> dict:
        """Returns the neighbouring group of tokens."""
        enumerated = list(enumerate(self.tokens))

        if direction == 1:
            token_items = enumerated[pointer:][::direction]
            balancer = reversed_dict(BALANCED_TOKENS.copy())
        else:
            token_items = enumerated[:pointer][::direction]
            balancer = BALANCED_TOKENS.copy()

        done = False
        force_terminate = False
        output = []
        consumed = set()
        balanced_tokens_depths = {k: 0 for k in balancer}

        ENDING = {constants.WHITESPACE, constants.ERRORTOKEN, constants.NUMBER, constants.STRING,
                  constants.DOT, constants.NAME, constants.COLON, constants.LBRACE, constants.RBRACE}
        LEADING = {constants.WHITESPACE, constants.ERRORTOKEN, constants.NEWLINE}
        TERM = {constants.EQUAL}

        for index, token in token_items:
            self.logger.write(f"TOKEN | {token} {done} {direction}\n")

            if (
                (
                    # Avoid going into a new line if the line is balanced.
                    token.exact_type == constants.NEWLINE
                    and not any(balanced_tokens_depths.values())
                )
                or (
                    # Avoid going backwards into assignments.
                    token.exact_type in TERM
                    and direction == -1
                )
                or (
                    token.exact_type in balanced_tokens_depths.keys()
                    and not any(balanced_tokens_depths.values())
                )
            ):
                break

            # Avoids returning early from consuming leading whitespace tokens.
            if (
                (not done and token.exact_type in LEADING)
                or token.exact_type in ENDING
            ):
                output.append(index)
                consumed.add(index)
                continue

            # Ensures balanced tokens.
            if (
                done
                and not any(balanced_tokens_depths.values())
                and (
                    # If this check is not done, the program will attempt to grab
                    # left parentheses as well: for example, "greeter(greeting"
                    # when the expected result is "greeting".
                    direction == -1
                    or constants.priority_of(token.exact_type) < rule.priority
                )
            ):
                break

            # Add or subtract to the balance if necessary.
            for k, v in balancer.items():
                if token.exact_type in (k, v):
                    balanced_tokens_depths[k] += ((token.exact_type == k) - (token.exact_type == v))
                    break

            if token.exact_type != constants.INDENT:
                output.append(index)
                consumed.add(index)
            done = True

        return {
            "consumed": consumed,
            "output": output[::direction]
        }

    def get_replacement(self, rule: Rule, match, matched_range: list) -> tuple:
        items = re.finditer(FORMAT_REGEX, rule.formatter)
        items = mit.unique_everseen(items, key=lambda x: x.groups())
        items = list(items)
        mapping = {}
        consumed = set()
        self.logger.write(f"SUBMATCHES | {items}\n")

        bucket_items = mit.bucket(items, lambda x: x.group(1).strip())

        mapping = {}
        maxtoken, mintoken = -np.inf, np.inf
        token_set = set()
        sometokenstuff = {}
        token_mapping = {}

        # Group format: Use a named capture group.
        for token_submatch in bucket_items["group"]:
            token_submatch = token_submatch.group()
            replacer = Replacer(rule.regex, token_submatch)
            mapping[token_submatch] = replacer.format_match(match[1])

        # Token format: Get the nth token relative to this one.

        # Finds the maximum and minimum required token.
        for token_submatch in bucket_items["token"]:
            num = int(token_submatch.group(2))
            maxtoken = max(maxtoken, num)
            mintoken = min(mintoken, num)
            token_set.add(num)
            sometokenstuff[num] = sometokenstuff.get(num, [])
            sometokenstuff[num].append(token_submatch)

        # Gets all items between the maximum and minimum token.
        for submatch in {maxtoken, mintoken} - {-np.inf, np.inf}:
            direction = np.sign(submatch)
            inner_pointer = matched_range.stop if direction == 1 else matched_range.start

            for n in range(np.abs(submatch)):
                token_indices = self.neighbouring_tokengroup(inner_pointer, direction, rule)
                self.logger.write((f"TOKENINDICES | {token_indices!r}\n"))
                assert token_indices["consumed"]
                inner_pointer = max(token_indices["consumed"]) if direction == 1 else min(token_indices["consumed"])

                matched_items = [self.tokens[i].string for i in token_indices["output"]]
                matched_items_string = "".join(matched_items)

                # Find all of the token subgroups that were based on this particular match.
                # Then processes them in a for loop since they might have different formattings.
                if (direction * (n + 1)) in sometokenstuff:
                    for token_submatch in sometokenstuff[direction * (n + 1)]:

                        token_name = token_submatch.group()

                        # MAGIC
                        # HACK: Should change internal class mechanics to be able to operate on strings as well.
                        temp = token_name.replace("token", "group")
                        temp = temp.replace(re.search(r"-?\d+", temp).group(), "0")
                        # MAGIC

                        replacer = Replacer("(.*)", temp)
                        mapping[token_name] = replacer.format(matched_items_string)

                # what does this do
                token_mapping[direction * (n + 1)] = token_indices

        # Only consume the items that should be.
        for key in token_set:
            consumed |= set(token_mapping[key]["output"])
            consumed |= token_mapping[key]["consumed"]

        consumed |= set(matched_range)
        return mapping, consumed

    def _token_range(self, i: int) -> range:
        # Sums the lengths of the previous lines and adds the line location.
        start = sum(map(lambda x: len(x.string), self.tokens[:i]))
        out = range(start, start + len(self.tokens[i].string))

        return out

    def source2token_idx(self, idx: int) -> int:
        """Returns the index of the source item which contains the string index in the source."""
        for i in range(len(self.tokens)):
            if idx < self._token_range(i).stop:
                if idx in self._token_range(i):
                    return i
                return None

        raise ValueError(f"Index {idx} out of matched_range.")

    def exact_type_at(self, index: int) -> int:
        """Gets the type at a location."""
        idx = self.source2token_idx(index)
        return self.tokens[idx].exact_type

# ===| Functions |===


def load_template(path: p.Path) -> mako.template:
    with open(path) as file:
        contents = file.read()
    template = mako.template.Template(contents)
    return template


def parse_metadata(contents):
    md_begin_index = contents.index(METADATA_BEGIN)
    md_final_index = contents.index(METADATA_FINAL)
    return contents[:md_begin_index] + contents[md_final_index:], contents[md_begin_index:md_final_index]
