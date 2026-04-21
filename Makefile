# Makefile for VARTAPRAVAH

.PHONY: help build up down logs stop restart shell test clean

help:
	@echo "VARTAPRAVAH - AI News Avatar Generator"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make build          - Build Docker image"
	@echo "  make up             - Start containers (detached)"
	@echo "  make down           - Stop and remove containers"
	@echo "  make logs           - View container logs"
	@echo "  make stop           - Stop containers"
	@echo "  make restart        - Restart containers"
	@echo "  make shell          - Access container shell"
	@echo "  make test           - Run API tests"
	@echo "  make clean          - Remove containers and volumes"
	@echo "  make lint           - Check code style"
	@echo "  make format         - Format Python code"
	@echo ""
	@echo "Examples:"
	@echo "  make up             - Start the app"
	@echo "  make logs           - Watch logs in real-time"
	@echo "  make test           - Test the API"
	@echo ""

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ VARTAPRAVAH is running!"
	@echo "📖 API Docs: http://localhost:8000/docs"
	@echo "💚 Health: http://localhost:8000/health"

down:
	docker-compose down

logs:
	docker-compose logs -f vartapravah

stop:
	docker-compose stop

restart:
	docker-compose restart

shell:
	docker-compose exec vartapravah bash

test:
	@echo "Running API tests..."
	@pip install requests -q 2>/dev/null || true
	python test_api.py

clean:
	docker-compose down -v
	rm -rf output/*.mp4 output/*.wav logs/*.log
	@echo "✅ Cleaned up containers and artifacts"

lint:
	@echo "Checking code style..."
	python -m py_compile app/*.py
	@echo "✅ Syntax check passed"

format:
	@echo "Formatting Python code..."
	python -m autopep8 --in-place app/*.py
	@echo "✅ Code formatted"

ps:
	docker-compose ps

env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env from .env.example"; \
	else \
		echo "⚠️  .env already exists"; \
	fi

health:
	curl -s http://localhost:8000/health | python -m json.tool

info:
	curl -s http://localhost:8000/info | python -m json.tool

docs:
	@echo "📖 Opening API docs..."
	@command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:8000/docs || \
	command -v open >/dev/null 2>&1 && open http://localhost:8000/docs || \
	echo "📖 Open http://localhost:8000/docs in your browser"

stats:
	docker stats vartapravah_ai --no-stream

prune:
	docker system prune -f
	@echo "✅ Cleaned up Docker system"

pull:
	docker-compose pull

deploy:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
	@echo "✅ Deployment complete"

.DEFAULT_GOAL := help
