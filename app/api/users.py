from fastapi import (APIRouter,
                     HTTPException)

from app.domain.user.models import *
from app.core.db import db

router_users = APIRouter(prefix='/users', tags=['Users'])


@router_users.get('/{user_id}')
async def read_user(user_id: int) -> UserVO:
    _user = db.get(User, user_id)
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user


@router_users.post('/')
async def create_user(user: UserInfoVO) -> None:
    db.add(User(**user.dict()))
    db.commit()
    return None


@router_users.put('/{user_id}')
async def update_user(user_id: int,
                      user: UserInfoVO) -> None:
    _user = db.get(User, user_id)
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.dict()
    for attr in user_dict.keys():
        setattr(_user, attr, user_dict[attr])
    db.commit()
    return None


@router_users.put('/{user_id}/phys')
async def update_user_phys(user_id: int,
                           user: UserPhysVO) -> None:
    _user = db.get(User, user_id)
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = user.dict()
    for attr in user_dict.keys():
        setattr(_user, attr, user_dict[attr])
    db.commit()
    return None


@router_users.delete('/{user_id}')
async def delete_user(user_id: int) -> None:
    _user = db.get(User, user_id)
    if not _user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(_user)
    db.commit()
    return None


@router_users.get('/')
async def read_all_users() -> list[UserVO]:
    users = db.query(User).all()
    return users
