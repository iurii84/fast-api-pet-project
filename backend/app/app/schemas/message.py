from typing import Optional

from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    item: str


class Message(MessageBase):
    pass
