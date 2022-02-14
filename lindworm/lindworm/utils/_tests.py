#!/usr/bin/env python3.10
import regex_replace

Uppercaser = regex_replace.Replacer(r"(.*)", "{ group : 0 -> U}")

assert Uppercaser.format("hello world") == "HELLO WORLD"

Uppercaser = regex_replace.Replacer(r"(.*)", "{ group : 0 -> U }")
