import asyncio
from typing import Any, Dict, List
from uuid import UUID

import structlog
from celery import current_task
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models import Business, JobResult, JobStatus, ScrapingJob
from app.scraper import scraper_manager
from app.services.data_processor import DataProcessor
from app.services.deduplication import DeduplicationEngine

logger = structlog.get_logger(__name__)


@celery_app.task(bind=True)
def scrape_businesses(self, job_id: str) -> Dict[str, Any]:
    """Celery task to scrape businesses for a job."""
    return asyncio.run(_scrape_businesses_async(self, job_id))


async def _scrape_businesses_async(task, job_id: str) -> Dict[str, Any]:
    """Async implementation of business scraping."""
    async with AsyncSessionLocal() as db:
        try:
            # Get job details
            job = await db.get(ScrapingJob, UUID(job_id))
            if not job:
                raise ValueError(f"Job {job_id} not found")
            
            # Update job status
            job.status = JobStatus.RUNNING
            if hasattr(current_task, 'update_state'):
                current_task.update_state(
                    state='PROGRESS',
                    meta={'progress': 0, 'status': 'Starting scraping...'}
                )
            await db.commit()
            
            logger.info(f"Starting scraping job {job_id}: {job.keyword} in {job.location}")
            
            # Scrape from all sources
            all_results = await scraper_manager.scrape_multiple_sources(
                sources=job.sources,
                keyword=job.keyword,
                location=job.location,
                radius_miles=job.radius_miles,
                use_proxy=True
            )
            
            # Process and deduplicate results
            processor = DataProcessor()
            deduplicator = DeduplicationEngine()
            
            total_businesses = 0
            processed_count = 0
            
            for source, businesses in all_results.items():
                if not businesses:
                    continue
                    
                logger.info(f"Processing {len(businesses)} businesses from {source}")
                
                for business_data in businesses:
                    try:
                        # Process business data
                        processed_data = await processor.process_business_data(business_data)
                        
                        # Check for duplicates
                        existing_business = await deduplicator.find_duplicate(
                            db, processed_data
                        )
                        
                        if existing_business:
                            business = existing_business
                        else:
                            # Create new business
                            business = Business(**processed_data)
                            db.add(business)
                            await db.flush()  # Get the ID
                        
                        # Create job result association
                        job_result = JobResult(
                            job_id=job.id,
                            business_id=business.id,
                            source=source,
                            confidence_score=1.0,  # Could be improved with ML scoring
                        )
                        db.add(job_result)
                        
                        processed_count += 1
                        
                        # Update progress
                        if hasattr(current_task, 'update_state'):
                            progress = min(90, int((processed_count / len(businesses)) * 90))
                            current_task.update_state(
                                state='PROGRESS',
                                meta={
                                    'progress': progress,
                                    'status': f'Processed {processed_count} businesses...'
                                }
                            )
                        
                    except Exception as e:
                        logger.warning(f"Error processing business: {e}")
                        continue
                
                total_businesses += len(businesses)
            
            # Update job completion
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.results_count = processed_count
            
            await db.commit()
            
            logger.info(f"Completed scraping job {job_id}: {processed_count} businesses processed")
            
            return {
                "job_id": job_id,
                "status": "completed",
                "total_found": total_businesses,
                "total_processed": processed_count,
                "sources": list(all_results.keys())
            }
            
        except Exception as e:
            logger.error(f"Error in scraping job {job_id}: {e}")
            
            # Update job status to failed
            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                await db.commit()
            
            raise
