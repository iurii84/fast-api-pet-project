from app.crud.base import CRUDBase
from app.models import DeviceDataBind


class CRUDDeviceDataBind(CRUDBase[DeviceDataBind, DeviceDataBind, DeviceDataBind]):
    pass


device_data_bind = CRUDDeviceDataBind(DeviceDataBind)
