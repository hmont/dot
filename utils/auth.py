import functools

from typing import Callable
from typing import Optional
from typing import cast

from fastapi import Request
from fastapi.responses import RedirectResponse

from state.global_state import redis

from tables import users

from objects.user import User

def require_auth(func: Callable):

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get('request')

        if request is None:
            raise ValueError("Endpoints using the @require_auth decorator "
                             "must include the request as an argument")

        request = cast(Request, request)

        session_id: Optional[str] = request.cookies.get('session_id')

        if not session_id:
            return RedirectResponse(url="/login")

        redis_user = await redis.get(session_id)

        if not redis_user:
            return RedirectResponse(url="/login")

        return await func(*args, **kwargs)

    return wrapper

async def get_user(request: Request) -> Optional[User]:
    session_id = request.cookies.get('session_id')

    if not session_id:
        return None

    user_id = await redis.get(session_id)

    if not user_id:
        return None

    user = await users.fetch_one(user_id=user_id)

    if not user:
        return None

    return user