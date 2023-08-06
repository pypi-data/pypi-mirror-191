#!/bin/sh

rm -rf ./build && rm -rf dist && rm -rf src/py_ssdb_client.egg-info
python3 -m build && python3 -m twine upload --repository pypi  dist/*

rm -rf src/py_ssdb_client.egg-info
rm -rf ./build

