DOCKER_COMPOSE_FILE=docker-compose.yml

.PHONY: all
all: help

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  setup-env      - Set up the initial environment"
	@echo "  build          - Build all Docker images"
	@echo "  up             - Start all services using docker-compose"
	@echo "  down           - Stop all services using docker-compose"
	@echo "  restart        - Restart all services using docker-compose"

.PHONY: setup-env
setup-env:
	@echo "Setting up the initial environment..."
	uv sync --frozen --no-install-project --no-dev

.PHONY: build
build:
	@echo "Building all Docker images..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

.PHONY: up
up:
	@echo "Starting all services..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

.PHONY: down
down:
	@echo "Stopping all services..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: restart
restart: down up
