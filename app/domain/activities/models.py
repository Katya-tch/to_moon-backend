from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column,
                        Integer,
                        Date)
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    staircase_id = Column(Integer)
    floor_start = Column(Integer)
    floor_end = Column(Integer)
    user_id = Column(Integer)
    created_at = Column(Date)


class ActivityCreateVO(BaseModel):
    staircase_id: int | None = None
    floor_start: int
    floor_end: int
    user_id: int | None = 1


class ActivityReadVO(BaseModel):
    id: int
    staircase_name: str
    floor_start: int
    floor_end: int
    height: float
    calories: float


class ActivityStatVO(BaseModel):
    height: float
    calories: float
