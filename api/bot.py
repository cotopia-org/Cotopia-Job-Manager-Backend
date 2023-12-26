from typing import List

import fastapi
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from api.utils.bot import get_user_id
from api.utils.jobs import accept_job, create_job, get_accepted_jobs
from bot_auth import decode_token
from db.db_setup import get_db
from schemas.job import Job, JobCreate
from schemas.userjob import AcceptedJob

router = fastapi.APIRouter()


def read_token(token: str):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not logged in! Only valid bots can log in!",
        )
    else:
        try:
            decoded = decode_token(token)
        except:  # noqa: E722
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Your Token Is NOT ACCEPTABLE!",
            )

        if decoded is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token! Login Again!",
            )
        else:
            return decoded


@router.get("/bot", status_code=200)
async def bot_hello(request: Request):
    d = read_token(request.headers.get("Authorization"))
    return d


@router.post("/bot/job", response_model=Job, status_code=201)
async def submit_job_as_a_bot(
    job: JobCreate, request: Request, db: Session = Depends(get_db)
):
    bots_data = read_token(request.headers.get("Authorization"))
    user_id = get_user_id(db=db, bots_data=bots_data)
    return create_job(db=db, job=job, creator_id=user_id)


@router.post("/bot/accept/{job_id}", status_code=201)
async def accept(
    job_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    bots_data = read_token(request.headers.get("Authorization"))
    user_id = get_user_id(db=db, bots_data=bots_data)
    return accept_job(db=db, job_id=job_id, user_id=user_id)


@router.get("/bot/accepted_jobs/me", response_model=List[AcceptedJob])
async def get_accepts(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    bots_data = read_token(request.headers.get("Authorization"))
    user_id = get_user_id(db=db, bots_data=bots_data)
    accepts = get_accepted_jobs(db=db, user_id=user_id, skip=skip, limit=limit)
    return accepts
