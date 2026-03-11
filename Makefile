# Makefile for LearnDrift

.PHONY: help up down build logs clean setup test

help:
	@echo "LearnDrift - Development Commands"
	@echo "=================================="
	@echo "make setup       - Initial setup and build"
	@echo "make up         - Start all services with Docker Compose"
	@echo "make down       - Stop all services"
	@echo "make build      - Build Docker images"
	@echo "make logs       - Show Docker logs"
	@echo "make clean      - Clean up Docker containers and volumes"
	@echo "make backend    - Run backend locally"
	@echo "make frontend   - Run frontend locally"
	@echo "make test       - Run tests"

setup:
	@echo "Setting up LearnDrift..."
	docker-compose build
	@echo "Setup complete! Run 'make up' to start services."

up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name node_modules -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

backend:
	cd backend && python -m venv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt && \
	uvicorn app.main:app --reload

frontend:
	cd frontend && npm install && npm start

test:
	@echo "Running tests..."
	docker-compose exec backend pytest
