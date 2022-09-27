from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy import and_
from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.session import SessionLocal
from app.models import DeviceDataBind

from app.db.redis_cache import cache
from app.schemas import RegisterDeviceDataBind, PatchDeviceDataBind


@cache.cache()
def cacheable_get_data_binders(skip: int, limit: int):
    db = SessionLocal()

    res = db.query(DeviceDataBind).offset(skip).limit(limit).all()

    db.close()
    return jsonable_encoder(res)


@cache.cache()
def cacheable_get_subscribers(uuid: str, device_prop: str):
    db = SessionLocal()

    res = db.query(DeviceDataBind).where((and_(DeviceDataBind.device_uuid == uuid,
                                               DeviceDataBind.device_prop == device_prop))).all()

    db.close()
    return jsonable_encoder(res)


class CRUDDeviceDataBind(CRUDBase[DeviceDataBind, DeviceDataBind, DeviceDataBind]):

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[DeviceDataBind]:

        return cacheable_get_data_binders(skip=skip, limit=limit)

    def get_subscribers(self, uuid: UUID4, device_prop: str):
        return cacheable_get_subscribers(uuid=str(uuid), device_prop=device_prop)

    def create(self, db: Session, *, obj_in: RegisterDeviceDataBind) -> DeviceDataBind:
        # invalidate redis cache
        cacheable_get_data_binders.invalidate_all()
        cacheable_get_subscribers.invalidate_all()

        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: DeviceDataBind,
            obj_in: Union[PatchDeviceDataBind, Dict[str, Any]]
    ) -> DeviceDataBind:
        # invalidate redis cache
        cacheable_get_data_binders.invalidate_all()
        cacheable_get_subscribers.invalidate_all()

        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> DeviceDataBind:
        # invalidate redis cache
        cacheable_get_data_binders.invalidate_all()
        cacheable_get_subscribers.invalidate_all()

        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


device_data_bind = CRUDDeviceDataBind(DeviceDataBind)
