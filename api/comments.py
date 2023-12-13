import fastapi
from fastapi import Depends, HTTPException
from api.utils.comments import post_comment, edit_comment, delete_comment, get_comment_by_id
from schemas.comment import Comment, CommentCreate, CommentUpdate
from db.db_setup import get_db
from sqlalchemy.orm import Session



router = fastapi.APIRouter()

router.post("/comments", response_model=Comment, status_code=201)
async def add_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return post_comment(db=db, comment=comment)


router.post("/comments/{comment_id}", response_model=Comment, status_code=201)
async def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    db_comment = get_comment_by_id(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found!")
    else:
        return edit_comment(db=db, comment_id=comment_id, comment=comment)