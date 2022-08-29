from app.crud.base import CRUDBase
from app.models import SensorLocation


class CRUDSensorLocation(CRUDBase[SensorLocation, SensorLocation, SensorLocation]):
    pass


sensor_location = CRUDSensorLocation(SensorLocation)
