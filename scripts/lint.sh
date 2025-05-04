#!/bin/sh
set -e

echo "Run Ruff checks"
ruff check pulseeco tests

echo "Check formatting"
ruff format --check --diff pulseeco tests

echo "Run mypy type checking"
mypy .
