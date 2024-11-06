from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

from app.api.users import router_users
from app.api.staircases import router_staircases

app_router = APIRouter(prefix='/api/v1')
app_router.include_router(router_users)
app_router.include_router(router_staircases)


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
