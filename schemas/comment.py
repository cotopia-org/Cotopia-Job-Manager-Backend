from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    job_id: int
    body: str


class CommentCreate(CommentBase):
    ...


class CommentUpdate(CommentCreate):
    body: str | None = None
    is_archived: bool | None = None


class Comment(CommentUpdate):
    id: int
    author_id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
