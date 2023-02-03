from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import Response
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.responses import JSONResponse

from core import jwt_manager
from core.oauth_settings import oauth
from db.repository.users import retrieve_user_by_email, create_new_user
from db.session import get_db
from schemas.users import UserCreate

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for(name='authenticate')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth")
async def authenticate(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        raise jwt_manager.CREDENTIALS_EXCEPTION

    user_data = access_token.get('userinfo')
    email = user_data.get('email')

    if not retrieve_user_by_email(email=email, db=db):
        username = user_data.get('name')
        user_create_schema = UserCreate(username=username, email=email, password='test')
        create_new_user(user=user_create_schema, db=db)

    jwt = jwt_manager.create_token(email)

    # return the JWT token to the user so that user could make requests to our API endpoints
    return JSONResponse({'access_token': jwt})


@router.get("/login/home")
def get_login_home(request: Request, db: Session = Depends(get_db)):
    # user = retrieve_user_by_email(email=request.user.email, db=db)
    # if user:
    #     name = user.get('name')
    #     return HTMLResponse(f'<p>Hello {name}!. You are already logged in. </p><a href=/v1/logout>Logout</a>')

    return HTMLResponse('<a href=/v1/login>Login</a>')


@router.get("/unprotected-endpoint")
def get_auth_data(request: Request):
    return JSONResponse({'result': 'Unprotected endpoint'})


@router.get("/protected-endpoint")
def get_auth_data(request: Request, current_email: str = Depends(jwt_manager.get_current_user_email), db: Session = Depends(get_db)):
    if retrieve_user_by_email(email=current_email, db=db):
        return JSONResponse({'result': 'Protected endpoint', 'access_token': jwt_manager.create_token(current_email)})
    raise jwt_manager.CREDENTIALS_EXCEPTION


@router.get("/logout")
async def logout(request: Request):
    # TO DO: Expire JWT token
    return RedirectResponse(url='/v1/login/home')
