from sqlalchemy.orm import Session

from db.models.jobs import Job
from schemas.jobs import JobCreate


def create_new_job(job: JobCreate, db: Session, owner_id: int):
    job_object = Job(**job.dict(), owner_id=owner_id)
    db.add(job_object)
    db.commit()
    db.refresh(job_object)
    return job_object


def retrieve_job(id: int, db: Session, owner_id: int):
    item = db.query(Job).filter(Job.id == id, Job.owner_id == owner_id).first()
    return item


def list_active_jobs(db: Session, owner_id: int):
    jobs = db.query(Job).filter(Job.is_active == True, Job.owner_id == owner_id).all()
    return jobs


def update_job_by_id(id: int, job: JobCreate, db: Session, owner_id):
    existing_job = db.query(Job).filter(Job.id == id, Job.owner_id == owner_id)
    if not existing_job.first():
        return 0
    job.__dict__.update(
        owner_id=owner_id
    )  # update dictionary with new key value of owner_id
    existing_job.update(job.__dict__)
    db.commit()
    return 1


def delete_job_by_id(id: int, db: Session):
    existing_job = db.query(Job).filter(Job.id == id)
    if not existing_job.first():
        return 0
    existing_job.delete(synchronize_session=False)
    db.commit()
    return 1
