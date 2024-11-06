from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Boolean)
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Staircase(Base):
    __tablename__ = "staircases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    address = Column(String)
    floors = Column(Integer)
    stair_height = Column(Integer)
    stairs_per_floor = Column(Integer)
    stairs_to_first = Column(Integer)
    have_elevator = Column(Boolean)
    owner_id = Column(Integer)


class StaircaseCreateVO(BaseModel):
    title: str
    address: str | None = None
    floors: int
    stair_height: int = 15
    stairs_per_floor: int = 18
    stairs_to_first: int = 5
    have_elevator: bool = True


class StaircaseVO(StaircaseCreateVO):
    id: int
    owner_id: int | None = None
