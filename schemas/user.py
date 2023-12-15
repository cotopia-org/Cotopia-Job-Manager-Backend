from datetime import datetime

from pydantic import BaseModel

from .job import Job


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    discord_user_id: int | None = None


class User(UserUpdate):
    id: int
    is_active: bool
    role: int
    created_at: datetime
    updated_at: datetime
    submitted_jobs: list[Job]
    accepted_jobs: list[Job]

    class Config:
        orm_mode = True
