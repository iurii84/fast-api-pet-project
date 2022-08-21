from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects import postgresql


from app.db.base_class import Base

# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class Message(Base):
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column()
    temp = Column(Float, index=True)
    hum = Column(Float, index=True)
    created = Column(postgresql.TIMESTAMP, nullable=False)
    compress_ratio = Column(Integer, default=0, nullable=True)
    type = Column(Integer, nullable=True)
