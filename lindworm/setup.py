#!/usr/bin/env python3.10
import pathlib as p

from setuptools import find_namespace_packages, setup

setup(
    name="lindworm-language",
    version="0.1.0",
    description="Lindworm programming language compiler and standard library",
    url="https://github.com/midnattssol/lindworm",
    author="midnattssol",
    author_email="cd154a7e15@protonmail.com",
    license="BSD 2-clause",
    packages=find_namespace_packages(include=["lindworm.*"]),
    install_requires=[
        "numpy",
        "mako",
        "more_itertools",
        "regex",
        "colorama",
        "frozendict",
        "isort",
    ],
    extras_require={
        "autopep8 linting": ["autopep8"],
        "black linting": ["black"],
    },
    scripts=["bin/lindworm", "bin/sigurd"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
)
