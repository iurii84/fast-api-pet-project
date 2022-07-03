from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func
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
            self, db: Session, *,
            skip: int = 0,
            limit: int = 300000,
            order_by: str = "id",
            after_id: int = 0,
            lastMinutes: int = 0
    ) -> List[Message]:
        if order_by == 'id':
            if after_id > 0:
                return db.query(self.model).where(self.model.id > after_id).order_by(Message.id).offset(skip). \
                    limit(limit).all()
            else:
                if lastMinutes > 0:
                    date_time_now = datetime.now()
                    date_time_result = date_time_now - timedelta(minutes=lastMinutes)
                    return db.query(self.model).where(self.model.created > date_time_result).order_by(Message.id).\
                        offset(skip).limit(limit).all()
            message_id = db.query(func.max(self.model.id)).first()[0] - 1000

            return db.query(self.model).where(self.model.id > message_id).order_by(Message.id).offset(skip).limit(limit).all()
        else:
            db.query(self.model).offset(skip).limit(limit).all()


message = CRUDMessage(Message)
