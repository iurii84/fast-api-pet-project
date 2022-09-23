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


class RegisterDeviceDataBind(BaseModel):
    binder_name: str
    device_id: int
    device_prop: str
    subscriber_id: int
    char_placeholder: int


class PatchDeviceDataBind(BaseModel):
    binder_name: Union[None, str]
    device_id: Union[None, int]
    device_prop: Union[None, str]
    subscriber_id: Union[None, int]
    char_placeholder: Union[None, int]