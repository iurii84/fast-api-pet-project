import json

from starlette.websockets import WebSocket
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps

from app.worker import compress_db

router = APIRouter()


@router.post("", response_model=schemas.MessageInDb)
async def send_message(msg: schemas.Message, db: Session = Depends(deps.get_db)) -> Any:
    message = crud.message.create(db, obj_in=msg)
    return message


@router.get("", response_model=List[schemas.MessageInDb])
async def get_messages(db: Session = Depends(deps.get_db),
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
async def compress_after_date_time(
        msg: schemas.MessageCompress
) -> Any:
    task = compress_db.delay(**msg.__dict__)
    # return task.get(timeout=20)
    return task.id


@router.websocket("/compress_after_date_time")
async def compress_after_date_time(
        websocket: WebSocket) -> Any:
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        task = compress_db.delay(**data)
        await websocket.send_json(task.get(timeout=20))

