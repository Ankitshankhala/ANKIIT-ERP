# Makefile for ANKIIT ERP

# Default command
.DEFAULT_GOAL := help

# ==============================================================================
# Development Environment
# ==============================================================================

dev: ## Start all services with Docker Compose in detached mode
	@echo "🚀 Starting development environment..."
	@docker-compose up -d

down: ## Stop and remove all services
	@echo "🛑 Stopping development environment..."
	@docker-compose down

logs: ## Tail the logs of all running services
	@echo "📜 Tailing logs..."
	@docker-compose logs -f

logs-backend: ## Tail the logs of the backend service
	@echo "📜 Tailing backend logs..."
	@docker-compose logs -f backend

logs-frontend: ## Tail the logs of the frontend service
	@echo "📜 Tailing frontend logs..."
	@docker-compose logs -f frontend

# ==============================================================================
# Quality & Auditing
# ==============================================================================

lint-backend: ## Run flake8 linter on the backend
	@echo "🐍 Linting backend with flake8..."
	@docker-compose exec backend flake8 .

type-check-backend: ## Run mypy type checker on the backend
	@echo "🐍 Type checking backend with mypy..."
	@docker-compose exec backend mypy .

lint-frontend: ## Run ESLint on the frontend
	@echo "🤖 Linting frontend with ESLint..."
	@docker-compose exec frontend npm run lint --if-present

type-check-frontend: ## Run TypeScript compiler on the frontend
	@echo "🤖 Type checking frontend with tsc..."
	@docker-compose exec frontend npm run type-check --if-present

audit-backend: ## Run pip-audit for security vulnerabilities in backend
	@echo "🔒 Auditing backend dependencies..."
	@docker-compose exec backend pip-audit

audit-frontend: ## Run npm audit for security vulnerabilities in frontend
	@echo "🔒 Auditing frontend dependencies..."
	@docker-compose exec frontend npm audit

# ==============================================================================
# Database
# ==============================================================================

db-shell: ## Access the PostgreSQL shell
	@echo "🗄️ Accessing PostgreSQL shell..."
	@docker-compose exec postgres psql -U ankiit_user -d ankiit_erp

# ==============================================================================
# Help
# ==============================================================================

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: dev down logs logs-backend logs-frontend lint-backend type-check-backend lint-frontend type-check-frontend audit-backend audit-frontend db-shell help
