import bcrypt

from fastapi import APIRouter
from fastapi import Request

from utils.auth import require_auth
from utils.auth import get_user

from tables import user_preferences
from tables import users

router = APIRouter(prefix='/preferences')

@router.post('/fetch')
@require_auth(endpoint=True)
async def fetch(request: Request):
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    preferences = await user_preferences.fetch_one(user.id)

    if not preferences:
        preferences = await user_preferences.create(user.id)

    assert preferences is not None

    return preferences.to_dict()

@router.post('/fetch_profile_settings')
@require_auth(endpoint=True)
async def fetch_profile_settings(request: Request):
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    return user.to_dict()


@router.post('/update_profile_settings')
@require_auth(endpoint=True)
async def update_profile_settings(request: Request):
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    body = await request.json()

    await users.update_one(
        user_id=user.id,
        display_name=body['display_name'],
        bio=body['bio']
    )

    return {'success': True, 'message': 'profile settings updated!'}


@router.post('/update_password')
@require_auth(endpoint=True)
async def update_password(request: Request):
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    body = await request.json()

    current_pw: str = body['current_password']
    new_pw: str = body['new_password']
    confirm_pw: str = body['confirm_password']

    if not bcrypt.checkpw(current_pw.encode(), user.password_bytes):
        return {'success': False, 'message': 'current password is incorrect'}

    confirm_pw_hashed = bcrypt.hashpw(confirm_pw.encode(), bcrypt.gensalt(12))

    new_pw_encoded = new_pw.encode()

    if not bcrypt.checkpw(new_pw_encoded, confirm_pw_hashed):
        return {'success': False, 'message': 'passwords do not match'}

    new_pw_hashed = bcrypt.hashpw(new_pw_encoded, bcrypt.gensalt(12))

    await users.update_one(
        user_id=user.id,
        password_hash=new_pw_hashed
    )

    return {'success': True, 'message': 'password updated!'}


@router.post('/update')
@require_auth(endpoint=True)
async def update(request: Request):
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    body = await request.json()

    await user_preferences.update_one(
        user_id=user.id,
        is_private=body['is_private']
    )

    return {'success': True, 'message': 'privacy settings updated!'}