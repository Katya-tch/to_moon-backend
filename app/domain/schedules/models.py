from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column,
                        Integer,
                        Boolean)
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    time_hours = Column(Integer)
    time_minutes = Column(Integer)
    mon = Column(Boolean)
    tue = Column(Boolean)
    wed = Column(Boolean)
    thu = Column(Boolean)
    fri = Column(Boolean)
    sat = Column(Boolean)
    sun = Column(Boolean)
    staircase_id = Column(Integer)


class ScheduleCreateVO(BaseModel):
    time_hours: int
    time_minutes: int
    mon: bool | None = False
    tue: bool | None = False
    wed: bool | None = False
    thu: bool | None = False
    fri: bool | None = False
    sat: bool = False
    sun: bool = False
    staircase_id: int


class ScheduleReadVO(BaseModel):
    id: int
    time: str
    weekdays: str
