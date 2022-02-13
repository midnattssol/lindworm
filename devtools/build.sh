#!/bin/sh
cd $(dirname $0)

echo "- validating lindworm build"
python validate.py || exit 1

echo "- build valid!"
echo "- building from source..."

python pybuild/build.py "pybuild.cson" || exit 1

cd ../lindworm
pip install .
cd ../devtools

python build_infix_curry.py > "lindworm/lindworm/data/rules/infix_curry.cson"

echo "- build complete!"
echo "- running tests..."

python ../lindworm/run_tests.py
