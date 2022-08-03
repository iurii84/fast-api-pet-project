from datetime import datetime, timedelta
from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Sensor


class CRUDSensor(CRUDBase[Sensor, Sensor, Sensor]):

    def get_multi(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 10
    ) -> List[Sensor]:
        res = db.query(self.model).offset(skip).limit(limit).all()
        print(res)
        return res


sensor = CRUDSensor(Sensor)
