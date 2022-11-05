from pydantic import UUID4
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.schemas import DeviceDataBindBase

router = APIRouter()


@router.get("", response_model=List[schemas.DeviceDataBindBase])
async def get_device_data_binds(db: Session = Depends(deps.get_db),
                                subscriber_uuid=None,
                                skip: int = 0,
                                limit: int = 10) -> Any:
    device_data_binds = crud.device_data_bind.get_multi(db,
                                                        skip=skip,
                                                        limit=limit,
                                                        subscriber_uuid=subscriber_uuid)
    return device_data_binds


@router.get("/subscribers")
async def get_device_data_bind_subscribers(uuid: UUID4,
                                           device_prop: str) -> Any:
    device_data_bind_subscribers = crud.device_data_bind.get_subscribers(uuid=uuid,
                                                                         device_prop=device_prop)
    return device_data_bind_subscribers


@router.post("")
async def post_device_data_bind(*, msg: schemas.RegisterDeviceDataBind, db: Session = Depends(deps.get_db)) -> Any:
    device_data_bind = crud.device_data_bind.create(db=db, obj_in=msg)
    return device_data_bind


@router.patch("/{binder_id}", response_model=DeviceDataBindBase)
async def patch_device_data_bind(
        *,
        msg: schemas.PatchDeviceDataBind,
        db: Session = Depends(deps.get_db),
        binder_id: int,
) -> Any:
    """
    Partial update device.
    """
    existing_device_data_binder = crud.device_data_bind.get(db=db, id=binder_id)
    if not existing_device_data_binder:
        raise HTTPException(status_code=404, detail="Binder not found")

    device_data_binder_updated = crud.device_data_bind.update(db=db, db_obj=existing_device_data_binder, obj_in=msg)
    return device_data_binder_updated


@router.delete("/{binder_id}", response_model=schemas.DeleteDeviceReturn)
def delete_device_data_bind(
        *,
        db: Session = Depends(deps.get_db),
        binder_id: int,
) -> Any:
    """
    Delete device.
    """
    binder = crud.device_data_bind.get(db=db, id=binder_id)
    if not binder:
        raise HTTPException(status_code=404, detail="Binder not found")

    binder = crud.device_data_bind.remove(db=db, id=binder_id)
    return binder
