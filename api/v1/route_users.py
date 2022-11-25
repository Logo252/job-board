from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from db.repository.users import create_new_user, delete_user_by_id, retrieve_user_by_id, patch_user_by_id
from db.session import get_db
from schemas.users import UserCreate
from schemas.users import UserPatch
from schemas.users import UserShow

router = APIRouter()


@router.post("/", response_model=UserShow)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/{id}", response_model=UserShow)
def read_user(id: int, db: Session = Depends(get_db)):
    user = retrieve_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id {id} does not exist",
        )
    return user


@router.patch("/{id}")
def patch_user(id: int, user: UserPatch, db: Session = Depends(get_db)):
    message = patch_user_by_id(id, user, db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )


@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    message = delete_user_by_id(id, db)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found"
        )
