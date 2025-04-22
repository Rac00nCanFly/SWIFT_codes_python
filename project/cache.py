from fastapi_redis_cache import FastApiRedisCache, cache
import logging

logger = logging.getLogger(__name__)

redis_cache = FastApiRedisCache()

def init_redis():
    try:
        redis_cache.init(
            host_url="redis://redis:6379",
            prefix="swift-cache",
            socket_timeout=5,  
            socket_connect_timeout=5,
            retry_on_timeout=True,
            health_check_interval=30
        )
        logger.info("Redis connection initialized successfully")
    except Exception as e:
        logger.error(f"Redis connection error: {str(e)}")
        raise