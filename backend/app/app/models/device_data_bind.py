from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class DeviceDataBind(Base):

    __tablename__ = 'device_data_bind'

    id = Column(postgresql.BIGINT, primary_key=True, index=True)
    binder_name = Column(postgresql.VARCHAR(50), nullable=True)
    device_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    device_prop = Column(postgresql.VARCHAR(50), nullable=False)
    subscriber_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    char_placeholder = Column(postgresql.SMALLINT, nullable=True)
