import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

with open('{}/ui/html/job_chat.html'.format(os.getcwd()), 'r') as file:
    html = file.read()


@router.get("/job-chat")
def display_job_board():
    return HTMLResponse(html)
