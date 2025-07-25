from fastapi import APIRouter

from .posts import router as posts_router
from .auth import router as auth_router
from .users import router as users_router
from .preferences import router as preferences_router
from .accounts import router as accounts_router

api_router = APIRouter(prefix="/api")

api_router.include_router(posts_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(preferences_router)
api_router.include_router(accounts_router)
