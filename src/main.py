import os

import uvicorn as uvicorn
from redis import asyncio as aioredis
import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import redis_conf
from auth.router import router as auth_router
from config import app_configs, settings
from database import database as db


app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.on_event("startup")
async def startup() -> None:
    pool = aioredis.ConnectionPool.from_url(
        settings.REDIS_URL, max_connections=10, decode_responses=True
    )
    redis_conf.redis_client = aioredis.Redis(connection_pool=pool)
    if not db.is_connected:
        await db.connect()
        print(db.is_connected)


@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()
    await redis_conf.redis_client.close()


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "db": db.is_connected
    }


app.include_router(auth_router, prefix="/auth", tags=["Auth"])


uvicorn.run(app)

