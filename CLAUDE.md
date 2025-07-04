# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

9Scraper is a full-stack web scraping platform that collects business data from multiple sources (Google Maps, Yelp, Yellow Pages, etc.) using a microservices architecture.

## Tech Stack

- **Backend**: FastAPI (Python 3.11+), SQLAlchemy, PostgreSQL, Redis, Celery, Playwright
- **Frontend**: React 18 with TypeScript, Vite, Redux Toolkit, Tailwind CSS, Socket.io
- **Infrastructure**: Docker, Docker Compose, Nginx

## Essential Commands

### Development Workflow
```bash
make install    # Initial setup (creates .env from .env.example)
make dev        # Start development environment
make test       # Run all tests (backend pytest + frontend tests)
make lint       # Run linting (flake8, mypy, frontend lint)
make format     # Format code (black, isort for backend)
make logs       # View application logs
make status     # Check service status
```

### Database Operations
```bash
make migrate    # Run database migrations
make migration  # Create new migration (prompts for name)
make backup     # Backup database
```

### Production Deployment
```bash
make prod       # Deploy production environment
make update     # Update and rebuild services
make clean      # Clean up containers and volumes
```

## Architecture Overview

### Backend Structure (/backend)
- `app/api/` - REST API endpoints (FastAPI routers)
- `app/core/` - Core configurations (database, celery, config)
- `app/models/` - SQLAlchemy database models
- `app/schemas/` - Pydantic schemas for validation
- `app/scraper/` - Web scraping implementations for each source
- `app/services/` - Business logic (data processing, deduplication)
- `app/tasks/` - Celery background tasks
- `app/utils/` - Utility functions

### Frontend Structure (/frontend)
- `src/components/` - Reusable React components
- `src/pages/` - Page components (Dashboard, Jobs, Results)
- `src/services/` - API and WebSocket client services
- `src/store/` - Redux store configuration
- `src/hooks/` - Custom React hooks
- `src/types/` - TypeScript type definitions

### Key Services Architecture
1. **API Server** (FastAPI) - Handles HTTP requests, authentication, job management
2. **Celery Workers** - Execute scraping tasks asynchronously
3. **Redis** - Message broker for Celery, caching, rate limiting
4. **PostgreSQL** - Primary data storage
5. **WebSocket Server** - Real-time progress updates to frontend

### Scraping Flow
1. User creates job via API → stored in PostgreSQL
2. API enqueues Celery task → Redis message queue
3. Celery worker picks up task → executes scraper
4. Scraper uses Playwright → collects data from source
5. Results processed → deduplicated → stored in PostgreSQL
6. Progress updates sent via WebSocket → real-time UI updates

## Development URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Important Patterns

### Adding New Scraper Source
1. Create scraper class in `backend/app/scraper/sources/`
2. Implement `scrape()` method following existing patterns
3. Register in `backend/app/scraper/factory.py`
4. Add source to frontend options in `frontend/src/types/job.ts`

### API Endpoint Pattern
- Use dependency injection for database sessions
- Validate with Pydantic schemas
- Handle errors with proper HTTP status codes
- Follow RESTful conventions

### Frontend State Management
- Use Redux Toolkit for global state
- React Query for server state
- Local component state for UI-only concerns

## Performance Considerations
- Scraping targets: 100-150 businesses/minute
- Use connection pooling for database
- Implement rate limiting per source
- Cache frequently accessed data in Redis

## Testing Approach
- Backend: pytest with fixtures for database/redis
- Frontend: Jest and React Testing Library
- Integration tests use Docker test environment

## Security Notes
- Environment variables in `.env` (never commit)
- API key authentication for production
- CORS configured for frontend origin
- Rate limiting on API endpoints