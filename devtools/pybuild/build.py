#!/usr/bin/env python3.10
"""Automatically builds __init__.py files based on regexes of the local files."""
import argparse
import itertools as it
import pathlib as p

import cson
import isort
import more_itertools as mit
import regex as re

HASHBANG = "#!/usr/bin/env python3.10\n"
IMPORT_REGEX = re.compile(r"from\s+\.\S+\s+import((\s*\([^)]*\))|(.*$))\n", re.M)


def submodules_in_folder(folder: p.Path):
    examples = []
    for item in folder.iterdir():
        if not (item.suffix == ".py" and not item.name.startswith("_")):
            continue
        examples.append(item)
    yield from sorted(examples)


def build_folder_init(folder: p.Path, regexes):
    buffer = HASHBANG
    target = folder / "__init__.py"
    right_buffer = ""

    # Removes all local imports from the file.
    if target.exists():
        with open(target, "r") as file:
            right_buffer = file.read().removeprefix(HASHBANG)
        while match := re.search(IMPORT_REGEX, right_buffer):
            right_buffer = right_buffer.replace(match.group(), "")
        right_buffer = "\n" + right_buffer.strip() + "\n"

    # Finds all local files to import from.
    for filename in submodules_in_folder(folder):
        with open(filename) as file_:
            contents = file_.read()
            item = [sorted(re.findall(regex, contents, re.M)) for name, regex in regexes.items()]
            item = mit.flatten(item)
            item = list(item)
            if not item:
                continue
            item = "(\n    " + ",\n    ".join(item) + "\n)"
            string = f"from .{filename.stem.split('.', 1)[0]} import {item}\n"
        buffer += string

    # Sorts imports.
    with open(folder / "__init__.py", "w") as file:
        code = (buffer + right_buffer).rstrip() + "\n"
        code = isort.code(code)
        file.write(code)


def from_file(filename: p.Path) -> None:
    print(f"Building Python imports from file '{filename}'.")

    with open(filename, "r", encoding="utf-8") as file:
        contents = cson.load(file)

    tasks = contents["tasks"]
    exit_code = 0

    for folder, regex_names in tasks.get("mkinit", {}).items():
        folder = p.Path(folder)
        regexes = dict(zip(regex_names, map(contents["regexes"].get, regex_names)))

        print(f"Building '{folder / '__init__.py'}' with {len(regexes)} regexes...", end="")

        if not folder.exists():
            print(" ERROR: the folder does not exist. skipping.")
            exit_code |= 1

        assert None not in regexes

        build_folder_init(folder, regexes)
        print(" done!")

    return exit_code


def main() -> None:
    parser = argparse.ArgumentParser(description='Automatically generate __init__.py files.')
    parser.add_argument('path', metavar='P', type=p.Path, help='path to load build instructions from')
    args = parser.parse_args()
    exit_code = from_file(args.path)
    exit(exit_code)


if __name__ == '__main__':
    main()
