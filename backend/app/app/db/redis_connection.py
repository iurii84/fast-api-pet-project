import redis

redis_previous_device_data = redis.Redis(host='redis',
                                         port=6379,
                                         db=1,
                                         decode_responses=True)
