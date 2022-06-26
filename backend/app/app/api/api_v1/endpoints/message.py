from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("", response_model=schemas.MessageInDb)
def send_message(msg: schemas.Message, db: Session = Depends(deps.get_db)) -> Any:
    message = crud.message.create(db, obj_in=msg)
    print(msg)
    return message
