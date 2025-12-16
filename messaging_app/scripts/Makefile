.PHONY: help quality test coverage clean

# Help
help:
	@echo "Available commands:"
	@echo "  make quality    - Run all quality checks"
	@echo "  make lint       - Run flake8 linting"
	@echo "  make format     - Format code with black and isort"
	@echo "  make test       - Run tests with coverage"
	@echo "  make coverage   - Generate coverage report"
	@echo "  make clean      - Clean up generated files"
	@echo "  make all        - Run quality, test, and coverage"

# Quality checks
quality:
	@echo "Running quality checks..."
	python scripts/run_quality_checks.py

lint:
	@echo "Running flake8 linting..."
	flake8 alx_travel_app/ --max-line-length=120 --exclude=migrations

format:
	@echo "Formatting code..."
	black alx_travel_app/
	isort alx_travel_app/

# Testing
test:
	@echo "Running tests..."
	pytest alx_travel_app/ tests/ -v --tb=short

coverage:
	@echo "Running tests with coverage..."
	pytest alx_travel_app/ tests/ \
		--cov=alx_travel_app \
		--cov-report=html:coverage-reports/html \
		--cov-report=xml:coverage-reports/coverage.xml \
		--cov-report=term-missing

# Combined
all: quality test coverage

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf coverage-reports/ test-reports/ .pytest_cache/ .mypy_cache/
	rm -rf htmlcov/ .coverage *.egg-info/ dist/ build/
	