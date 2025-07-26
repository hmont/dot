import functools

from typing import Callable
from typing import Optional

from fastapi import Request
from fastapi import Response

from fastapi.responses import RedirectResponse

from state.global_state import redis

from tables import users

from objects.user import User

async def get_user(request: Optional[Request]) -> Optional[User]:
    """
    Returns the user of the given request, or None if there is none.
    """
    if request is None:
        raise ValueError('endpoints or pages using the @require_auth '
                         'decorator must include the request '
                         'as an argument')

    session_id = request.cookies.get('session_id')

    if not session_id:
        return None

    user_id = await redis.get(session_id) if session_id else None

    if not user_id:
        return None

    user = await users.fetch_one(user_id=user_id)

    if not user:
        return None

    return user


def require_auth(endpoint: bool = False):
    """
    Decorator to indicate that a webpage or API endpoint requires the user to be \
    logged in (i.e. have a valid session ID).

    Args:
        endpoint (bool, optional): Whether this path is an \
        API endpoint (True) or a page (False). Defaults to False.
    """
    def factory(func: Callable):

        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            kwargs.pop('require_auth', None)

            if require_auth and await get_user(kwargs.get('request')) is None:
                if not endpoint:
                    return RedirectResponse('/login')

                return {
                    'success': False,
                    'message': 'you must login or sign up to do this'
                }

            return await func(*args, **kwargs)
        return wrapper
    return factory


async def logout(request: Request, response: Response):
    """
    Log out the user of the given request and return the given Response.
    """
    session_id = request.cookies.get('session_id')

    if session_id is None:
        return {'success': False, 'message': 'not logged in'}

    await redis.delete(session_id)

    response.delete_cookie('session_id')

    return {'success': True, 'message': 'logged out'}
