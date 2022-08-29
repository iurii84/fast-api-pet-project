from app.crud.base import CRUDBase
from app.models import SensorType


class CRUDSensorType(CRUDBase[SensorType, SensorType, SensorType]):
    pass


sensor_type = CRUDSensorType(SensorType)
