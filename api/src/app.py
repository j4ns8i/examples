from fastapi import FastAPI, Response
import fastapi
from loguru import logger
import redis.asyncio as _redis

from . import config
from .logger import logger

app = FastAPI()
pool = _redis.ConnectionPool(host=config.redis_host, port=config.redis_port, protocol=3)
redis = _redis.Redis(connection_pool=pool)


@app.get("/healthz")
async def healthz(response: Response):
    try:
        await redis.ping()
        return {"status": "up"}
    except Exception as e:
        logger.bind(error=str(e)).error(f"error pinging redis")
        response.status_code = fastapi.status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "down"}
