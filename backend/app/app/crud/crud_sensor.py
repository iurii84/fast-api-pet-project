from datetime import datetime, timedelta

from fastapi import HTTPException
from typing import List

from sqlalchemy import func, and_, distinct, subquery, select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Sensor,  Message


class CRUDSensor(CRUDBase[Sensor, Sensor, Sensor]):

    def get_multi(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 10
    ) -> List[Sensor]:
        res = db.query(self.model).offset(skip).limit(limit).all()
        return res

    def get_unregistered_sensors(self, db: Session) -> List[Sensor]:
        sub_query = db.query(Sensor.uuid).subquery()
        res = db.query(
            distinct(Message.uuid).label("uuid"),
            func.min(Message.created).label("first_occurrence"),
            Message.type.label("type")). \
            filter(Message.uuid.notin_(sub_query)). \
            group_by(Message.uuid, Message.type).all()
        # SELECT distinct uuid, min(created) as first_occurence, "type" FROM public.message
        # where uuid  not in (Select  uuid from public.sensor)
        # group by uuid, type
        return res

    def register_sensor(self, db: Session, msg: Sensor) -> Sensor:
        registered_sensors = db.query(Sensor.uuid).all()
        registered_sensor_uuid_list = []

        unregistered_sensors = db.query(distinct(Message.uuid).label("uuid")).all()
        unregistered_sensor_uuid_list = []

        for reg_sens in registered_sensors:
            registered_sensor_uuid_list.append(reg_sens['uuid'])

        for unreg_sens in unregistered_sensors:
            unregistered_sensor_uuid_list.append(unreg_sens['uuid'])

        if msg.uuid in registered_sensor_uuid_list:
            raise HTTPException(status_code=400, detail="Sensor already registered")
        elif msg.uuid not in unregistered_sensor_uuid_list:
            raise HTTPException(status_code=400, detail="Not existing sensor. Check if connected")

        else:
            sensor_data_from_msg = db.query(Message) \
                .filter(Message.uuid == msg.uuid) \
                .order_by(Message.created) \
                .limit(1) \
                .all()[0]

            db_obj = Sensor(uuid=msg.uuid,
                            name=msg.name,
                            location=msg.location,
                            type=sensor_data_from_msg.type,
                            first_occurrence=sensor_data_from_msg.created,
                            date_registered=datetime.now())

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj


sensor = CRUDSensor(Sensor)
