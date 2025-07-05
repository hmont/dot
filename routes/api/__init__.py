from fastapi import APIRouter

from .posts import router as posts_router
from .auth import router as auth_router

api_router = APIRouter(prefix="/api")

api_router.include_router(posts_router)
api_router.include_router(auth_router)