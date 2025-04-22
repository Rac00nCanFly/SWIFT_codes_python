from fastapi_redis_cache import FastApiRedisCache, cache

redis_cache = FastApiRedisCache()
redis_cache.init(
    host_url="redis://redis:6379",
    prefix="swift-cache"
)
