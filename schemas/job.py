from datetime import datetime

from pydantic import BaseModel

from ..db.models.job import JobStatus
from .comment import Comment
from .user import User


class JobBase(BaseModel):
    creator_id: int
    title: str
    workspace: str


class JobCreate(JobBase):
    description: str | None = None
    tags: list | None = None
    weights: dict | None = None
    deadline: datetime | None = None


class JobUpdate(JobCreate):
    title: str | None = None
    workspace: str | None = None
    description: str | None = None
    tags: list | None = None
    weights: dict | None = None
    deadline: datetime | None = None
    status: JobStatus | None = None
    is_archived: bool | None = None


class Job(JobUpdate):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    creator: User
    acceptors: list[User]
    comments: list[Comment]

    class Config:
        orm_mode = True
