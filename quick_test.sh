#!/bin/bash

# Quick Test Runner - Test the CI setup locally before pushing

echo "🧪 Running Quick Test..."
echo ""

# Check if dependencies are installed
if ! python3 -c "import pytest" 2>/dev/null; then
    echo "❌ pytest not installed. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run a quick smoke test
echo "Running smoke test (test_login.py)..."
echo ""

BROWSER=chrome HEADLESS=true pytest tests/test_login.py -v --tb=short

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Smoke test passed! CI setup is working correctly."
    echo ""
    echo "Next steps:"
    echo "  1. git add ."
    echo "  2. git commit -m 'Add CI/CD automation setup'"
    echo "  3. git push origin main"
else
    echo "❌ Smoke test failed. Please check the errors above."
    echo ""
    echo "Common issues:"
    echo "  - Chrome not installed"
    echo "  - Dependencies not installed: pip install -r requirements.txt"
    echo "  - Test credentials incorrect in utils/config.py"
fi

exit $EXIT_CODE
