#!/bin/bash
read -r -p 'Did you check the dependencies?'
python3 -m build
python3 -m twine upload --repository pypi dist/*
rm dist/*
rm requirements.txt