#!/bin/bash

# CI Test Runner Script
# Usage: ./run_tests.sh [chrome|firefox|all] [headless|headed]

set -e

BROWSER=${1:-chrome}
MODE=${2:-headless}

echo "=========================================="
echo "Starting CI Test Execution"
echo "=========================================="
echo "Browser: $BROWSER"
echo "Mode: $MODE"
echo "=========================================="

# Set environment variables
export BROWSER=$BROWSER

if [ "$MODE" == "headless" ]; then
    export HEADLESS=true
else
    export HEADLESS=false
fi

# Create directories
mkdir -p reports screenshots

# Run tests based on browser
if [ "$BROWSER" == "all" ]; then
    echo "Running tests on Chrome..."
    BROWSER=chrome pytest tests/ -v -n auto --html=reports/report_chrome.html --self-contained-html

    echo "Running tests on Firefox..."
    BROWSER=firefox pytest tests/ -v -n auto --html=reports/report_firefox.html --self-contained-html
else
    echo "Running tests on $BROWSER..."
    pytest tests/ -v -n auto --html=reports/report_$BROWSER.html --self-contained-html
fi

echo "=========================================="
echo "Test Execution Completed"
echo "=========================================="

# Display summary
if [ -f reports/history/index.json ]; then
    python3 << EOF
import json
with open('reports/history/index.json') as f:
    data = json.load(f)
    if data:
        run = data[0]
        print(f"\nTest Summary:")
        print(f"  Total: {run['total']}")
        print(f"  Passed: {run['passed']}")
        print(f"  Failed: {run['failed']}")
        print(f"  Errors: {run['error']}")
        print(f"  Pass Rate: {run['pass_rate']}%")
        print(f"  Duration: {run['duration']}s")
EOF
fi

echo ""
echo "Reports available in: reports/"
echo "Screenshots available in: screenshots/"
