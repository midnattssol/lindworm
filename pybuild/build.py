#!/usr/bin/env python3.10
"""Automatically builds __init__.py files based on regexes of the local files."""
import argparse
import itertools as it
import pathlib as p

import cson
import more_itertools as mit
import regex as re

HASHBANG = "#!/usr/bin/env python3.10\n"


def submodules_in_folder(folder: p.Path):
    examples = []
    for item in folder.iterdir():
        if not (item.suffix == ".py" and not item.name.startswith("_")):
            continue
        examples.append(item)
    yield from sorted(examples)


def import_matching(folder, regexes):
    buffer = HASHBANG

    for filename in submodules_in_folder(folder):
        with open(filename) as file_:
            contents = file_.read()
            item = [re.findall(x, contents, re.M) for x in regexes]
            item = map(sorted, item)
            item = mit.flatten(item)
            item = list(item)
            if not item:
                continue
            item = ("(\n    " + ",\n    ".join(item) + "\n)") if len(item) > 1 else mit.first(item, "")
            string = f"from .{filename.stem.split('.', 1)[0]} import {item}\n"
        buffer += string

    with open(folder / "__init__.py", "w") as file:
        file.write(buffer)


def from_file(filename):
    print(f"Building from file '{filename}'.")

    with open(filename, "r", encoding="utf-8") as file:
        contents = cson.load(file)

    tasks = contents["tasks"]

    for folder, regex_names in tasks.get("mkinit", {}).items():
        folder = p.Path(folder)
        regexes = list(map(contents["regexes"].get, regex_names))
        print(f"Building '{folder / '__init__.py'}' with {len(regexes)} regexes...", end="")
        assert folder.exists()
        assert None not in regexes
        import_matching(folder, regexes)
        print(" done!")


def main() -> None:
    parser = argparse.ArgumentParser(description='Automatically generate __init__.py files.')
    parser.add_argument('path', metavar='P', type=p.Path, help='path to load build instructions from')
    args = parser.parse_args()
    from_file(args.path)


if __name__ == '__main__':
    main()
