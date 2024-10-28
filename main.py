from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from core.shared.db import init_db
from core.shared.conf import settings
from core.auth.routes import auth_route
from core.family.routes import family_router
from core.bank.routes import bank_routes
# from core.shared.middleware import JWTBearer, JWTMiddleware

SERVER_PREFIX = "/api"

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup event
    await init_db()
    yield
    # Shutdown event
    await Tortoise.close_connections()

app = FastAPI(
    title="DUMMY_PROJECT",
    version="1.0.0",
    openapi_url=f"{SERVER_PREFIX}/openapi.json",
    docs_url=f"{SERVER_PREFIX}/docs",
    redoc_url=f"{SERVER_PREFIX}/redoc",
    debug=True,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Uncomment and configure JWT Middleware if required
# app.add_middleware(JWTMiddleware)

register_tortoise(
    app,
    db_url=settings.DATABASE,
    modules={"models": ["core.shared.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(auth_route, prefix=f"{SERVER_PREFIX}/auth", tags=["auth"])
app.include_router(family_router, prefix=f"{SERVER_PREFIX}/family", tags=["family"])
app.include_router(bank_routes, prefix=f"{SERVER_PREFIX}/bank", tags=["bank"])
