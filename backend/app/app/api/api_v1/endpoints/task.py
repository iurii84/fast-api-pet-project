from celery.result import AsyncResult
from typing import Any
from fastapi import APIRouter
from app.core.celery_app import app

router = APIRouter()


@router.get("/get_state")
async def get_task_state_by_id(task_id: str) -> Any:
    task = AsyncResult(task_id, app=app)
    return task.state


@router.get("/get_result")
async def get_task_state_by_id(task_id: str) -> Any:
    task = AsyncResult(task_id, app=app)
    return task.get()