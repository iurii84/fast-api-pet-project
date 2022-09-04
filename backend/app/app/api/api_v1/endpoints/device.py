from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Device])
def get_devices(db: Session = Depends(deps.get_db),
                skip: int = 0,
                limit: int = 10) -> Any:
    devices = crud.device.get_multi(db,
                                    skip=skip,
                                    limit=limit)
    return devices


@router.get("/get_unregistered", response_model=List[schemas.DeviceToRegister])
def get_unregistered_devices(db: Session = Depends(deps.get_db)) -> Any:
    devices = crud.device.get_unregistered_devices(db)
    return devices


@router.post("/register")
def register_device(*, msg: schemas.RegisterDevice, db: Session = Depends(deps.get_db)) -> Any:
    device = crud.device.register_device(db, msg=msg)
    return device
