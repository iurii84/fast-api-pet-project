from typing import Any
from fastapi import FastAPI, WebSocket

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app import models, schemas
from app.api import deps

from app.utils import send_test_email
from app.worker import add

router = APIRouter()


@router.post("/test-celery/", status_code=201)
def test_celery(
        msg: schemas.Msg,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    res = add.delay(2, 2)
    return {"msg": res.get(timeout=7)}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
        email_to: EmailStr,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        res = add.delay(2, 2)
        await websocket.send_text(f"msg: {res.get(timeout=7)}")
