from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func, and_, distinct, subquery, select
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Sensor, SensorToRegister, Message


class CRUDSensor(CRUDBase[Sensor, Sensor, Sensor]):

    def get_multi(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 10
    ) -> List[Sensor]:
        res = db.query(self.model).offset(skip).limit(limit).all()
        return res

    def get_unregistered_sensors(self, db: Session) -> List[SensorToRegister]:
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


sensor = CRUDSensor(Sensor)
