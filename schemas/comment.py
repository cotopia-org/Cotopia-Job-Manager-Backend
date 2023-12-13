from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    author_id: int
    job_id: int
    body: str

class CommentCreate(CommentBase):
    ...


class CommentUpdate(CommentCreate):
    body: str
    is_archived: bool | None = None


class Comment(CommentUpdate):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
