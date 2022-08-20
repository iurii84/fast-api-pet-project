import datetime
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Sensor])
def get_sensors(db: Session = Depends(deps.get_db),
                skip: int = 0,
                limit: int = 10) -> Any:
    sensors = crud.sensor.get_multi(db,
                                    skip=skip,
                                    limit=limit)
    return sensors


@router.get("/get_unregistered", response_model=List[schemas.SensorToRegister])
def get_unregistered_sensors(db: Session = Depends(deps.get_db)) -> Any:
    sensors = crud.sensor.get_unregistered_sensors(db)
    return sensors
