#!/bin/bash

# IBB Traffic Data Reader - Pre-Push Quality Check

set -e

echo "🚀 Running pre-push quality checks..."
echo

echo "🔧 Code formatting and linting..."
ruff format .
ruff check . --fix
echo "✅ Code quality checks passed"
echo

echo "🧪 Running tests with coverage..."
pytest --cov=reader --cov-report=term --cov-fail-under=80
echo "✅ Tests passed"
echo

echo "🎉 Ready to push! 🚀"
