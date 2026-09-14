"""API v1 router."""

from fastapi import APIRouter

from app.api.v1 import auth, jobs, dashboard, health

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(jobs.router)
api_router.include_router(dashboard.router)
api_router.include_router(health.router)
