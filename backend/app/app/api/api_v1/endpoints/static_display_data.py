from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.StaticDisplayData])
async def get_static_display_data(db: Session = Depends(deps.get_db),
                                  skip: int = 0,
                                  limit: int = 10) -> Any:
    static_display_data_entries = crud.static_display_data.get_multi(db,
                                                                     skip=skip,
                                                                     limit=limit)
    return static_display_data_entries


@router.post("")
async def post_static_display_data(*, msg: schemas.StaticDisplayDataRegister,
                                   db: Session = Depends(deps.get_db)) -> Any:
    static_display_data = crud.static_display_data.create(db=db, obj_in=msg)
    return static_display_data
