#!/bin/sh
set -e

# Run pre-commit hooks
pre-commit run --all-files

# Run typing checks
mypy pulseeco tests

# Run coverage
bash scripts/cov.sh
