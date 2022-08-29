from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.crud.crud_message import CRUDMessage
from app.models import Message

router = APIRouter()


@router.get("", response_model=List[schemas.SensorLocationBase])
def get_sensor_locations(db: Session = Depends(deps.get_db),
                         skip: int = 0,
                         limit: int = 10) -> Any:
    sensors = crud.sensor_location.get_multi(db,
                                             skip=skip,
                                             limit=limit)
    return sensors


message = CRUDMessage(Message)