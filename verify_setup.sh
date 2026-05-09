#!/bin/bash

# Quick test to verify CI setup
echo "🔍 Verifying CI Setup..."
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version

# Check pip
echo "✓ Checking pip..."
pip --version

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt found"
else
    echo "✗ requirements.txt not found"
    exit 1
fi

# Check if pytest.ini exists
if [ -f "pytest.ini" ]; then
    echo "✓ pytest.ini found"
else
    echo "✗ pytest.ini not found"
    exit 1
fi

# Check if workflows exist
if [ -d ".github/workflows" ]; then
    echo "✓ GitHub workflows directory found"
    echo "  Workflows:"
    ls -1 .github/workflows/ | sed 's/^/    - /'
else
    echo "✗ GitHub workflows directory not found"
    exit 1
fi

# Check if test directory exists
if [ -d "tests" ]; then
    echo "✓ Tests directory found"
    echo "  Test files:"
    ls -1 tests/*.py 2>/dev/null | sed 's/^/    - /'
else
    echo "✗ Tests directory not found"
    exit 1
fi

# Check if Makefile exists
if [ -f "Makefile" ]; then
    echo "✓ Makefile found"
else
    echo "✗ Makefile not found"
fi

# Check if Docker files exist
if [ -f "Dockerfile" ] && [ -f "docker-compose.yml" ]; then
    echo "✓ Docker configuration found"
else
    echo "⚠ Docker configuration not found (optional)"
fi

echo ""
echo "✅ CI Setup verification complete!"
echo ""
echo "Next steps:"
echo "  1. Install dependencies: pip install -r requirements.txt"
echo "  2. Run tests locally: pytest tests/ -v"
echo "  3. Push to GitHub to activate CI/CD"
echo ""
