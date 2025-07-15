from typing import Optional

from fastapi import APIRouter
from fastapi import Request

from tables import users as users_table
from tables import user_preferences

from utils.auth import require_auth
from utils.auth import get_user

router = APIRouter(prefix='/users')

@router.post('/fetch')
@require_auth(endpoint=True)
async def fetch_user(
    request: Request,
    u: Optional[int] = None,
    name: Optional[str] = None,
):
    kwargs = {}
    req_user = await get_user(request)

    assert req_user is not None

    if not u and not name:
        return {'success': False, 'message': 'one of u or name must be provided'}

    if u:
        kwargs['user_id'] = u

    if name:
        kwargs['username'] = name

    user = await users_table.fetch_one(**kwargs)

    if not user:
        return {'success': False, 'message': 'user not found'}

    prefs = await user_preferences.fetch_one(user.id)

    if prefs is not None and prefs.is_private and req_user.id != user.id:
        return {'success': False, 'is_private': True}

    content = user.to_dict()

    return {'success': True, 'is_private': False, 'user': content}
