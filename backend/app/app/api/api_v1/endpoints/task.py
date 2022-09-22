from celery.result import AsyncResult
from typing import Any
from fastapi import APIRouter, HTTPException
from app.core.celery_app import app

router = APIRouter()


@router.get("")
async def get_task_by_id(task_id: str) -> Any:
    task = AsyncResult(task_id, app=app)
    if task.state == "SUCCESS":
        return {"task_state": task.state,
                "task": task.get(),
                "task_message": "Task finished successful"}
    elif task.state == "PENDING":
        return {"task_state": task.state,
                "task": None,
                "task_message": "Task not exists or not started yet"}
    elif task.state == "STARTED":
        return {"task_state": task.state,
                "task": None,
                "task_message": "Task is started successful. Wait and call to update"}
