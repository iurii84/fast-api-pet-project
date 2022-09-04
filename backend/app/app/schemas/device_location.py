from pydantic import BaseModel


class DeviceLocationBase(BaseModel):
    location_id: int
    name: str
    description: str

    class Config:
        orm_mode = True
