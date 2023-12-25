from pydantic import BaseModel

from db.models.job import JobStatus


class AcceptedJobBase(BaseModel):
    user_id: int
    job_id: int


class AcceptedJob(AcceptedJobBase):
    acceptor_status: JobStatus


class AcceptedJobUpdate(BaseModel):
    acceptor_status: JobStatus
