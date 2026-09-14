"""Common response schemas."""

from typing import Any, Dict, Optional

from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None


class HealthComponent(BaseModel):
    status: str
    detail: Optional[str] = None
    latency_ms: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"
    components: Dict[str, HealthComponent]


class DashboardStats(BaseModel):
    downloads_today: int
    downloads_total: int
    completed: int
    failed: int
    cancelled: int
    volume_downloaded_bytes: int
    current_speed_bps: float
    active_workers: int
    jobs_in_queue: int
    jobs_downloading: int
    jobs_paused: int
