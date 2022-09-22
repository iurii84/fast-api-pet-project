from sqlalchemy import Column, Integer
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class DeviceType(Base):
    __tablename__ = 'device_type'

    type_id = Column(Integer, primary_key=True, index=True)
    name = Column(postgresql.VARCHAR(50), nullable=False)
    description = Column(postgresql.TEXT, nullable=True)
    screen_type = Column(postgresql.SMALLINT, nullable=True, default=None)
    json = Column(postgresql.JSON, nullable=True, default={})

