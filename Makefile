.DEFAULT_GOAL := help

IMAGE_NAME := golden-raspberry-awards-api
CONTAINER_NAME := golden-raspberry-awards-api

.PHONY: help sync run dev test lint format format-check typecheck check docker-build docker-run docker-stop

help: ## Show the available development commands.
	@awk 'BEGIN { FS = ":.*##" } /^[a-zA-Z0-9_-]+:.*##/ { printf "%-16s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

sync: ## Synchronize dependencies from the lock file.
	uv sync --frozen

run: ## Start the API without hot reload.
	uv run --frozen uvicorn --app-dir src app.main:app --host 0.0.0.0 --port 8000

dev: ## Start the API with hot reload.
	uv run --frozen uvicorn --app-dir src app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run the integration tests.
	uv run --frozen pytest

lint: ## Run Ruff lint checks.
	uv run --frozen ruff check .

format: ## Format the code with Ruff.
	uv run --frozen ruff format .

format-check: ## Check code formatting with Ruff.
	uv run --frozen ruff format --check .

typecheck: ## Run mypy.
	uv run --frozen mypy .

check: lint format-check typecheck test ## Run all local CI quality checks.

docker-build: ## Build the production image.
	docker build --tag $(IMAGE_NAME) .

docker-run: ## Run the production image on port 8000.
	docker run --detach --name $(CONTAINER_NAME) --publish 8000:8000 $(IMAGE_NAME)

docker-stop: ## Stop and remove the container started by docker-run.
	@if docker container inspect "$(CONTAINER_NAME)" >/dev/null 2>&1; then docker rm --force "$(CONTAINER_NAME)"; fi
