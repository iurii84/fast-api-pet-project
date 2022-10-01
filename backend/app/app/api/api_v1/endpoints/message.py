import json
import time
import asyncio

from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.core.WebSocketConnectionManager import WebSocketConnectionManager
from app.db.redis_connection import redis_connection

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


@router.post("/compress")
async def task_compress_device_messages(
        msg: schemas.MessageCompress
) -> Any:
    """This endpoint is used to compress db records for the given device in the indicated time ranges
    From 2 record it creates 1 record with the average values for time and all the sensors values, like temp,
    hum...
    Each time is finished - it increments 'compress_ratio' with 1"""
    task = compress_db.delay(**msg.__dict__)

    return {"task_id": task.id}


ws_manager = WebSocketConnectionManager()


# arr = []
# thread = p.run_in_thread(sleep_time=0.001)
# thread.


@router.websocket("/compress/{client_id}")
async def compress_after_date_time(
        websocket: WebSocket, client_id: str) -> Any:
    pubsub = await ws_manager.connect(websocket, client_id)

    try:
        while True:
            # data = await websocket.receive_text()
            message = pubsub.get_message()
            if message:
                await ws_manager.send_personal_message(str(message['data']), websocket)

            await asyncio.sleep(0.002)

            # await ws_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, pubsub, client_id)
        await ws_manager.broadcast(f"Client #{client_id} left the chat")





@router.get("/test/{msg}")
async def task_compress_device_messages(
        msg
):
    r = redis_connection
    r.publish('a613d4aa-3d03-42ac-955a-cd39ea14b214', msg)
