from sqlalchemy import Column, Integer, Float
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID


from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), nullable=False)
    temp = Column(Float, index=True)
    hum = Column(Float, index=True)
    created = Column(postgresql.TIMESTAMP, nullable=False, index=True)
    compress_ratio = Column(postgresql.SMALLINT, default=0, nullable=False)
    type = Column(postgresql.SMALLINT, nullable=True)
