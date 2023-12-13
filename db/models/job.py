import enum as pyEnum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class JobStatus(pyEnum):
    todo = "todo"
    doing = "doing"
    done = "done"


class Job(Timestamp, Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    workspace = Column(String(63), nullable=False)
    title = Column(String(127), nullable=False)
    description = Column(String(511), nullable=True)
    tags = Column(JSON, nullable=True)
    weights = Column(JSON, nullable=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(JobStatus), nullable=False, default="todo")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    creator = relationship("User", back_populates="submitted_jobs")
    acceptor_users = relationship(
        "User", secondary="users_jobs", back_populates="accepted_jobs"
    )
    # comments


class UserJob(Timestamp, Base):
    __tablename__ = "users_jobs"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True)
