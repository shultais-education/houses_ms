from redis.asyncio import Redis
import json


class CacheService:

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    async def get(self, key, default=None):
        data = await self.redis_client.get(key)

        if data is not None:
            return json.loads(data)

        return default

    async def set(self, key, value, ttl=None):
        value = json.dumps(value)
        await self.redis_client.setex(name=key, value=value, time=ttl)
        return True
