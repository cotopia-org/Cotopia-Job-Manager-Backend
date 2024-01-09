import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models.job import Job as JobModel
from db.models.job import UserJob as UserJobModel
from schemas.job import JobCreate, JobUpdate
from schemas.userjob import AcceptedJobUpdate


def create_job(db: Session, job: JobCreate, creator_id: int):
    db_job = JobModel(creator_id=creator_id)
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
    db_job.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(job).items():
        if value:
            setattr(db_job, var, value)

    db.add(db_job)
    db.commit()
    return db_job


def delete_job(db: Session, job_id: int):
    db_comment = db.query(JobModel).get(job_id)
    db_comment.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db_comment.is_archived = True

    db.add(db_comment)
    db.commit()
    return db_comment


def accept_job(db: Session, job_id: int, user_id: int):
    the_accept = db.query(UserJobModel).get({"job_id": job_id, "user_id": user_id})
    if the_accept:
        raise HTTPException(status_code=400, detail="The job is already accepted!")
    else:
        the_accept = UserJobModel(user_id=user_id, job_id=job_id)
        db.add(the_accept)
        db.commit()
        db.refresh(the_accept)
        return the_accept


def decline_job(db: Session, job_id: int, user_id: int):
    the_accept = db.query(UserJobModel).get({"job_id": job_id, "user_id": user_id})
    if the_accept:
        db.query(UserJobModel).filter(
            UserJobModel.job_id == job_id and UserJobModel.user_id == user_id
        ).delete()
        db.commit()
        return the_accept
    else:
        raise HTTPException(
            status_code=404, detail="Not found! This job was not accepted by the user!"
        )


def get_an_accepted_job(db: Session, job_id: int, user_id: int):
    return (
        db.query(UserJobModel)
        .filter(UserJobModel.job_id == job_id and UserJobModel.user_id == user_id)
        .first()
    )


def get_accepted_jobs(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    q = db.query(UserJobModel).filter(UserJobModel.user_id == user_id)
    return q.offset(skip).limit(limit).all()


def get_accepted_jobs_by_status(
    db: Session, user_id: int, status: str, skip: int = 0, limit: int = 100
):
    q = db.query(UserJobModel).filter(
        UserJobModel.user_id == user_id and UserJobModel.acceptor_status == status
    )
    return q.offset(skip).limit(limit).all()


def edit_accepted_job(db: Session, job_id: int, user_id: int, aj: AcceptedJobUpdate):
    db_aj = db.query(UserJobModel).get({"job_id": job_id, "user_id": user_id})
    db_aj.updated_at = datetime.datetime.now(datetime.timezone.utc)

    for var, value in vars(aj).items():
        if value:
            setattr(db_aj, var, value)

    db.add(db_aj)
    db.commit()
    return db_aj
