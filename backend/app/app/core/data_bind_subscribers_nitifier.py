from app.crud.crud_device_data_bind import cacheable_get_subscribers


def notify_subscribers(uuid: str, device_prop: str, new_value: int):
    subscribers = cacheable_get_subscribers(uuid=uuid, device_prop=device_prop)
    subscribers_uuid_list = [subscriber['subscriber_uuid'] for subscriber in subscribers]
    if subscribers:
        print(f"Notify observers for changed value for {device_prop} in {uuid}")
        print(f"SUBSCRIBERS: {subscribers_uuid_list}; NEW VALUE: {new_value}")
