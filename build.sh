#!/bin/sh
cd lindworm
pip install .
cd ..

python pybuild/build.py "pybuild.cson"
python tests.py
