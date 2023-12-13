from datetime import datetime

from sqlalchemy.orm import Session

from db.models.job import Job as JobModel
from schemas.job import JobCreate, JobUpdate


def create_job(db: Session, job: JobCreate):
    db_job = JobModel()
    for var, value in vars(job).items():
        if value:
            setattr(db_job, var, value)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def get_job_by_id(db: Session, job_id: int):
    return db.query(JobModel).filter(JobModel.id == job_id).first()


def get_all_jobs(db: Session, skip: int = 0, limit: int = 100):
    q = db.query(JobModel)
    return q.offset(skip).limit(limit).all()


def edit_job(db: Session, job_id: int, job: JobUpdate):
    db_job = db.query(JobModel).get(job_id)
    db_job.updated_at = datetime.now(datetime.timezone.utc)

    for var, value in vars(job).items():
        if value:
            setattr(db_job, var, value)

    db.add(db_job)
    db.commit()
    return db_job


def delete_job(db: Session, job_id: int):
    db_comment = db.query(JobModel).get(job_id)
    db_comment.updated_at = datetime.now(datetime.timezone.utc)
    db_comment.is_archived = True

    db.add(db_comment)
    db.commit()
    return db_comment
