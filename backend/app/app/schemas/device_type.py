from pydantic import BaseModel


class DeviceTypeBase(BaseModel):
    type_id: int
    name: str
    description: str

    class Config:
        orm_mode = True
