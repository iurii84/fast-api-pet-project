from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Device])
async def get_devices(db: Session = Depends(deps.get_db),
                      skip: int = 0,
                      limit: int = 10,
                      is_display: bool = False) -> Any:
    devices = crud.device.get_multi(db,
                                    skip=skip,
                                    limit=limit,
                                    is_display=is_display)
    return devices


@router.get("/get_unregistered", response_model=List[schemas.DeviceToRegister])
async def get_unregistered_devices(db: Session = Depends(deps.get_db)) -> Any:
    devices = crud.device.get_unregistered_devices(db)
    return devices


@router.get("/get_params_by_uuid/{device_uuid}")
async def get_params_by_uuid(device_uuid: str,
                             db: Session = Depends(deps.get_db)) -> Any:
    params = crud.device.get_params_by_uuid(db=db, device_uuid=device_uuid)
    return params


@router.post("/register")
async def register_device(*, msg: schemas.RegisterDevice, db: Session = Depends(deps.get_db)) -> Any:
    device = crud.device.register_device(db, msg=msg)
    return device


@router.patch("/{id}", response_model=schemas.Device)
async def patch_device(
        *,
        msg: schemas.PatchDevice,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Partial update device.
    """
    existing_device = crud.device.get(db=db, id=id)
    if not existing_device:
        raise HTTPException(status_code=404, detail="Item not found")

    device_updated = crud.device.update(db=db, db_obj=existing_device, obj_in=msg)
    return device_updated


@router.delete("/{id}", response_model=schemas.DeleteDeviceReturn)
def delete_device(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
) -> Any:
    """
    Delete device.
    """
    device = crud.device.get(db=db, id=id)
    if not device:
        raise HTTPException(status_code=404, detail="Item not found")

    device = crud.device.remove(db=db, id=id)
    return device
