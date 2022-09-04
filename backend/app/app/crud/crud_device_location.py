from app.crud.base import CRUDBase
from app.models import DeviceLocation


class CRUDDeviceLocation(CRUDBase[DeviceLocation, DeviceLocation, DeviceLocation]):
    pass


device_location = CRUDDeviceLocation(DeviceLocation)
