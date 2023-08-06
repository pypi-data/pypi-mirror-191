#!/bin/bash
pipenv requirements --dev > requirements.txt
python3 -m build
python3 -m twine upload --repository pypi dist/*