from fastapi import APIRouter
from fastapi import Request
from fastapi import Response

import bcrypt

from utils.auth import get_user
from utils.auth import logout

from tables import users
from tables import posts
from tables import user_preferences

router = APIRouter(prefix='/account')

@router.post('/delete')
async def delete_account(request: Request, response: Response):
    user = await get_user(request)

    if user is None:
        return {'success': False,
                'message': 'not logged in'}

    password: str | None = (await request.json()).get('password')

    if not password or not bcrypt.checkpw(
        password.encode(), user.password_bytes
    ):
        return {'success': False,
                'message': 'incorrect password'}

    await logout(request=request, response=response) # type: ignore

    await users.delete_one(user_id=user.id)
    await user_preferences.delete_one(user_id=user.id)
    await posts.delete(poster_id=user.id)



    return {'success': True,
            'message': 'we\'re sorry to see you go :('}
