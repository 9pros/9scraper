# 9Scraper Makefile
# Convenient commands for development and deployment

.PHONY: help install dev prod clean test lint format docs

# Default target
help:
	@echo "🔍 9Scraper - Available Commands"
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     Install dependencies and setup environment"
	@echo "  make dev         Start development environment"
	@echo ""
	@echo "🚀 Deployment:"
	@echo "  make prod        Deploy production environment"
	@echo "  make stop        Stop all services"
	@echo "  make restart     Restart all services"
	@echo ""
	@echo "🧪 Testing & Quality:"
	@echo "  make test        Run all tests"
	@echo "  make lint        Run linting checks"
	@echo "  make format      Format code"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean       Clean up containers and volumes"
	@echo "  make logs        View application logs"
	@echo "  make status      Show service status"
	@echo ""

# Installation and setup
install:
	@echo "📦 Setting up 9Scraper..."
	@cp -n .env.example .env 2>/dev/null || true
	@echo "✅ Environment file created (if not exists)"
	@echo "⚠️  Please edit .env file with your configuration"

# Development environment
dev:
	@echo "🛠️  Starting development environment..."
	@docker-compose -f docker-compose.dev.yml up -d
	@echo "✅ Development services started"
	@echo "🌐 Services available at:"
	@echo "   PostgreSQL: localhost:5432"
	@echo "   Redis: localhost:6379"

# Production deployment
prod:
	@echo "🚀 Deploying production environment..."
	@./scripts/deploy.sh

# Stop services
stop:
	@echo "🛑 Stopping all services..."
	@docker-compose down
	@docker-compose -f docker-compose.dev.yml down 2>/dev/null || true

# Restart services
restart:
	@echo "🔄 Restarting services..."
	@docker-compose restart

# Testing
test:
	@echo "🧪 Running tests..."
	@cd backend && python -m pytest tests/ -v
	@cd frontend && npm test

# Linting
lint:
	@echo "🔍 Running linting checks..."
	@cd backend && flake8 app/
	@cd backend && mypy app/
	@cd frontend && npm run lint

# Code formatting
format:
	@echo "🎨 Formatting code..."
	@cd backend && black app/
	@cd backend && isort app/
	@cd frontend && npm run format 2>/dev/null || echo "No formatter configured"

# View logs
logs:
	@echo "📋 Viewing application logs..."
	@docker-compose logs -f

# Service status
status:
	@echo "📊 Service Status:"
	@docker-compose ps

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@docker-compose down -v
	@docker-compose -f docker-compose.dev.yml down -v 2>/dev/null || true
	@docker system prune -f
	@echo "✅ Cleanup completed"

# Database migrations
migrate:
	@echo "🗄️  Running database migrations..."
	@docker-compose exec backend alembic upgrade head

# Create new migration
migration:
	@echo "📝 Creating new migration..."
	@read -p "Migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"

# Backup database
backup:
	@echo "💾 Creating database backup..."
	@mkdir -p backups
	@docker-compose exec postgres pg_dump -U postgres ninescrap > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup created in backups/ directory"

# Health check
health:
	@echo "🏥 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ Backend unhealthy"
	@curl -f http://localhost:3000 || echo "❌ Frontend unhealthy"
	@curl -f http://localhost/nginx-health || echo "❌ Nginx unhealthy"

# Update services
update:
	@echo "🔄 Updating services..."
	@git pull
	@docker-compose pull
	@docker-compose up -d --build
	@echo "✅ Services updated"
