import enum as pyEnum

from sqlalchemy import BigInteger, Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import Timestamp


class Role(pyEnum.IntEnum):
    default = 1


class User(Timestamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(511))
    role = Column(Enum(Role))
    is_active = Column(Boolean, default=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    discord_user_id = Column(BigInteger, nullable=True)
    submitted_jobs = relationship("Job", back_populates="creator")
    accepted_jobs = relationship(
        "Job", secondary="users_jobs", back_populates="acceptor_users"
    )
