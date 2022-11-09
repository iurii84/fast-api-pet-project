from typing import Union, List

from pydantic import BaseModel, UUID4


class StaticDisplayData(BaseModel):
    id: int
    frame_name: Union[None, str]
    device_uuid: UUID4
    frame_priority: Union[None, int]
    data_json: dict

    class Config:
        orm_mode = True


class StaticDisplayDataRegister(BaseModel):
    frame_name: Union[None, str]
    device_uuid: UUID4
    frame_priority: Union[None, int]
    data_json: list
    placed_databinds: List[int]
    is_active: bool
