from datetime import datetime
from typing import List, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_db
from app.core.celery_app import celery_app
from app.models import Business, JobResult, JobStatus, ScrapingJob
from app.schemas import (
    JobResultsResponse,
    PaginatedResponse,
    ScrapingJob as ScrapingJobSchema,
    ScrapingJobCreate,
    ScrapingJobUpdate,
    SuccessResponse,
)

router = APIRouter()
logger = structlog.get_logger(__name__)


@router.post("/", response_model=ScrapingJobSchema)
async def create_scraping_job(
    job_data: ScrapingJobCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ScrapingJobSchema:
    """Create a new scraping job."""
    try:
        # Create job instance
        job = ScrapingJob(
            keyword=job_data.keyword,
            location=job_data.location,
            radius_miles=job_data.radius_miles,
            sources=job_data.sources,
            options=job_data.options.dict(),
            status=JobStatus.PENDING,
        )
        
        db.add(job)
        await db.flush()  # Get the ID
        await db.commit()
        
        # Start scraping task
        celery_app.send_task(
            "app.tasks.scraping.scrape_businesses",
            args=[str(job.id)],
            queue="scraping"
        )
        
        logger.info(f"Created scraping job {job.id} for '{job.keyword}' in '{job.location}'")
        
        return ScrapingJobSchema.from_orm(job)
        
    except Exception as e:
        logger.error(f"Error creating scraping job: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=PaginatedResponse[ScrapingJobSchema])
async def list_jobs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[JobStatus] = None,
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ScrapingJobSchema]:
    """List all scraping jobs with pagination."""
    try:
        # Build query
        stmt = select(ScrapingJob).order_by(desc(ScrapingJob.created_at))
        
        if status:
            stmt = stmt.where(ScrapingJob.status == status)
        
        # Add pagination
        offset = (page - 1) * size
        stmt = stmt.offset(offset).limit(size)
        
        # Execute query
        result = await db.execute(stmt)
        jobs = result.scalars().all()
        
        # Get total count
        count_stmt = select(ScrapingJob)
        if status:
            count_stmt = count_stmt.where(ScrapingJob.status == status)
        
        count_result = await db.execute(select(count_stmt.subquery().c.id).count())
        total = count_result.scalar()
        
        # Calculate pages
        pages = (total + size - 1) // size
        
        return PaginatedResponse(
            items=[ScrapingJobSchema.from_orm(job) for job in jobs],
            total=total,
            page=page,
            size=size,
            pages=pages,
        )
        
    except Exception as e:
        logger.error(f"Error listing jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}", response_model=ScrapingJobSchema)
async def get_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ScrapingJobSchema:
    """Get a specific scraping job."""
    try:
        job = await db.get(ScrapingJob, job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return ScrapingJobSchema.from_orm(job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{job_id}/results", response_model=JobResultsResponse)
async def get_job_results(
    job_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> JobResultsResponse:
    """Get results for a specific job."""
    try:
        # Get job
        job = await db.get(ScrapingJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get results with pagination
        stmt = (
            select(Business)
            .join(JobResult)
            .where(JobResult.job_id == job_id)
            .order_by(Business.name)
            .offset((page - 1) * size)
            .limit(size)
        )
        
        result = await db.execute(stmt)
        businesses = result.scalars().all()
        
        # Get total count
        count_stmt = select(JobResult).where(JobResult.job_id == job_id)
        count_result = await db.execute(select(count_stmt.subquery().c.id).count())
        total = count_result.scalar()
        
        pages = (total + size - 1) // size
        
        return JobResultsResponse(
            job=ScrapingJobSchema.from_orm(job),
            businesses=[Business.from_orm(business) for business in businesses],
            total_results=total,
            page=page,
            size=size,
            pages=pages,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job results {job_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{job_id}", response_model=ScrapingJobSchema)
async def update_job(
    job_id: UUID,
    job_update: ScrapingJobUpdate,
    db: AsyncSession = Depends(get_db),
) -> ScrapingJobSchema:
    """Update a scraping job (mainly for status updates)."""
    try:
        job = await db.get(ScrapingJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Update fields
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        # Set completion time if job is completed
        if job_update.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            job.completed_at = datetime.utcnow()
        
        await db.commit()
        
        return ScrapingJobSchema.from_orm(job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job {job_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{job_id}", response_model=SuccessResponse)
async def cancel_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SuccessResponse:
    """Cancel a scraping job."""
    try:
        job = await db.get(ScrapingJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            raise HTTPException(status_code=400, detail="Job cannot be cancelled")
        
        # Update job status
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        await db.commit()
        
        # TODO: Cancel Celery task
        # celery_app.control.revoke(task_id, terminate=True)
        
        logger.info(f"Cancelled job {job_id}")
        
        return SuccessResponse(message="Job cancelled successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job {job_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{job_id}/restart", response_model=ScrapingJobSchema)
async def restart_job(
    job_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> ScrapingJobSchema:
    """Restart a failed or cancelled job."""
    try:
        job = await db.get(ScrapingJob, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        if job.status not in [JobStatus.FAILED, JobStatus.CANCELLED]:
            raise HTTPException(status_code=400, detail="Job cannot be restarted")
        
        # Reset job status
        job.status = JobStatus.PENDING
        job.progress = 0
        job.error_message = None
        job.retry_count += 1
        job.completed_at = None
        
        await db.commit()
        
        # Start new scraping task
        celery_app.send_task(
            "app.tasks.scraping.scrape_businesses",
            args=[str(job.id)],
            queue="scraping"
        )
        
        logger.info(f"Restarted job {job_id}")
        
        return ScrapingJobSchema.from_orm(job)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error restarting job {job_id}: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
