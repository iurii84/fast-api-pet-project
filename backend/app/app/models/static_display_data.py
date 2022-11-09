from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class StaticDisplayData(Base):

    __tablename__ = 'static_display_data'

    id = Column(postgresql.BIGINT, primary_key=True, index=True)
    frame_name = Column(postgresql.VARCHAR(50), nullable=True)
    device_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    frame_priority = Column(postgresql.SMALLINT, nullable=True)
    data_json = Column(postgresql.JSON, nullable=False)
    is_active = Column(postgresql.BOOLEAN, nullable=False, default=False)
    placed_databinds = Column(postgresql.TEXT, nullable=True, default="")
