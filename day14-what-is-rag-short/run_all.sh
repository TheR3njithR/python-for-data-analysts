#!/bin/bash
# rebuild nothing: data is the six text notes. Print the diagram, run the phone question, then the tests.
set -e
python rag.py --diagram
python rag.py "How many days to return a phone?"
python -m pytest -q tests
