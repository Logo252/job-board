from fastapi import FastAPI
from core.config import settings
from api.base import api_router
from db.session import engine
from db.base import Base


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    # drop_tables()
    create_tables()
    return app


def include_router(app):
    app.include_router(api_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)


app = start_application()
