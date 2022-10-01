from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

import json

from app.core.data_bind_subscribers_nitifier import notify_subscribers
from app.crud.base import CRUDBase
from app.db.redis_connection import redis_connection
from app.models import Message


class CRUDMessage(CRUDBase[Message, Message, Message]):
    def create(self, db: Session, *, obj_in: Message) -> Message:
        obj_dict = obj_in.__dict__
        db_obj = Message(
            **obj_dict,
            created=datetime.now()

        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        uuid = str(obj_in.uuid)

        # get value from redis
        try:
            res = json.loads(redis_connection.get(uuid))
            for item in res:
                if obj_dict[item] != res[item]:
                    notify_subscribers(uuid=uuid, device_prop=item, new_value=res[item])
        except TypeError:
            print("Data is not found in Redis")

        # update value in redis
        obj_dict.pop("uuid")
        redis_connection.set(uuid, json.dumps(obj_dict))

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
                    return db.query(self.model).where(self.model.created > date_time_result).order_by(Message.id). \
                        offset(skip).limit(limit).all()
            message_id = db.query(func.max(self.model.id)).first()[0] - 1000

            return db.query(self.model).where(self.model.id > message_id).order_by(Message.id).offset(skip).limit(
                limit).all()
        else:
            db.query(self.model).offset(skip).limit(limit).all()

    def compress_data(self,
                      db: Session,
                      obj_in):
        db_date_time_delta = db.query(self.model). \
            where((and_(self.model.created > obj_in.start_date_time,
                        self.model.created < obj_in.end_date_time,
                        self.model.uuid == obj_in.uuid,
                        self.model.compress_ratio == obj_in.for_items_with_compress_ratio))).all()
        items_found = len(db_date_time_delta)
        items_selected_to_compress = None

        even = None
        if items_found % 2 == 0:
            even = True
        else:
            even = False

        if even:
            items_selected_to_compress = items_found
        else:
            db_date_time_delta.pop()
            items_selected_to_compress = len(db_date_time_delta)

        buff = []
        avg_temp = 0
        avg_hum = 0
        avg_time = None
        for i in db_date_time_delta:
            buff.append(i)
            if len(buff) == 2:
                avg_temp = (buff[0].temp + buff[1].temp) / 2
                avg_hum = (buff[0].hum + buff[1].hum) / 2
                delta_time = buff[1].created - buff[0].created
                avg_time = buff[0].created + delta_time / 2

                msg_1_id = buff[0].id
                msg_2_id = buff[1].id

                db_update = db.query(self.model). \
                    filter(Message.id == msg_2_id).\
                    update({'temp': avg_temp,
                            'hum': avg_hum,
                            'created': avg_time,
                            'compress_ratio': Message.compress_ratio + 1})

                db_delete = db.query(self.model).\
                    filter(Message.id == msg_1_id).\
                    delete()
                db.commit()

                print(f"AVG_TEMP: {avg_temp} ---- AVG_HUM: {avg_hum} ---- AVG_TIME: {avg_time}")

                buff.clear()
                avg_temp = 0
                avg_hum = 0
                avg_time = None

        return {"items_found": items_found,
                "is_even": even,
                "items_selected_to_compress": items_selected_to_compress,
                "db_update": None,
                "db_delete": None}


message = CRUDMessage(Message)
