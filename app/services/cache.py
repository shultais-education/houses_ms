from redis.asyncio import Redis


class CacheService:

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key):
        ...

    async def set(self, key, value, ttl=None):
        ...
