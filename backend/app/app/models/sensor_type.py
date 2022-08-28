from sqlalchemy import Column, Integer
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class SensorType(Base):
    __tablename__ = 'sensor_type'

    type_id = Column(Integer, primary_key=True, index=True)
    name = Column(postgresql.VARCHAR(50), nullable=False)
    description = Column(postgresql.TEXT, nullable=True)

