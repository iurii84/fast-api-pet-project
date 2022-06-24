import uuid
from fastapi import APIRouter, HTTPException

from app import schemas

router = APIRouter()


@router.post("", response_model=schemas.Message)
def send_message(msg: schemas.Message):
    try:
        uuid.UUID(msg.uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Wrong uuid")
    print(msg)
    return msg
