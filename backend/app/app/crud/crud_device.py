from datetime import datetime

from fastapi import HTTPException
from typing import List

from sqlalchemy import func, distinct
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Device, Message, DeviceType


class CRUDDevice(CRUDBase[Device, Device, Device]):

    def get_multi(
            self, db: Session, *,
            skip: int = 0,
            limit: int = 10,
            is_display: bool = False
    ) -> List[Device]:
        res = None
        if is_display:
            res = db.query(Device.id,
                           Device.uuid,
                           Device.location,
                           Device.date_registered,
                           Device.name,
                           Device.type,
                           Device.first_occurrence,
                           DeviceType.screen_type,
                           DeviceType.json).join(DeviceType, Device.type == DeviceType.type_id).\
                filter(DeviceType.screen_type.is_not(None)).offset(skip).limit(limit).all()
        else:
            res = db.query(self.model).offset(skip).limit(limit).all()
        return res

    def get_unregistered_devices(self, db: Session) -> List[Device]:
        sub_query = db.query(Device.uuid).subquery()
        res = db.query(
            distinct(Message.uuid).label("uuid"),
            func.min(Message.created).label("first_occurrence"),
            Message.type.label("type")). \
            filter(Message.uuid.notin_(sub_query)). \
            group_by(Message.uuid, Message.type).all()
        # SELECT distinct uuid, min(created) as first_occurence, "type" FROM public.message
        # where uuid  not in (Select  uuid from public.device)
        # group by uuid, type
        return res

    def register_device(self, db: Session, msg: Device) -> Device:
        registered_devices = db.query(Device.uuid).all()
        registered_devices_uuid_list = []

        unregistered_devices = db.query(distinct(Message.uuid).label("uuid")).all()
        unregistered_devices_uuid_list = []

        for reg_device in registered_devices:
            registered_devices_uuid_list.append(reg_device['uuid'])

        for unreg_device in unregistered_devices:
            unregistered_devices_uuid_list.append(unreg_device['uuid'])

        if msg.uuid in registered_devices_uuid_list:
            raise HTTPException(status_code=400, detail="Device already registered")
        elif msg.uuid not in unregistered_devices_uuid_list:
            raise HTTPException(status_code=400, detail="Not existing device. Check if connected")

        else:
            device_data_from_msg = db.query(Message) \
                .filter(Message.uuid == msg.uuid) \
                .order_by(Message.created) \
                .limit(1) \
                .all()[0]

            db_obj = Device(uuid=msg.uuid,
                            name=msg.name,
                            location=msg.location,
                            type=device_data_from_msg.type,
                            first_occurrence=device_data_from_msg.created,
                            date_registered=datetime.now())

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj


device = CRUDDevice(Device)
