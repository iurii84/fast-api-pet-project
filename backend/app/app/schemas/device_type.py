from typing import Union

from pydantic import BaseModel, Field


class DeviceTypeBase(BaseModel):
    type_id: int
    name: str
    description: str
    screen_type: Union[None, int]
    json_field: Union[None, dict] = Field(alias='json')

    class Config:
        orm_mode = True
