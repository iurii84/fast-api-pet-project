from fastapi import APIRouter

from app.api.api_v1.endpoints import \
    items, login, users, utils, message, device, device_location, device_type, task, device_data_bind, static_display_data

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(message.router, prefix="/message", tags=["message"])
api_router.include_router(device.router, prefix="/device", tags=["device"])
api_router.include_router(device_location.router, prefix="/device_location", tags=["device_location"])
api_router.include_router(device_type.router, prefix="/device_type", tags=["device_type"])
api_router.include_router(task.router, prefix="/task", tags=["task"])
api_router.include_router(device_data_bind.router, prefix="/device_data_bind", tags=["device_data_bind"])
api_router.include_router(static_display_data.router, prefix="/static_display_data", tags=["static_display_data"])
