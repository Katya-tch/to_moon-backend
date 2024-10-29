import uvicorn
from fastapi import FastAPI

from app.router import app_router

app = FastAPI(
    docs_url='/api/v1/schema/swagger',
    redoc_url='/api/v1/schema/redoc',
    openapi_url='/api/v1/schema.json'
)
app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app)
