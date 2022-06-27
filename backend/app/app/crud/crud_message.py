from datetime import datetime
from typing import List

from sqlalchemy.orm import Session

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

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, order_by: str = "id"
    ) -> List[Message]:
        if order_by == 'id':
            return db.query(self.model).order_by(Message.id).offset(skip).limit(limit).all()
        else:
            db.query(self.model).offset(skip).limit(limit).all()


message = CRUDMessage(Message)
