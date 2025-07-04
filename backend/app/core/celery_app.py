from celery import Celery

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "9scraper",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.scraping"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    result_expires=3600,  # 1 hour
    task_soft_time_limit=1800,  # 30 minutes
    task_time_limit=2400,  # 40 minutes
    worker_max_tasks_per_child=50,
)

# Task routing
celery_app.conf.task_routes = {
    "app.tasks.scraping.scrape_businesses": {"queue": "scraping"},
    "app.tasks.scraping.process_business_data": {"queue": "processing"},
    "app.tasks.scraping.export_results": {"queue": "exports"},
}
