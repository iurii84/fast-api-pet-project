from app.crud.base import CRUDBase
from app.models import DeviceType


class CRUDDeviceType(CRUDBase[DeviceType, DeviceType, DeviceType]):
    pass


device_type = CRUDDeviceType(DeviceType)
