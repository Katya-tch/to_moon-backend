from fastapi import (APIRouter,
                     HTTPException)

from app.domain.schedules.models import *
from app.core.db import db

router_schedules = APIRouter(prefix='/schedules', tags=['Schedules'])
days_transl = {
    'mon': 'ПН',
    'tue': 'ВТ',
    'wed': 'СР',
    'thu': 'ЧТ',
    'fri': 'ПТ',
    'sat': 'СБ',
    'sun': 'ВС',
}


@router_schedules.get('/{schedule_id}')
async def read_schedule(schedule_id: int) -> ScheduleCreateVO:
    _schedule = db.get(Schedule, schedule_id)
    if not _schedule:
        raise HTTPException(status_code=404, detail="Staicase not found")
    return _schedule


@router_schedules.post('/')
async def create_schedule(schedule: ScheduleCreateVO) -> None:
    db.add(Schedule(**schedule.dict()))
    db.commit()
    return None


@router_schedules.put('/{schedule_id}')
async def update_schedule(schedule_id: int,
                          schedule: ScheduleCreateVO) -> None:
    _schedule = db.get(Schedule, schedule_id)
    if not _schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule_dict = schedule.dict()
    for attr in schedule_dict.keys():
        setattr(_schedule, attr, schedule_dict[attr])
    db.commit()
    return None


@router_schedules.delete('/{schedule_id}')
async def delete_schedule(schedule_id: int) -> None:
    _schedule = db.get(Schedule, schedule_id)
    if not _schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    db.delete(_schedule)
    db.commit()
    return None


@router_schedules.get('/all/{staircase_id}')
async def read_all_schedules(staircase_id: int) -> list[ScheduleReadVO]:
    schedules = db.query(Schedule).filter_by(staircase_id=staircase_id)
    new_schedules = []
    for schedule in schedules:
        new_schedule = schedule.__dict__
        new_schedule['weekdays'] = ' '.join([days_transl[_] for _ in days_transl.keys() if new_schedule.pop(_, False)])
        new_schedule['time'] = (f'{str(new_schedule.pop("time_hours")).rjust(2, "0")}:'
                                f'{str(new_schedule.pop("time_minutes")).rjust(2, "0")}')
        new_schedules += [new_schedule]
    return new_schedules
