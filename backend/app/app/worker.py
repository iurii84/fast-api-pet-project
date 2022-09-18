import json
import time

from fastapi import Depends
from raven import Client

from app import schemas, crud
from app.api import deps
from app.core.celery_app import app
from app.core.config import settings
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas import MessageCompress

client_sentry = Client(settings.SENTRY_DSN)


@app.task(acks_late=True)
def test_celery(word: str) -> str:
    time.sleep(30)
    return f"test2 task return {word}"


@app.task()
def add(a, b):
    time.sleep(5)
    return a+b


@app.task()
def compress_db(**kwargs):
    db = SessionLocal()

    payload = MessageCompress(**kwargs)
    result = crud.message.compress_data(db=db, obj_in=payload)
    db.close()
    return result



