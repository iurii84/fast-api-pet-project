from typing import Union

from pydantic import BaseModel, UUID4


class DeviceDataBindBase(BaseModel):
    id: int
    binder_name: str
    device_uuid: UUID4
    device_prop: str
    subscriber_uuid: UUID4
    char_placeholder: int

    class Config:
        orm_mode = True


class RegisterDeviceDataBind(BaseModel):
    binder_name: str
    device_uuid: UUID4
    device_prop: str
    subscriber_uuid: UUID4
    char_placeholder: int


class PatchDeviceDataBind(BaseModel):
    binder_name: Union[None, str]
    device_uuid: Union[None, UUID4]
    device_prop: Union[None, str]
    subscriber_uuid: Union[None, UUID4]
    char_placeholder: Union[None, int]