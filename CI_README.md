# Automation QA - CI/CD Setup

This project includes automated testing with CI/CD integration.

## Quick Start

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run tests in parallel
pytest tests/ -v -n auto

# Run specific test file
pytest tests/test_login.py -v

# Run with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Using Make Commands

```bash
make install        # Install dependencies
make test          # Run all tests
make test-parallel # Run tests in parallel
make test-smoke    # Run smoke tests only
make clean         # Clean reports and screenshots
make report        # Generate HTML report
```

### Using Shell Scripts

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh chrome headless
./run_tests.sh firefox headed
./run_tests.sh all headless
```

**Windows:**
```cmd
run_tests.bat chrome headless
run_tests.bat firefox headed
run_tests.bat all headless
```

## CI/CD Workflows

### 1. Main CI Pipeline (`.github/workflows/ci.yml`)
- **Triggers:** Push to main/develop, Pull Requests, Daily at 2 AM UTC
- **Browsers:** Chrome and Firefox (matrix)
- **Features:**
  - Parallel execution with pytest-xdist
  - HTML reports generation
  - Screenshot capture on failures
  - Test summary in GitHub Actions

### 2. Smoke Tests (`.github/workflows/smoke-tests.yml`)
- **Triggers:** Push to main, Pull Requests, Manual
- **Purpose:** Quick validation (login tests only)
- **Duration:** ~1-2 minutes

### 3. Parallel Tests (`.github/workflows/parallel-tests.yml`)
- **Triggers:** Manual with test suite selection
- **Options:** all, authentication, product, cart, checkout
- **Features:** Distributed parallel execution

### 4. Regression Tests (`.github/workflows/regression.yml`)
- **Triggers:** Weekdays at midnight UTC, Manual
- **Purpose:** Full regression suite
- **Retention:** 90 days

## Test Structure

```
tests/
├── test_login.py           # Authentication tests
├── test_user_account.py    # User account management
├── test_search_product.py  # Product search
├── test_add_to_cart.py     # Shopping cart
└── test_checkout.py        # Checkout process
```

## Configuration

### Environment Variables

```bash
export BROWSER=chrome        # chrome or firefox
export HEADLESS=true         # true or false
```

### pytest.ini

Configure test discovery, markers, and logging in `pytest.ini`.

### Test Markers

```python
@pytest.mark.smoke          # Quick smoke tests
@pytest.mark.regression     # Full regression suite
@pytest.mark.authentication # Auth related tests
@pytest.mark.product        # Product related tests
@pytest.mark.cart           # Cart tests
@pytest.mark.checkout       # Checkout tests
@pytest.mark.slow           # Long-running tests
```

## Reports

### Test Reports Location
- **HTML Reports:** `reports/*.html`
- **JSON History:** `reports/history/*.json`
- **Screenshots:** `screenshots/*.png`
- **Logs:** `reports/pytest.log`

### CI Artifacts
All test results are uploaded as GitHub Actions artifacts with retention:
- Smoke tests: 7 days
- Regular tests: 30 days
- Regression tests: 90 days

## Parallel Execution

Tests run in parallel using pytest-xdist:

```bash
# Auto-detect CPU cores
pytest tests/ -n auto

# Specific number of workers
pytest tests/ -n 4

# Load balancing by group
pytest tests/ -n auto --dist loadgroup
```

## Browser Support

- **Chrome:** Stable version with ChromeDriver (auto-managed)
- **Firefox:** Latest version with GeckoDriver (auto-managed)

Both browsers support headless mode for CI environments.

## Troubleshooting

### Tests fail in CI but pass locally
- Check browser versions
- Verify headless mode compatibility
- Review CI logs and screenshots

### Parallel execution issues
- Reduce worker count: `-n 2`
- Use sequential execution: remove `-n` flag
- Check for test dependencies

### Screenshot not captured
- Ensure `screenshots/` directory exists
- Check driver is still active when failure occurs
- Review conftest.py hook implementation

## Manual Workflow Triggers

Trigger workflows manually from GitHub Actions tab:
1. Go to Actions tab
2. Select workflow
3. Click "Run workflow"
4. Choose parameters (if applicable)

## Contributing

When adding new tests:
1. Follow existing test structure
2. Add appropriate markers
3. Update test documentation
4. Ensure tests pass locally before pushing
5. Check CI pipeline results
