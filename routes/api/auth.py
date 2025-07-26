import secrets

from datetime import timedelta
from datetime import datetime
from datetime import timezone

from fastapi import APIRouter
from fastapi import Request
from fastapi import Response

from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError

import bcrypt

from tables import users

from state.global_state import redis

from utils import settings

from utils.auth import require_auth
from utils.auth import logout as _logout

router = APIRouter(prefix='/auth')

@router.post('/register')
async def register(request: Request):
    """
    The endpoint for account creation.
    """
    if not settings.REGISTRATION_ENABLED:
        return {
            'success': False,
            'message': 'registration is disabled for this '
                       'instance'
        }

    body = await request.json()

    username: str = body['username']
    password: str = body['password']

    if not username.isalnum():
        return {
            'success': False,
            'message': 'username can only contain '
                       'alphanumeric characters'
        }

    password_hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(12)
    )

    content = {
        "success": True,
        "message": "account created - you may now login"
    }

    try:
        await users.create(
            username=username,
            password_bytes=password_hashed
        )
    except IntegrityError:
        content['success'] = False
        content['message'] = 'another user already exists with this username'

    return JSONResponse(content=content)


@router.post('/login')
async def login(request: Request, response: Response):
    """
    The endpoint for account login.
    """
    body = await request.json()

    username: str = body['username']
    password: str = body['password']

    content = {
        "success": True,
        "message": "logged in successfully - redirecting"
    }

    user = await users.fetch_one(username=username)

    if not user or not bcrypt.checkpw(
        password.encode(), user.password_bytes
    ):
        content['success'] = False
        content['message'] = 'invalid username/password combination'
        return JSONResponse(content=content)

    session_id = secrets.token_urlsafe(32)

    expiry = datetime.now(timezone.utc) + timedelta(days=7)

    response.set_cookie(
        key='session_id',
        value=session_id,
        expires=expiry,
        httponly=True,
        samesite='lax',
        secure=True
    )

    await redis.set(
        name=session_id,
        value=user.id,
        ex=timedelta(days=7)
    )

    return content


@router.post('/logout')
@require_auth(endpoint=True)
async def logout(request: Request, response: Response):
    """
    The endpoint for account logout.

    Requires that the user be logged in.
    """
    return await _logout(request=request, response=response)
