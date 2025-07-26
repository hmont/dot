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
    """
    The endpoint for fetching user preferences (e.g. private profile)
    """
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
    """
    The endpoint for fetching user profile settings \
    (e.g. username, biography).

    This takes no query parameters, so it is intended to \
    be used with the dashboard as it gets the user to fetch \
    implicitly.

    Requires the user to be logged in.
    """
    user = await get_user(request)

    if not user:
        return {'success': False,
                'message': 'invalid user'}

    return user.to_dict()


@router.post('/update_profile_settings')
@require_auth(endpoint=True)
async def update_profile_settings(request: Request):
    """
    The endpoint for updating user profile settings \
    (e.g. username, biography).

    This ONLY allows for updating the user's user ID,
    display name, and biography.

    Requires the user to be logged in as it also gets \
    the user to be updated implicitly (see the \
    fetch_profile_settings endpoint).
    """
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
    """
    The endpoint for updating a user's password.

    Requires the user to be logged in.
    """
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
    """
    The endpoint for updating a user's privacy settings (i.e. \
    whether they have a private profile).

    Requires the user to be logged in.
    """
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
