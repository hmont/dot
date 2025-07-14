from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from utils import settings

from state.global_state import classifier
from state.global_state import database
from state.global_state import redis

from routes.web import web_router
from routes.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    classifier.setup()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(web_router)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app",
        host=settings.DOT_HOST,
        port=settings.DOT_PORT
    )