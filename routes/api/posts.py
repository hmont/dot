from typing import Optional

from fastapi import APIRouter, Request

from state.global_state import redis
from state.global_state import classifier

from tables import posts

from utils.auth import require_auth
from utils.auth import get_user

router = APIRouter(prefix='/posts')

@router.post('/create')
@require_auth(endpoint=True)
async def create_post(request: Request):
    """
    The endpoint for post creation.

    Requires that the user be logged in.
    """
    session_id = request.cookies['session_id']

    user_id = await redis.get(session_id)

    data = await request.json()

    content = data['content'][:120]

    positivity_score = classifier.predict(content)

    if positivity_score < 2:
        return {
            'success': False,
            'message': 'this post looks a bit negative - remember, '
                       'dot is all about spreading love and positivity!'
        }

    await posts.create(
        poster=user_id,
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
