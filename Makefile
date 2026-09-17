.PHONY: help install install-dev run test coverage lint format type-check security-scan clean docker-build docker-run

help:
	@echo "Motus - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo ""
	@echo "Run:"
	@echo "  make run            Run application"
	@echo "  make run-venv       Run with virtual environment Python"
	@echo ""
	@echo "Testing:"
	@echo "  make test           Run test suite"
	@echo "  make coverage       Generate coverage report"
	@echo "  make test-unit      Run unit tests only"
	@echo "  make test-integration  Run integration tests only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint           Run linters (flake8)"
	@echo "  make format         Format code (black, isort)"
	@echo "  make type-check     Run type checking (mypy)"
	@echo "  make security-scan  Run security scans (bandit, safety)"
	@echo "  make quality        Run all quality checks"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run in Docker"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          Remove build artifacts and cache"

install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

install-dev:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .
	pre-commit install

run:
	python3 -m motus

run-venv:
	./venv/bin/python -m motus

test:
	pytest --cov=motus --cov-report=term-missing -v

coverage:
	pytest --cov=motus --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

lint:
	flake8 src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/motus --strict

security-scan:
	bandit -r src/motus
	safety check

quality: format lint type-check test security-scan
	@echo "All quality checks passed!"

docker-build:
	docker compose build

docker-run:
	docker compose up

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist htmlcov .coverage bandit-report.json
	@echo "Cleanup complete!"
