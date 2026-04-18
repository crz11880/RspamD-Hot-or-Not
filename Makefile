.PHONY: help install run run-dev test clean docker-build docker-up docker-down lint

help:
	@echo "RspamdHotOrNot - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        Install dependencies and setup"
	@echo "  make dev-install    Install with dev dependencies"
	@echo ""
	@echo "Running:"
	@echo "  make run            Run production server"
	@echo "  make run-dev        Run development server with reload"
	@echo ""
	@echo "Database:"
	@echo "  make db-init        Initialize database"
	@echo "  make db-reset       Reset database (⚠️  deletes all data)"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test           Run tests"
	@echo "  make lint           Run linter"
	@echo "  make format         Format code with black"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-up      Start with docker-compose"
	@echo "  make docker-down    Stop docker-compose"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          Clean cache and temp files"
	@echo "  make help           Show this help message"

install:
	@bash install.sh

dev-install:
	@. venv/bin/activate; pip install -r requirements.txt -e ".[dev]"

run:
	@. venv/bin/activate; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

run-dev:
	@. venv/bin/activate; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

db-init:
	@. venv/bin/activate; python -c "from app.db import init_db; init_db(); print('Database initialized')"

db-reset:
	@rm -f data/db/*.db
	@. venv/bin/activate; python -c "from app.db import init_db; init_db(); print('Database reset')"

test:
	@. venv/bin/activate; pytest -v

lint:
	@. venv/bin/activate; flake8 app/ --max-line-length=100

format:
	@. venv/bin/activate; black app/ --line-length=100

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf htmlcov
	@rm -rf dist build *.egg-info
	@echo "Cache cleaned"

docker-build:
	@docker build -t rspamd-hot-or-not:latest .

docker-up:
	@docker-compose up -d

docker-down:
	@docker-compose down

.DEFAULT_GOAL := help
