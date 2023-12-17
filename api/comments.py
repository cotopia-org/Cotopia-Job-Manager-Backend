from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.comments import edit_comment, get_comment_by_id, post_comment
from auth import get_current_active_user
from db.db_setup import get_db
from schemas.comment import Comment, CommentCreate, CommentUpdate
from schemas.user import User

router = fastapi.APIRouter()


@router.post("/comments", response_model=Comment, status_code=201)
async def add_comment(
    comment: CommentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return post_comment(db=db, comment=comment, author_id=current_user.id)


@router.put("/comments/{comment_id}", response_model=Comment, status_code=200)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found!")
    else:
        if db_comment.author_id == current_user.id:
            return edit_comment(db=db, comment_id=comment_id, comment=comment)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the author of this comment!"
            )


@router.delete("/comments/{comment_id}", status_code=204)
async def remove_comment(
    comment_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found!")
    else:
        if db_comment.author_id == current_user.id:
            comment = CommentUpdate(is_archived=True)
            edit_comment(db=db, comment_id=comment_id, comment=comment)
        else:
            raise HTTPException(
                status_code=403, detail="You are not the author of this comment!"
            )
