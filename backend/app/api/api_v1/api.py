from fastapi import APIRouter

from app.api.api_v1.endpoints import jobs

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])

# Add more routers as needed
# api_router.include_router(businesses.router, prefix="/businesses", tags=["businesses"])
# api_router.include_router(exports.router, prefix="/exports", tags=["exports"])
