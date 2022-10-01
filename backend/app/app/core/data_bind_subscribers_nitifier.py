import json

from app.crud.crud_device_data_bind import cacheable_get_subscribers
from app.db.redis_connection import redis_connection


def notify_subscribers(uuid: str, device_prop: str, new_value: int):
    print(f"SUBSCRIBER_DATA {uuid}  {device_prop}  {new_value}")
    bind_subscribers = cacheable_get_subscribers(uuid=uuid, device_prop=device_prop)

    if bind_subscribers:
        for binder in bind_subscribers:
            redis_connection.publish(binder['subscriber_uuid'], json.dumps({"binder_id": binder["id"],
                                                                            "value": new_value}))
