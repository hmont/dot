from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi import Request

from fastapi.staticfiles import StaticFiles

from utils import settings

from state.global_state import classifier
from state.global_state import database

from routes.web import web_router
from routes.api import api_router

from routes.web.frontend import handler_404

@asynccontextmanager
async def lifespan(a: FastAPI): # pylint: disable=unused-argument,missing-function-docstring
    classifier.setup()
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(404)
async def not_found(request: Request): # pylint: disable=missing-function-docstring
    return await handler_404(request)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(web_router)
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app",
        host=settings.DOT_HOST,
        port=settings.DOT_PORT
    )
