-- PostgreSQL initialization script for 9Scraper
-- This script sets up the database with proper extensions and initial configuration

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- Create indexes for performance
-- These will be created automatically by SQLAlchemy migrations,
-- but we can add them here for initial setup

-- Set up database configuration
ALTER DATABASE ninescrap SET timezone TO 'UTC';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE ninescrap TO postgres;

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully';
END
$$;
