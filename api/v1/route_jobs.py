from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from db.repository.jobs import create_new_job
from db.repository.jobs import delete_job_by_id
from db.repository.jobs import list_active_jobs
from db.repository.jobs import retrieve_job
from db.repository.jobs import update_job_by_id
from db.session import get_db
from schemas.jobs import JobCreate
from schemas.jobs import ShowJob

router = APIRouter()


@router.post("/", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    job = create_new_job(job=job, db=db, owner_id=current_user)
    return job


@router.get("/{id}", response_model=ShowJob)
def read_job(id: int, db: Session = Depends(get_db)):
    job = retrieve_job(id=id, db=db)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with this id {id} does not exist",
        )
    return job


@router.get("", response_model=List[ShowJob])  # new
def read_jobs(db: Session = Depends(get_db)):
    jobs = list_active_jobs(db=db)
    return jobs


@router.put("/{id}")
def update_job(id: int, job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    message = update_job_by_id(id=id, job=job, db=db, owner_id=current_user)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )
    return job


@router.delete("/{id}")
def delete_job(id: int, db: Session = Depends(get_db)):
    current_user_id = 1
    message = delete_job_by_id(id=id, db=db, owner_id=current_user_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {id} not found"
        )
