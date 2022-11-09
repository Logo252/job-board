from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from db.repository.users import create_new_user
from db.session import get_db
from schemas.users import UserCreate
from schemas.users import UserShow

router = APIRouter()


@router.post("/", response_model=UserShow)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user

# TO DO:  Add changes here for additional routes to be able update and delete user
