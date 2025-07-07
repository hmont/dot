from datetime import datetime

from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from fastapi.responses import PlainTextResponse

import timeago

from utils.auth import require_auth

from state.global_state import classifier

from tables import users

templates = Jinja2Templates("templates")

frontend_router = APIRouter()

@frontend_router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@frontend_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)

@frontend_router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)

@frontend_router.get("/feed")
@require_auth
async def feed(request: Request):
    return templates.TemplateResponse(name="feed.html", request=request)

@frontend_router.get("/users/{username}")
async def profile(request: Request, username: str):
    user = await users.fetch_one(username=username)

    if not user:
        return templates.TemplateResponse(name="404.html", request=request)

    return templates.TemplateResponse(
        name="profile.html",
        request=request,
        context={
            'user': user,
            'time_ago': timeago.format(user.created_at, datetime.now()),
            'user_id': user.id
        }
    )