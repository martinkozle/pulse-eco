#!/bin/sh
set -e

echo "Run pre-commit hooks"
pre-commit run --all-files

echo "Run lint checks"
./scripts/lint.sh

echo "Run coverage"
./scripts/cov.sh
