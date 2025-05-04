#!/bin/sh
set -e

# Run tests with coverage
coverage run -m pytest tests

# Combine coverage data and generate reports
coverage combine
coverage report --show-missing
coverage xml
