import enum as pyEnum

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String

from ..db_setup import Base
from .mixins import Timestamp


class JobStatus(pyEnum.IntEnum):
    todo = 1
    doing = 2
    done = 3


class Job(Timestamp, Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    workspace = Column(String(63), nullable=False)
    title = Column(String(127), nullable=False)
    description = Column(String(511), nullable=True)
    tags = Column(JSON, nullable=True)
    weights = Column(JSON, nullable=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(Enum(JobStatus), nullable=False)
    creator = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    # acceptors
    # comments
