#!/bin/bash
# dev only

rm dist/*
python setup.py sdist
python setup.py bdist_wheel sdist
twine upload dist/*


