from pydantic import BaseModel

from db.models.job import JobStatus

from .job import MinimalJob
from .user import MinimalUser


class AcceptedJobBase(BaseModel):
    user_id: int
    job_id: int


class AcceptedJob(AcceptedJobBase):
    acceptor_status: JobStatus
    job: MinimalJob
    user: MinimalUser


class AcceptedJobUpdate(BaseModel):
    acceptor_status: JobStatus
