from fastapi import APIRouter

from .frontend import frontend_router

web_router = APIRouter()

web_router.include_router(frontend_router)
