.PHONY: help install test test-parallel test-smoke test-chrome test-firefox clean report

help:
	@echo "Available commands:"
	@echo "  make install        - Install dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-parallel - Run tests in parallel"
	@echo "  make test-smoke    - Run smoke tests only"
	@echo "  make test-chrome   - Run tests in Chrome"
	@echo "  make test-firefox  - Run tests in Firefox"
	@echo "  make clean         - Clean reports and screenshots"
	@echo "  make report        - Generate HTML report"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-parallel:
	pytest tests/ -v -n auto

test-smoke:
	pytest tests/test_login.py -v -m smoke

test-chrome:
	BROWSER=chrome pytest tests/ -v

test-firefox:
	BROWSER=firefox pytest tests/ -v

clean:
	rm -rf reports/ screenshots/ .pytest_cache/ __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

report:
	pytest tests/ -v --html=reports/report.html --self-contained-html
