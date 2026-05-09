# Automation QA - CI/CD Testing Framework

Complete CI/CD automation setup for Selenium-based testing with GitHub Actions, Docker support, and multiple execution options.

## 🚀 Quick Start

### Local Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run tests in parallel
pytest tests/ -v -n auto

# Run with HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Using Make Commands

```bash
make install        # Install dependencies
make test          # Run all tests
make test-parallel # Run tests in parallel
make test-smoke    # Run smoke tests only
make test-chrome   # Run in Chrome
make test-firefox  # Run in Firefox
make clean         # Clean reports and screenshots
make report        # Generate HTML report
```

### Using Shell Scripts

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh chrome headless    # Chrome headless
./run_tests.sh firefox headed     # Firefox with UI
./run_tests.sh all headless       # Both browsers
```

**Windows:**
```cmd
run_tests.bat chrome headless
run_tests.bat firefox headed
run_tests.bat all headless
```

## 🎯 CI/CD Workflows

### 1. Main CI Pipeline (`.github/workflows/ci.yml`)
- **Triggers:** Push to main/develop, Pull Requests, Daily at 2 AM UTC, Manual
- **Browsers:** Chrome & Firefox (parallel matrix)
- **Features:**
  - Parallel test execution with pytest-xdist
  - HTML reports generation
  - Screenshot capture on failures
  - Test summary in GitHub Actions
  - 30-day artifact retention

### 2. Smoke Tests (`.github/workflows/smoke-tests.yml`)
- **Triggers:** Push to main, Pull Requests, Manual
- **Purpose:** Quick validation (login tests only)
- **Duration:** ~1-2 minutes
- **Retention:** 7 days

### 3. Parallel Tests (`.github/workflows/parallel-tests.yml`)
- **Triggers:** Manual with test suite selection
- **Options:** all, authentication, product, cart, checkout
- **Features:** Distributed parallel execution

### 4. Regression Tests (`.github/workflows/regression.yml`)
- **Triggers:** Weekdays at midnight UTC, Manual
- **Purpose:** Full regression suite
- **Retention:** 90 days

## 📁 Project Structure

```
Automation-QA/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Main CI pipeline
│       ├── smoke-tests.yml     # Smoke tests
│       ├── parallel-tests.yml  # Parallel execution
│       └── regression.yml      # Scheduled regression
├── tests/
│   ├── test_login.py           # Authentication tests
│   ├── test_user_account.py    # User account tests
│   ├── test_search_product.py  # Product search tests
│   ├── test_add_to_cart.py     # Shopping cart tests
│   └── test_checkout.py        # Checkout tests
├── pages/                      # Page Object Models
├── locators/                   # Element locators
├── utils/
│   ├── config.py              # Configuration
│   ├── driver_setup.py        # WebDriver setup
│   └── helpers.py             # Helper functions
├── reports/                    # Test reports (generated)
├── screenshots/                # Screenshots (generated)
├── conftest.py                # Pytest fixtures and hooks
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── Makefile                   # Make commands
├── run_tests.sh              # Shell script runner
├── run_tests.bat             # Windows batch runner
├── verify_setup.sh           # Setup verification
├── Dockerfile                # Docker image
├── docker-compose.yml        # Multi-container setup
└── README.md                 # This file
```

## 🧪 Running Tests

### pytest Commands

```bash
# All tests
pytest tests/ -v

# Parallel execution (auto-detect cores)
pytest tests/ -v -n auto

# Parallel with specific workers
pytest tests/ -v -n 4

# Specific test file
pytest tests/test_login.py -v

# With markers
pytest tests/ -v -m smoke
pytest tests/ -v -m "authentication or product"
pytest tests/ -v -m "not slow"

# Stop on first failure
pytest tests/ -v -x

# Maximum failures
pytest tests/ -v --maxfail=3

# Verbose output
pytest tests/ -vv --tb=long

# With HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

### Environment Variables

```bash
# Set browser
export BROWSER=chrome        # chrome or firefox
export HEADLESS=true         # true or false

# Run tests
pytest tests/ -v

# Or inline
BROWSER=firefox HEADLESS=true pytest tests/ -v
```

## 🏷️ Test Markers

```python
@pytest.mark.smoke          # Quick smoke tests
@pytest.mark.regression     # Full regression suite
@pytest.mark.authentication # Auth related tests
@pytest.mark.product        # Product related tests
@pytest.mark.cart           # Cart tests
@pytest.mark.checkout       # Checkout tests
@pytest.mark.slow           # Long-running tests
```

