from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.DeviceTypeBase])
def get_sensor_type(db: Session = Depends(deps.get_db),
                    skip: int = 0,
                    limit: int = 10) -> Any:
    sensor_types = crud.device_type.get_multi(db,
                                              skip=skip,
                                              limit=limit)
    return sensor_types
