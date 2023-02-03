from fastapi import APIRouter

from api.v1 import route_jobs as v1_route_jobs
from api.v1 import route_users as v1_route_users
from api.v1 import route_authorization as v1_route_authorization
from api import route_job_chat
from api.websockets.route_websocket import WebsocketRoute

api_router = APIRouter()
api_router.include_router(v1_route_users.router, prefix="/v1/users", tags=["users"])
api_router.include_router(v1_route_jobs.router, prefix="/v1/jobs", tags=["jobs"])
api_router.include_router(v1_route_authorization.router, prefix="/v1", tags=["auth"])

api_router.include_router(route_job_chat.router, prefix="", tags=["chat"])

api_router.add_api_websocket_route('/ws/{participant_id}', WebsocketRoute)
