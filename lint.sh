#!/bin/bash

# IBB Traffic Data Reader - Pre-Push Quality Check
# Comprehensive script for code quality, testing, and coverage before pushing to main

set -e

echo "� Running pre-push quality checks..."
echo

# Check if required tools are installed
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo "❌ $1 is not installed. Installing development dependencies..."
        pip install -r requirements.txt
        return 1
    fi
    return 0
}

# Install dependencies if needed
if ! check_tool ruff || ! check_tool mypy || ! check_tool pytest; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo
fi

echo "� Step 1: Code formatting..."
ruff format .
echo "✅ Code formatted"
echo

echo "� Step 2: Linting and style checks..."
ruff check . --fix
echo "✅ Linting passed"
echo

echo "� Step 3: Checking for unused imports..."
ruff check . --select F401,F841 --no-fix
echo "✅ No unused imports found"
echo

echo "📋 Step 4: Import sorting..."
ruff check . --select I --no-fix
echo "✅ Import sorting verified"
echo

echo "🔤 Step 5: Type checking..."
mypy reader/
echo "✅ Type checking passed"
echo

echo "🧪 Step 6: Running tests with coverage..."
pytest --cov=reader --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80
echo "✅ Tests passed with sufficient coverage"
echo

