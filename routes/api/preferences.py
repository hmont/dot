from fastapi import APIRouter
from fastapi import Request

from utils.auth import require_auth
from utils.auth import get_user

router = APIRouter(prefix='/preferences')

@router.post('/fetch')
@require_auth
async def fetch_preferences(request: Request):
    user = await get_user(request)

    body = await request.json()

    assert user is not None

    if user.id != body.get('id'):
        return {'success': False,
                'message': 'invalid user'}

