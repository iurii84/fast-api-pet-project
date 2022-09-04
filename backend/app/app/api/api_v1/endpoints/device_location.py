from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.DeviceLocationBase])
def get_sensor_locations(db: Session = Depends(deps.get_db),
                         skip: int = 0,
                         limit: int = 10) -> Any:
    sensor_locations = crud.device_location.get_multi(db,
                                                      skip=skip,
                                                      limit=limit)
    return sensor_locations
