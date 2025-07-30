from datetime import datetime

from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse

import timeago

from utils.auth import get_user
from utils.auth import require_auth

from tables import users
from tables import user_preferences

templates = Jinja2Templates("templates")

frontend_router = APIRouter()

@frontend_router.get("/")
async def index(request: Request):
    """
    Homepage
    """
    return templates.TemplateResponse(name="index.html", request=request)


@frontend_router.get("/login")
async def login(request: Request):
    """
    Login page (/login)
    """
    if await get_user(request) is not None:
        return RedirectResponse('/feed')

    return templates.TemplateResponse(name="login.html", request=request)


@frontend_router.get("/register")
async def register(request: Request):
    """
    Registration page (/register)
    """
    if await get_user(request) is not None:
        return RedirectResponse('/feed')

    return templates.TemplateResponse(name="register.html", request=request)


@frontend_router.get("/feed")
# @require_auth()
async def feed(request: Request):
    """
    Feed page (/feed)
    """
    user = await get_user(request)

    # assert user is not None

    return templates.TemplateResponse(
        name="feed.html",
        request=request,
        context={'username': user.username if user else '',
                 'sign_up_button': (user is None)}

    )


@frontend_router.get("/users/{username}")
# @require_auth()
async def profile(request: Request, username: str):
    """
    User profile (/users/[username])
    """
    user = await users.fetch_one(username=username)

    logged_in_user = await get_user(request)

    context = {'username': logged_in_user.username if logged_in_user else ''}

    if not user:
        return templates.TemplateResponse(
            name="404.html",
            request=request,
            context=context
        )

    prefs = await user_preferences.fetch_one(user.id)

    if not prefs:
        return templates.TemplateResponse(
            name="404.html",
            request=request,
            context=context
        )

    if prefs.is_private and (not logged_in_user or logged_in_user.username != username):
        return templates.TemplateResponse(name="private_profile.html", request=request)

    return templates.TemplateResponse(
        name="profile.html",
        request=request,
        context={
            'user': user,
            'time_ago': timeago.format(user.created_at, datetime.now()),
            'user_id': user.id,
            'current_username': logged_in_user.username if logged_in_user else '',
            'sign_up_button': (logged_in_user is None)
        }
    )


@frontend_router.get("/dashboard")
@require_auth()
async def dashboard(request: Request):
    """
    Dashboard page (/dashboard)
    """
    user = await get_user(request)

    assert user is not None

    return templates.TemplateResponse(
        name="dashboard.html",
        request=request,
        context={'username': user.username})


async def handler_404(request: Request, exc):
    """
        Handler for 404 errors.
    """
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@frontend_router.get('/favicon.ico')
async def favicon(request: Request):
    return FileResponse('static/img/favicon.ico')