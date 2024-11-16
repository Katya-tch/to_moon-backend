from datetime import date

from fastapi import (APIRouter,
                     HTTPException)

from app.domain.activities.models import *
from app.domain.staircases.models import Staircase
from app.domain.user.models import User
from app.core.db import db

router_activities = APIRouter(prefix='/activities', tags=['Activities'])


@router_activities.get('/{activity_id}')
async def read_activity(activity_id: int) -> ActivityCreateVO:
    _activity = db.get(Activity, activity_id)
    if not _activity:
        raise HTTPException(status_code=404, detail="Staicase not found")
    return _activity


@router_activities.post('/')
async def create_activity(activity: ActivityCreateVO) -> None:
    db.add(Activity(**activity.dict(), created_at=date.today()))
    db.commit()
    return None


@router_activities.put('/{activity_id}')
async def update_activity(activity_id: int,
                          activity: ActivityCreateVO) -> None:
    _activity = db.get(Activity, activity_id)
    if not _activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity_dict = activity.dict()
    for attr in activity_dict.keys():
        setattr(_activity, attr, activity_dict[attr])
    db.commit()
    return None


@router_activities.delete('/{activity_id}')
async def delete_activity(activity_id: int) -> None:
    _activity = db.get(Activity, activity_id)
    if not _activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(_activity)
    db.commit()
    return None


@router_activities.get('/all/{user_id}')
async def read_all_activities(user_id: int) -> list[ActivityReadVO]:
    activities = db.query(Activity).filter_by(user_id=user_id).filter_by(created_at=date.today())
    new_activities = []
    for activity in activities:
        new_activity = activity.__dict__
        if staircase_id := activity.staircase_id:
            staircase = db.get(Staircase, staircase_id)
            stair_height = staircase.stair_height
            stairs_per_floor = staircase.stairs_per_floor
            stairs_to_first = staircase.stairs_to_first
            new_activity['staircase_name'] = staircase.title
        else:
            stair_height = 15
            stairs_per_floor = 18
            stairs_to_first = 5
            new_activity['staircase_name'] = 'Параметры по умолчанию'

        new_activity['floor_end'], new_activity['floor_start'] = (
            max(new_activity['floor_end'], new_activity['floor_start']),
            min(new_activity['floor_end'], new_activity['floor_start']))

        user = db.get(User, activity.user_id)

        new_activity['height'] = (new_activity['floor_end'] - new_activity['floor_start']) * stairs_per_floor
        if new_activity['floor_start'] == 0:
            new_activity['height'] += stairs_to_first - stairs_per_floor
        new_activity['height'] *= stair_height / 100
        new_activity['height'] = round(new_activity['height'], 1)

        new_activity['calories'] = round(float(user.weight) * 9.8 * new_activity['height'] * 4 * 0.24 / 1000, 1)
        new_activities += [new_activity]

    return new_activities


@router_activities.get('/stat/{user_id}')
async def read_stat_activities(user_id: int) -> ActivityStatVO:
    activities = db.query(Activity).filter_by(user_id=user_id).filter_by(created_at=date.today())
    new_activities = []
    for activity in activities:
        new_activity = activity.__dict__
        if staircase_id := activity.staircase_id:
            staircase = db.get(Staircase, staircase_id)
            stair_height = staircase.stair_height
            stairs_per_floor = staircase.stairs_per_floor
            stairs_to_first = staircase.stairs_to_first
            new_activity['staircase_name'] = staircase.title
        else:
            stair_height = 15
            stairs_per_floor = 18
            stairs_to_first = 5
            new_activity['staircase_name'] = 'Параметры по умолчанию'

        new_activity['floor_end'], new_activity['floor_start'] = (
            max(new_activity['floor_end'], new_activity['floor_start']),
            min(new_activity['floor_end'], new_activity['floor_start']))

        user = db.get(User, activity.user_id)

        new_activity['height'] = (new_activity['floor_end'] - new_activity['floor_start']) * stairs_per_floor
        if new_activity['floor_start'] == 0:
            new_activity['height'] += stairs_to_first - stairs_per_floor
        new_activity['height'] *= stair_height / 100
        new_activity['height'] = round(new_activity['height'], 1)

        new_activity['calories'] = round(float(user.weight) * 9.8 * new_activity['height'] * 4 * 0.24 / 1000, 1)
        new_activities += [new_activity]

    height = 0.0
    calories = 0.0

    for act in new_activities:
        height += act['height']
        calories += act['calories']

    return ActivityStatVO(height=round(height, 1),
                          calories=round(calories, 1))
