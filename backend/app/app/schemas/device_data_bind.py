from typing import Union

from pydantic import BaseModel, Field


class DeviceDataBindBase(BaseModel):
    id: int
    binder_name: str
    device_id: int
    device_prop: str
    subscriber_id: int
    char_placeholder: int

    class Config:
        orm_mode = True
