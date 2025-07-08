from typing import Optional

from fastapi import APIRouter
from fastapi import Request

from tables import users as users_table

router = APIRouter(prefix='/users')

@router.post('/fetch')
#@require_auth
async def fetch_user(request: Request, u: Optional[int] = None, name: Optional[str] = None):
    kwargs = {}

    if not u and not name:
        return {'success': False, 'message': 'one of u or name must be provided'}

    if u:
        kwargs['user_id'] = u

    if name:
        kwargs['username'] = name

    user = await users_table.fetch_one(**kwargs)

    if not user:
        return {'success': False, 'message': 'user not found'}

    content = user.to_dict()

    return {'success': True, 'user': content}