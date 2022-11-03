from fastapi import APIRouter

from api.v1 import route_jobs as v1_route_jobs
from api.v1 import route_users as v1_route_users

api_router = APIRouter()
api_router.include_router(v1_route_users.router, prefix="/v1/users", tags=["users"])
api_router.include_router(v1_route_jobs.router, prefix="/v1/jobs", tags=["jobs"])
