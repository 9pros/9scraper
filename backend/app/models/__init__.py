"""Database models for 9Scraper."""

from .business import Business
from .job import JobStatus, ScrapingJob
from .result import JobResult

__all__ = [
    "Business",
    "JobResult", 
    "JobStatus",
    "ScrapingJob",
]
