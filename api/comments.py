import fastapi
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from api.utils.comments import edit_comment, get_comment_by_id, post_comment
from db.db_setup import get_db
from schemas.comment import Comment, CommentCreate, CommentUpdate

router = fastapi.APIRouter()


@router.post("/comments", response_model=Comment, status_code=201)
async def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return post_comment(db=db, comment=comment)


@router.put("/comments/{comment_id}", response_model=Comment, status_code=200)
async def update_comment(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)
):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found!")
    else:
        return edit_comment(db=db, comment_id=comment_id, comment=comment)


@router.delete("/comments/{comment_id}", status_code=204)
async def remove_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found!")
    else:
        comment = CommentUpdate(is_archived=True)
        edit_comment(db=db, comment_id=comment_id, comment=comment)
