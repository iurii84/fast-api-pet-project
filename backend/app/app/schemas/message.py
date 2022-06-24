from typing import Optional, Union

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    uuid: str


class Message(MessageBase):
    temp: Union[None, float]
    hum: Union[None, float]


class MessageInDb(Message):
    id: int

    class Config:
        orm_mode = True
