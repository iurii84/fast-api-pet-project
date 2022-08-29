from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, message, sensor, sensor_location, sensor_type

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(message.router, prefix="/message", tags=["message"])
api_router.include_router(sensor.router, prefix="/sensor", tags=["sensor"])
api_router.include_router(sensor_location.router, prefix="/sensor_location", tags=["sensor_location"])
api_router.include_router(sensor_type.router, prefix="/sensor_type", tags=["sensor_type"])
