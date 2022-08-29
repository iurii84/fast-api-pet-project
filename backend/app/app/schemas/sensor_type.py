from pydantic import BaseModel


class SensorTypeBase(BaseModel):
    type_id: int
    name: str
    description: str

    class Config:
        orm_mode = True
