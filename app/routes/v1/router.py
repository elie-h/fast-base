from fastapi import APIRouter

from app.routes.v1.endpoints import health

router_v1 = APIRouter()
router_v1.include_router(health.router, tags=["health"])
