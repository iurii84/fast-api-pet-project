import datetime

from typing import Union

from pydantic import BaseModel, UUID4


class MessageBase(BaseModel):
    uuid: UUID4


class Message(MessageBase):
    temp: Union[None, float]
    hum: Union[None, float]


class MessageInDb(Message):
    id: int
    created: datetime.datetime

    class Config:
        orm_mode = True
