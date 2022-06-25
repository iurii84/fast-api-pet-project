from datetime import datetime
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import Message


class CRUDMessage(CRUDBase[Message, Message, Message]):
    def create(self, db: Session, *, obj_in: Message) -> Message:
        db_obj = Message(
            uuid=obj_in.uuid,
            temp=obj_in.temp,
            hum=obj_in.hum,
            created=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


message = CRUDMessage(Message)
