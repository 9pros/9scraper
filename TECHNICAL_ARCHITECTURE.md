# 9Scraper Technical Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer (Nginx)                     │
└─────────────────────────────────────────────────────────────────┘
                                    │
        ┌──────────────────────────┴────────────────────────────┐
        │                                                        │
┌───────▼────────┐                                    ┌─────────▼────────┐
│   Frontend     │                                    │    API Server    │
│  (React SPA)   │                                    │   (FastAPI)      │
└────────────────┘                                    └──────────────────┘
                                                               │
                                ┌──────────────────────────────┼────────────────────────────────┐
                                │                              │                                │
                        ┌───────▼────────┐          ┌─────────▼────────┐           ┌───────────▼──────────┐
                        │  Task Queue    │          │   PostgreSQL     │           │   Redis Cache        │
                        │   (Celery)     │          │   Database       │           │   & Session Store    │
                        └────────────────┘          └──────────────────┘           └──────────────────────┘
                                │
                    ┌──────────┴───────────┬────────────────────┬─────────────────┐
                    │                      │                    │                 │
            ┌───────▼────────┐   ┌────────▼────────┐  ┌────────▼────────┐  ┌─────▼──────┐
            │ Scraper Worker │   │ Scraper Worker  │  │ Scraper Worker  │  │   More...  │
            │   (Celery)     │   │   (Celery)      │  │   (Celery)      │  │            │
            └────────────────┘   └─────────────────┘  └─────────────────┘  └────────────┘
                    │                      │                    │
            ┌───────▼────────────────────────────────────────────┐
            │           Proxy Pool (Residential IPs)              │
            └─────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. API Server (FastAPI)
- **Purpose**: Handle HTTP requests, manage jobs, serve results
- **Key Features**:
  - Async request handling
  - WebSocket support for real-time updates
  - Automatic API documentation
  - Request validation with Pydantic
  - JWT authentication

### 2. Task Queue (Celery)
- **Purpose**: Distributed task processing
- **Configuration**:
  - Broker: Redis
  - Result Backend: Redis
  - Concurrency: 4 workers per instance
  - Task Routing: Priority-based queues

### 3. Database (PostgreSQL)
- **Purpose**: Persistent storage for business data and job metadata
- **Key Features**:
  - JSONB for flexible business data
  - Full-text search capabilities
  - Geospatial queries with PostGIS
  - Partitioning for large datasets

### 4. Scraper Workers
- **Purpose**: Execute scraping tasks
- **Technology**: Playwright (headless browser)
- **Capabilities**:
  - Multi-browser support
  - Stealth plugins
  - Proxy rotation
  - CAPTCHA handling

## Data Flow

1. **Job Creation**
   ```
   User → Frontend → API → Database (Job Created) → Task Queue
   ```

2. **Scraping Process**
   ```
   Task Queue → Worker → Proxy → Target Site → Worker → Database
   ```

3. **Real-time Updates**
   ```
   Worker → Redis Pub/Sub → WebSocket → Frontend
   ```

4. **Result Retrieval**
   ```
   Frontend → API → Database → Data Processing → Response
   ```

## Security Considerations

### 1. API Security
- Rate limiting per IP and API key
- Request size limits
- Input validation and sanitization
- CORS policy enforcement

### 2. Data Security
- Encryption at rest (PostgreSQL)
- Encryption in transit (TLS)
- Secure credential storage
- Proxy authentication

### 3. Infrastructure Security
- Container isolation
- Network segmentation
- Regular security updates
- Monitoring and alerting

## Scalability Strategy

### Horizontal Scaling
- **API Servers**: Load balanced, stateless
- **Workers**: Auto-scaling based on queue depth
- **Database**: Read replicas for queries
- **Cache**: Redis cluster for high availability

### Performance Optimizations
- Database query optimization
- Result caching strategy
- Batch processing for exports
- CDN for static assets

## Monitoring & Observability

### Metrics Collection
- **Prometheus**: System and application metrics
- **Grafana**: Visualization dashboards
- **Custom Metrics**:
  - Scraping success rate
  - Average response time
  - Queue depth
  - Proxy health

### Logging
- **Application Logs**: Structured JSON format
- **Access Logs**: Nginx access logs
- **Error Tracking**: Sentry integration
- **Log Aggregation**: ELK stack

### Alerting
- High error rate alerts
- Queue backup alerts
- Database connection pool alerts
- Proxy failure alerts

## Deployment Strategy

### Development
```bash
docker-compose -f docker-compose.dev.yml up
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables
```env
# Database
DATABASE_URL=postgresql://user:pass@host/db
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://redis:6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Proxy Provider
PROXY_PROVIDER=brightdata
PROXY_API_KEY=your_key_here

# Security
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

## Database Schema

### Core Tables

```sql
-- Businesses table
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(500),
    data JSONB,  -- Flexible additional data
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Scraping jobs table
CREATE TABLE scraping_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword VARCHAR(255) NOT NULL,
    location GEOGRAPHY(POINT),
    radius_miles INTEGER,
    status VARCHAR(50),
    progress INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);

-- Results association
CREATE TABLE job_results (
    job_id UUID REFERENCES scraping_jobs(id),
    business_id UUID REFERENCES businesses(id),
    source VARCHAR(50),
    confidence_score DECIMAL(3,2),
    PRIMARY KEY (job_id, business_id)
);
```

## Error Handling Strategy

### Retry Logic
- Exponential backoff with jitter
- Max 3 retries per task
- Dead letter queue for failed tasks

### Error Categories
1. **Transient**: Network timeouts, rate limits
2. **Permanent**: Invalid selectors, blocked access
3. **Critical**: Database connection, proxy failure

## Performance Benchmarks

### Target Metrics
- API Response: < 200ms (p95)
- Scraping Rate: 100-150 businesses/min
- Database Query: < 50ms (p95)
- Export Generation: < 5s for 10k records

### Load Testing
```bash
# Using Locust
locust -f tests/load_test.py --host=http://localhost:8000
```

---

**Last Updated**: 2025-07-04