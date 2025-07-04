# 9Scraper Environment Setup Guide

This guide will help you configure all environment variables for the 9Scraper application.

## Quick Setup

1. Copy the provided `.env` file to your project root
2. Review and update any placeholders marked with `# TODO:`
3. Ensure all external services are configured before running the application

## Environment Variables Reference

### 🔧 Application Settings (Auto-configured)

These settings are pre-configured but can be adjusted as needed:

- **PROJECT_NAME**: Application name (default: "9Scraper")
- **VERSION**: Application version (default: "1.0.0")
- **ENVIRONMENT**: Deployment environment (`development`, `staging`, `production`)
- **DEBUG**: Debug mode (`true` for development, `false` for production)

### 🔐 Security (Auto-generated)

These have been automatically generated with secure values:

- **SECRET_KEY**: Application secret key for JWT tokens and session management
  - ✅ Auto-generated with 64-byte secure random token
  - ⚠️ Never share or commit this value
  
- **ACCESS_TOKEN_EXPIRE_MINUTES**: JWT token expiration time (default: 10080 = 7 days)

### 🗄️ Database Configuration (Partially auto-generated)

- **POSTGRES_SERVER**: Database hostname (default: "postgres" for Docker)
- **POSTGRES_USER**: Database username (default: "postgres")
- **POSTGRES_PASSWORD**: ✅ Auto-generated with secure 32-byte token
- **POSTGRES_DB**: Database name (default: "ninescrap")
- **POSTGRES_PORT**: Database port (default: 5432)

### 📦 Redis Configuration (Partially auto-generated)

- **REDIS_HOST**: Redis hostname (default: "redis" for Docker)
- **REDIS_PORT**: Redis port (default: 6379)
- **REDIS_PASSWORD**: ✅ Auto-generated with secure 32-byte token
- **REDIS_DB**: Redis database number (default: 0)

### 🔄 Celery Configuration (Auto-configured)

These are automatically configured based on your Redis settings:

- **CELERY_BROKER_URL**: Automatically constructed from Redis settings
- **CELERY_RESULT_BACKEND**: Automatically constructed from Redis settings

### 🌐 Proxy Configuration (Requires External Setup)

⚠️ **REQUIRES EXTERNAL SERVICE SETUP**

1. **USE_PROXIES**: Enable/disable proxy usage (`true`/`false`)
2. **PROXY_PROVIDER**: Proxy service provider (default: "brightdata")
3. **PROXY_API_KEY**: 
   - 📋 Sign up at [Bright Data](https://brightdata.com) or your preferred proxy provider
   - Create a new proxy zone
   - Copy the API key from your dashboard
   - Replace `your-proxy-api-key` with your actual key

### 📊 Monitoring & Logging (Optional)

⚠️ **OPTIONAL - For production monitoring**

1. **SENTRY_DSN**: 
   - 📋 Sign up at [Sentry.io](https://sentry.io)
   - Create a new project
   - Copy the DSN from Project Settings → Client Keys
   - Replace `your-sentry-dsn` or leave empty to disable
   
2. **ENABLE_METRICS**: Enable application metrics (`true`/`false`)

### 🕷️ Scraping Configuration (Pre-configured)

These are optimized defaults that can be adjusted based on your needs:

- **MAX_CONCURRENT_SCRAPERS**: Maximum parallel scraping tasks (default: 10)
- **SCRAPER_TIMEOUT**: Request timeout in seconds (default: 30)
- **MAX_RETRIES**: Maximum retry attempts for failed requests (default: 3)
- **DELAY_BETWEEN_REQUESTS**: Delay between requests in seconds (default: 1.0)
- **RATE_LIMIT_PER_MINUTE**: Maximum requests per minute (default: 100)

### 🖥️ Frontend Configuration (Auto-configured for local development)

- **VITE_API_URL**: API endpoint path (default: "/api/v1")
- **VITE_WS_URL**: WebSocket URL (update for production)

### 🔗 CORS Configuration

- **BACKEND_CORS_ORIGINS**: Allowed origins for CORS
  - Default includes localhost ports
  - ⚠️ Update `https://yourdomain.com` with your actual domain for production

## Step-by-Step Setup Instructions

### 1. Local Development Setup

```bash
# The .env file has been created with secure defaults
# No additional setup required for local development
```

### 2. External Services Setup

#### Proxy Service (Required for scraping)

1. Choose a proxy provider:
   - [Bright Data](https://brightdata.com) (recommended)
   - [ScraperAPI](https://scraperapi.com)
   - [Oxylabs](https://oxylabs.io)

2. Sign up and create an account
3. Create a new proxy zone/endpoint
4. Copy your API key
5. Update `PROXY_API_KEY` in `.env`

#### Sentry Monitoring (Optional but recommended for production)

1. Sign up at [Sentry.io](https://sentry.io)
2. Create a new project (select Python/FastAPI)
3. Copy the DSN from project settings
4. Update `SENTRY_DSN` in `.env`

### 3. Production Deployment

Before deploying to production:

1. **Update CORS origins**: Replace `https://yourdomain.com` with your actual domain
2. **Set ENVIRONMENT**: Change to `production`
3. **Set DEBUG**: Change to `false`
4. **Update Frontend URLs**: 
   - Change `VITE_WS_URL` to your production WebSocket URL
5. **Verify all external service keys** are configured

### 4. Docker Deployment

If using Docker Compose, the default hostnames (`postgres`, `redis`) will work automatically. For non-Docker deployments, update:

- `POSTGRES_SERVER` to your database host
- `REDIS_HOST` to your Redis host

## Security Best Practices

1. **Never commit `.env` files** to version control
2. **Rotate secrets regularly** in production
3. **Use environment-specific `.env` files** (e.g., `.env.production`, `.env.staging`)
4. **Restrict database access** to only necessary hosts
5. **Use strong passwords** (already generated for you)

## Troubleshooting

### Database Connection Issues
- Verify `POSTGRES_SERVER` is reachable
- Check firewall rules
- Ensure database service is running

### Redis Connection Issues
- Verify `REDIS_HOST` is reachable
- Check if Redis password is correctly set
- Ensure Redis service is running

### Proxy Issues
- Verify your proxy API key is valid
- Check proxy provider service status
- Ensure you have sufficient proxy credits

## Need Help?

If you encounter any issues during setup:

1. Check application logs for detailed error messages
2. Verify all required environment variables are set
3. Ensure all external services are properly configured
4. Check network connectivity between services