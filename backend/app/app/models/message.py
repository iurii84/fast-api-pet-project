#from fastapi_utils.guid_type import GUID
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    # uuid = Column(GUID)
    uuid = Column()
    temp = Column(Float, index=True)
    hum = Column(Float, index=True)
    created = Column(postgresql.TIMESTAMP, nullable=False)
