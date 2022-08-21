import datetime

from typing import Union

from pydantic import BaseModel, UUID4


class MessageBase(BaseModel):
    uuid: UUID4


class Message(MessageBase):
    temp: Union[None, float]
    hum: Union[None, float]
    type: Union[None, int]


class MessageInDb(Message):
    id: int
    created: datetime.datetime

    class Config:
        orm_mode = True


class MessageCompress(MessageBase):
    start_date_time: datetime.datetime
    end_date_time: datetime.datetime
    for_items_with_compress_ratio: int
