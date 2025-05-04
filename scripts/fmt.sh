#!/bin/sh
set -e

echo "Fix Ruff issues"
ruff check --fix pulseeco tests

echo "Format code"
ruff format pulseeco tests
