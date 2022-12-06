import uvicorn
from fastapi import FastAPI
from sqlalchemy_utils import database_exists, create_database

from api.base import api_router
from core.config import settings
from db.base import Base
from db.session import engine


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    # drop_tables()
    create_db()
    create_tables()
    return app


def include_router(app):
    app.include_router(api_router)


def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(bind=engine)


app = start_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
