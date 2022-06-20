from fastapi import APIRouter

from app import schemas

router = APIRouter()


@router.post("", response_model=schemas.Message)
def send_message(msg: schemas.Message):
    print(msg)
    return msg
