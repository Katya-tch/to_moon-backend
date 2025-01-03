from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

from app.api.users import router_users
from app.api.staircases import router_staircases
from app.api.schedules import router_schedules
from app.api.activities import router_activities

app_router = APIRouter(prefix='/api/v1')
app_router.include_router(router_users)
app_router.include_router(router_staircases)
app_router.include_router(router_schedules)
app_router.include_router(router_activities)


class HealthCheck(BaseModel):
    status: str = 'OK'


@app_router.get(
    '/health',
    tags=['healthcheck'],
    summary='Perform a Health Check',
    status_code=status.HTTP_200_OK,
)
async def get_health() -> HealthCheck:
    return HealthCheck(status='OK')
