from app.crud.base import CRUDBase
from app.models import StaticDisplayData


class CRUDStaticDisplayData(CRUDBase[StaticDisplayData, StaticDisplayData, StaticDisplayData]):
    pass


static_display_data = CRUDStaticDisplayData(StaticDisplayData)
