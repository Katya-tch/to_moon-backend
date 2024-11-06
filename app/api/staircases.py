from fastapi import (APIRouter,
                     HTTPException)

from app.domain.staircases.models import *
from app.core.db import db

router_staircases = APIRouter(prefix='/staircases', tags=['Staircases'])


@router_staircases.get('/{staircase_id}')
async def read_staircase(staircase_id: int) -> StaircaseVO:
    _staircase = db.get(Staircase, staircase_id)
    if not _staircase:
        raise HTTPException(status_code=404, detail="Staicase not found")
    return _staircase


@router_staircases.post('/')
async def create_staircase(staircase: StaircaseCreateVO) -> None:
    db.add(Staircase(**staircase.dict()))
    db.commit()
    return None


@router_staircases.put('/{staircase_id}')
async def update_staircase(staircase_id: int,
                           staircase: StaircaseCreateVO) -> None:
    _staircase = db.get(Staircase, staircase_id)
    if not _staircase:
        raise HTTPException(status_code=404, detail="Staircase not found")
    staircase_dict = staircase.dict()
    for attr in staircase_dict.keys():
        setattr(_staircase, attr, staircase_dict[attr])
    db.commit()
    return None


@router_staircases.delete('/{staircase_id}')
async def delete_staircase(staircase_id: int) -> None:
    _staircase = db.get(Staircase, staircase_id)
    if not _staircase:
        raise HTTPException(status_code=404, detail="Staircase not found")
    db.delete(_staircase)
    db.commit()
    return None


@router_staircases.get('/')
async def read_all_staircases():
    staircases = db.query(Staircase).all()
    return staircases
