#!/bin/sh

# Using test package
# python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE

rm -rf ./build && rm -rf dist && rm -rf src/py_ssdb_client.egg-info
python3 -m build && python3 -m twine upload --repository testpypi dist/*

rm -rf src/py_ssdb_client.egg-info
rm -rf ./build

