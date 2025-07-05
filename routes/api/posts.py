from fastapi import APIRouter, Request

from utils.auth import require_auth

from state.global_state import redis

from tables import posts

router = APIRouter(prefix='/posts')

@router.post('/create')
@require_auth
async def create_post(request: Request):
    session_id = request.cookies['session_id']

    user_id = await redis.get(session_id)

    data = await request.json()

    content = data['content']

    await posts.create(
        poster=user_id,
        content=content
    )

    return {"message": "success"}