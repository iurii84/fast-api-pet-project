import datetime
import typing
from typing import Optional, Union

import uuid as uuid
from pydantic import BaseModel, Field, UUID4


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
