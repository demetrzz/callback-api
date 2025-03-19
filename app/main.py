from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.db import init_db
from app.routes import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
