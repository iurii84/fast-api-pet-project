from redis import StrictRedis
from redis_cache import RedisCache


client = StrictRedis(host="redis", port=6379, db=2, decode_responses=True)
cache = RedisCache(redis_client=client)