## 📊 Test Reports

### Report Locations
- **HTML Reports:** `reports/*.html`
- **JSON History:** `reports/history/*.json`
- **Screenshots:** `screenshots/*.png`
- **Logs:** `reports/pytest.log`

### CI Artifacts
All test results are uploaded as GitHub Actions artifacts:
- Smoke tests: 7 days retention
- Regular tests: 30 days retention
- Regression tests: 90 days retention

## ⚙️ Configuration

### Browser Configuration (`utils/config.py`)

```python
BASE_URL = "https://demowebshop.tricentis.com"
BROWSER = "chrome"           # chrome or firefox
HEADLESS = False             # True for headless mode
IMPLICIT_WAIT = 2            # seconds
PAGE_LOAD_TIMEOUT = 30       # seconds
SLOW_MODE = True             # True for demo mode
STEP_DELAY = 0.5             # seconds between actions
```

### pytest Configuration (`pytest.ini`)

- Test discovery patterns
- Output formatting
- Custom markers
- Logging configuration
- Warning filters

## 🐳 Docker Support

### Standalone Container

```bash
# Build image
docker build -t automation-qa .

# Run tests
docker run automation-qa
```

### With Selenium Grid

```bash
# Start Selenium Grid
docker-compose up -d selenium-hub chrome firefox

# Run tests
docker-compose run test-runner pytest tests/ -v

# Stop all services
docker-compose down
```

## 🔧 Troubleshooting

### Tests fail in CI but pass locally
- Check browser versions match
- Verify headless mode compatibility
- Review CI logs and screenshots in artifacts
- Check timing issues (increase waits)

### Parallel execution issues
- Reduce worker count: `pytest -n 2`
- Use sequential execution: remove `-n` flag
- Check for test dependencies or shared state

### Screenshot not captured
- Ensure `screenshots/` directory exists
- Check driver is still active when failure occurs
- Review `conftest.py` hook implementation

### WebDriver issues
- Driver auto-downloads via webdriver-manager
- Check internet connectivity for driver download
- Verify browser is installed on system

## 📈 CI/CD Best Practices

### Manual Workflow Triggers
1. Go to GitHub Actions tab
2. Select desired workflow
3. Click "Run workflow"
4. Choose parameters (if applicable)

### Adding New Tests
1. Follow existing test structure and naming
2. Add appropriate pytest markers
3. Update documentation if needed
4. Ensure tests pass locally before pushing
5. Check CI pipeline results

### Monitoring Test Health
- Review daily regression results
- Check pass rate trends in reports
- Investigate flaky tests
- Update selectors when UI changes

## 🎓 Next Steps

### 1. Verify Setup
```bash
chmod +x verify_setup.sh
./verify_setup.sh
```

### 2. Run Tests Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run smoke tests
pytest tests/test_login.py -v

# Run all tests
pytest tests/ -v -n auto
```

### 3. Push to GitHub
```bash
git add .
git commit -m "Add CI/CD automation setup"
git push origin main
```

### 4. Check GitHub Actions
- Go to repository → Actions tab
- View workflow runs
- Download artifacts
- Review test results

## 📝 Files Created

### CI/CD Configuration
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/smoke-tests.yml` - Smoke test workflow
- `.github/workflows/parallel-tests.yml` - Parallel execution
- `.github/workflows/regression.yml` - Scheduled regression

### Test Configuration
- `pytest.ini` - Pytest configuration
- `.gitignore` - Git ignore patterns

### Execution Scripts
- `Makefile` - Make commands
- `run_tests.sh` - Shell script for Linux/Mac
- `run_tests.bat` - Batch script for Windows
- `verify_setup.sh` - Setup verification

### Docker
- `Dockerfile` - Container image
- `docker-compose.yml` - Multi-container setup

### Documentation
- `README.md` - This comprehensive guide
- `SETUP_SUMMARY.md` - Detailed setup summary
- `CI_README.md` - CI/CD specific documentation

### Updated Files
- `utils/driver_setup.py` - Enhanced with Firefox support and webdriver-manager

## 📞 Support

For issues or questions:
- Check CI logs in GitHub Actions
- Review screenshots in artifacts
- Check `reports/pytest.log` for detailed logs
- Verify browser and driver compatibility

---

**Created:** 2026-05-09  
**Status:** ✅ Ready for use  
**Python:** 3.11+  
**Browsers:** Chrome, Firefox
