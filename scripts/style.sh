#!/bin/sh
set -e

# Run Ruff checks
ruff check pulseeco tests

# Check formatting
ruff format --check --diff pulseeco tests
