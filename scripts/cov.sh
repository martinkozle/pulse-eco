#!/bin/sh
set -e

echo "Run tests with coverage"
coverage run -m pytest tests

echo "Combine coverage data and generate reports"
coverage combine
coverage report --show-missing
coverage xml
