"""Dashboard and history endpoints."""

from fastapi import APIRouter

from app.core.deps import CurrentUser, DbSession
from app.schemas.common import DashboardStats
from app.services.job_service import JobService

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(current_user: CurrentUser, db: DbSession):
    service = JobService(db)
    stats = await service.get_dashboard_stats(current_user)
    return DashboardStats(**stats)
