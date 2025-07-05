from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from fastapi.responses import PlainTextResponse

from utils.auth import require_auth

from state.global_state import classifier

templates = Jinja2Templates("templates")

frontend_router = APIRouter()


@frontend_router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@frontend_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", request=request)

@frontend_router.get("/register")
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)

@frontend_router.get("/test/{text}")
async def test(request: Request, text: str):
    result = classifier.predict(text)

    print(f"Text: {text}\nResult: {result}")

    if result < 2:
        return PlainTextResponse("Try sending a more friendly message")
    else:
        return PlainTextResponse("Sufficiently happy")

@frontend_router.get("/feed")
@require_auth
async def feed(request: Request):
    return templates.TemplateResponse(name="feed.html", request=request)
