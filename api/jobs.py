from typing import Annotated, List

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.jobs import (
    accept_job,
    create_job,
    decline_job,
    edit_job,
    get_all_jobs,
    get_job_by_id,
)
from auth import get_current_active_user
from db.db_setup import get_db
from schemas.job import Job, JobCreate, JobUpdate
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/jobs", response_model=Job, status_code=201)
async def submit_job(job: JobCreate, db: Session = Depends(get_db)):
    return create_job(db=db, job=job)


@router.get("/jobs/{job_id}", response_model=Job)
async def get_a_job(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_job = get_job_by_id(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found!")
    return db_job


@router.get("/jobs", response_model=List[Job])
async def get_jobs(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    jobs = get_all_jobs(db=db, skip=skip, limit=limit)
    return jobs


@router.put("/jobs/{job_id}", response_model=Job, status_code=200)
async def update_job(
    job_id: int,
    job: JobUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_job = get_job_by_id(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found!")
    else:
        if db_job.id == current_user.id:
            return edit_job(db=db, job_id=job_id, job=job)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the creator of this job!"
            )


@router.delete("/jobs/{job_id}", status_code=204)
async def remove_job(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_job = get_job_by_id(db=db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found!")
    else:
        if db_job.id == current_user.id:
            job = JobUpdate(is_archived=True)
            edit_job(db=db, comment_id=job_id, job=job)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the creator of this job!"
            )


@router.post("/jobs/accept/{job_id}", status_code=201)
async def accept(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return accept_job(db=db, job_id=job_id, user_id=current_user.id)


@router.delete("/jobs/decline/{job_id}", status_code=204)
async def decline(
    job_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    decline_job(db=db, job_id=job_id, user_id=current_user.id)
