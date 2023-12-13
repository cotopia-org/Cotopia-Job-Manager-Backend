from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship


from ..db_setup import Base
from .mixins import Timestamp


class Comment(Timestamp, Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    job = relationship("Job", back_populates="comments")
    body = Column(Text, nullable=False)
    is_archived = Column(Boolean, default=False)

