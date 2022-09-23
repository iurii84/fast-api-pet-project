from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.DeviceDataBindBase])
async def get_device_data_binds(db: Session = Depends(deps.get_db),
                                skip: int = 0,
                                limit: int = 10) -> Any:
    device_data_binds = crud.device_data_bind.get_multi(db,
                                                        skip=skip,
                                                        limit=limit)
    return device_data_binds
