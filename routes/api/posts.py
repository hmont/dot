from typing import Optional

from fastapi import APIRouter, Request

from utils.auth import require_auth

from state.global_state import redis
from state.global_state import classifier

from tables import posts

from utils.auth import get_user

router = APIRouter(prefix='/posts')

@router.post('/create')
@require_auth(endpoint=True)
async def create_post(request: Request):
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
@require_auth(endpoint=True)
async def fetch_posts(
    request: Request,
    u: Optional[int] = None,
    p: Optional[int] = None,
    s: Optional[int] = None
):
    user = await get_user(request)

    assert user is not None

    _posts = await posts.fetch_public(
        auth_user_id=user.id, page=p, page_size=s, poster=u
    )

    content = {
        'success': True,
        'posts': [
            post.to_dict() for post in _posts
        ]
    }

    return content