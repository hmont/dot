import functools

from typing import Callable
from typing import Optional
from typing import cast

from fastapi import Request
from fastapi.responses import RedirectResponse

from state.global_state import redis

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
