from .crud_item import item
from .crud_user import user
from .crud_message import message
from .crud_device import device
from .crud_device_location import device_location
from .crud_device_type import device_type
from .crud_device_data_bind import device_data_bind
from .crud_static_display_data import static_display_data

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
