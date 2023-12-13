from datetime import datetime

from sqlalchemy.orm import Session

from db.models.comment import Comment as CommentModel
from schemas.comment import CommentCreate, CommentUpdate


def post_comment(db: Session, comment: CommentCreate):
    db_comment = CommentModel(
        author_id=comment.author_id, job_id=comment.job_id, body=comment.body
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment_by_id(db: Session, comment_id: int):
    return db.query(CommentModel).filter(CommentModel.id == comment_id).first()


def edit_comment(db: Session, comment_id: int, comment: CommentUpdate):
    db_comment = db.query(CommentModel).get(comment_id)
    db_comment.updated_at = datetime.now(datetime.timezone.utc)

    for var, value in vars(comment).items():
        if value:
            setattr(db_comment, var, value)

    db.add(db_comment)
    db.commit()
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(CommentModel).get(comment_id)
    db_comment.updated_at = datetime.now(datetime.timezone.utc)
    db_comment.is_archived = True

    db.add(db_comment)
    db.commit()
    return db_comment
