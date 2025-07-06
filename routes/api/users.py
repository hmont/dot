from fastapi import APIRouter
from fastapi import Request

from tables import users as users_table

router = APIRouter(prefix='/users')

@router.post('/fetch')
#@require_auth
async def fetch_user(request: Request, u: int):
    user = await users_table.fetch_one(user_id=u)

    if not user:
        return {'success': False, 'message': 'user not found'}

    content = user.to_dict()

    return {'success': True, 'user': content}