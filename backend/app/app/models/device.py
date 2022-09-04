from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import postgresql

from app.db.base_class import Base


# if TYPE_CHECKING:
#     from .message import Message  # noqa: F401


class Device(Base):
    id = Column(postgresql.BIGINT, primary_key=True, index=True)
    name = Column(postgresql.TEXT, nullable=True)
    uuid = Column(nullable=False)
    type = Column(postgresql.SMALLINT, nullable=True)
    location = Column(postgresql.SMALLINT, nullable=True)
    first_occurrence = Column(postgresql.TIMESTAMP, nullable=False)
    date_registered = Column(postgresql.TIMESTAMP, nullable=True)





