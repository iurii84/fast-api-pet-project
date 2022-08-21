import datetime
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("", response_model=schemas.MessageInDb)
def send_message(msg: schemas.Message, db: Session = Depends(deps.get_db)) -> Any:
    message = crud.message.create(db, obj_in=msg)
    return message


@router.get("", response_model=List[schemas.MessageInDb])
def get_messages(db: Session = Depends(deps.get_db),
                 skip: int = 0,
                 limit: int = 300000,
                 order_by: str = 'id',
                 after_id: int = 0,
                 lastMinutes: int = 0) -> Any:
    messages = crud.message.get_multi(db,
                                      skip=skip,
                                      limit=limit,
                                      order_by=order_by,
                                      after_id=after_id,
                                      lastMinutes=lastMinutes)
    return messages


@router.post("/compress_after_date_time")
def compress_after_date_time(
        msg: schemas.MessageCompress,
        db: Session = Depends(deps.get_db)
) -> Any:
    result = crud.message.compress_data(obj_in=msg, db=db)
    return result
