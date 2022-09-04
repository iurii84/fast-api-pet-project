import datetime

from typing import Union

from pydantic import BaseModel, UUID4


class SensorBase(BaseModel):
    uuid: UUID4


class Device(SensorBase):
    id: Union[None, int]
    name: Union[None, str]
    type: Union[None, int]
    location: Union[None, int]
    first_occurrence: datetime.datetime
    date_registered: datetime.datetime

    class Config:
        orm_mode = True


class DeviceToRegister(SensorBase):
    first_occurrence: datetime.datetime
    type: Union[None, int]


class RegisterDevice(SensorBase):
    name: Union[None, str]
    location: Union[None, int]


class RegisterDeviceReturn:
    id: Union[None, int]
