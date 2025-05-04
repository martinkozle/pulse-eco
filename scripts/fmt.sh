#!/bin/sh
set -e

# Fix Ruff issues
ruff check --fix pulseeco tests

# Format code
ruff format pulseeco tests
