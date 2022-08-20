from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base


# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class Sensor(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    uuid = Column(nullable=False)
    type = Column(Integer, nullable=True)
    location = Column(Integer, nullable=True)
    first_occurrence = Column(postgresql.TIMESTAMP, nullable=False)
    date_registered = Column(postgresql.TIMESTAMP, nullable=True)


class SensorToRegister(Base):
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(nullable=False)
    type = Column(Integer, nullable=True)
    first_occurrence = Column(postgresql.TIMESTAMP, nullable=False)

