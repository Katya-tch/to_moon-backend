from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Numeric)
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    height = Column(Integer)
    weight = Column(Numeric)
    image_path = Column(String)


class UserInfoVO(BaseModel):
    username: str
    email: str
    image_path: str | None = None


class UserPhysVO(BaseModel):
    weight: float | None = None
    height: int | None = None


class UserVO(UserInfoVO, UserPhysVO):
    id: int
