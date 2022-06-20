from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = Field(example="My super-pooper title")
    description: Optional[str] = Field(example="My even greater description")
    abc: UUID

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "id": "228",
    #             "title": "A very nice Item",
    #             "owner_id": 5678,
    #         }
    #     }


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True



# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
