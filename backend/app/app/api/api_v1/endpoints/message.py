import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("", response_model=schemas.MessageInDb)
def send_message(msg: schemas.Message, db: Session = Depends(deps.get_db)) -> Any:
    try:
        uuid.UUID(msg.uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong uuid")

    message = crud.message.create(db, obj_in=msg)
    print(msg)
    return message
