from sqlalchemy.orm import Session

from core.hashing import Hasher
from db.models.users import User
from schemas.users import UserCreate, UserPatch


def create_new_user(user: UserCreate, db: Session):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def retrieve_user_by_id(id: int, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user


def patch_user_by_id(id: int, user: UserPatch, db: Session):
    existing_user = db.query(User).filter(User.id == id)
    if not existing_user.first():
        return 0

    if 'password' in user.__dict__ and user.__dict__['password'] is not None:
        user.__dict__.update(
            hashed_password=Hasher.get_password_hash(user.password)
        )

    user.__dict__.pop('password')

    updated_user_data = {k: v for k, v in user.__dict__.items() if v is not None}

    existing_user.update(updated_user_data)
    db.commit()

    return 1


def delete_user_by_id(id: int, db: Session):
    existing_user = db.query(User).filter(User.id == id)
    if not existing_user.first():
        return 0
    existing_user.delete(synchronize_session=False)
    db.commit()
    return 1
