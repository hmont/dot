from typing import Optional

from fastapi import APIRouter, Request

from state.global_state import classifier

from tables import posts

from utils.auth import require_auth
from utils.auth import get_user

from constants import Privileges

router = APIRouter(prefix='/posts')

@router.post('/create')
@require_auth(endpoint=True)
async def create_post(request: Request):
    """
    The endpoint for post creation.

    Requires that the user be logged in.
    """
    user = await get_user(request)

    assert user is not None

    data = await request.json()

    content = data['content'].strip()[:120]

    if len(content) < 1:
        return {
            'success': False,
            'message': 'post cannot be empty'
        }

    positivity_score = classifier.predict(content)

    if positivity_score < 2:
        return {
            'success': False,
            'message': 'this post looks a bit negative - remember, '
                       'dot is all about spreading love and positivity!'
        }

    await posts.create(
        poster=user.id,
        content=content
    )

    return {'success': True, 'message': 'post created successfully!'}

@router.post('/fetch')
# @require_auth(endpoint=True)
async def fetch_posts(
    request: Request,
    u: Optional[int] = None,
    p: Optional[int] = None,
    s: Optional[int] = None
):
    """
    The endpoint for post fetching.
    """
    user = await get_user(request)

    user_id = user.id if user else None

    _posts = await posts.fetch_public(
        auth_user_id=user_id, page=p, page_size=s, poster=u
    )

    content = {
        'success': True,
        'posts': [
            post.to_dict() for post in _posts
        ]
    }

    return content

@router.post('/delete')
@require_auth(endpoint=True)
async def delete(request: Request):
    """
    Endpoint for deleting posts.

    Requires that the user be logged in
    """
    user = await get_user(request)

    assert user is not None

    post_id = (await request.json()).get('post')

    payload = {
        'success': False,
        'message': 'no post ID provided'
    }

    if post_id is None:
        return payload

    post = await posts.fetch_one(post_id)

    if post is None:
        payload['message'] = 'post not found'
        return payload

    if user.privs < Privileges.MODERATOR and user.id != post.poster_id:
        payload['message'] = 'no permission'
        return payload

    await posts.delete_one(post_id=post_id)

    payload['success'] = True
    payload['message'] = 'post deleted'

    return payload
