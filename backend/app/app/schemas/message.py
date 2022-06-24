from typing import Optional, Union

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    uuid: str
    temp: Union[None, float]
    hum: Union[None, float]


class Message(MessageBase):
    pass
