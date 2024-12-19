from django.core.handlers.wsgi import WSGIRequest
from ninja import *
from backend.requests import AuthenticatedRequest
from users.schemas import UserSchema
from .tokens import *
from .bearers import *
from .forms import *
from .schemas import *
from .services import AuthService, User

router = Router(tags=["auth"])


@router.post("/signup", response=TokenResponse)
def signup(
    request: WSGIRequest,
    form: SignUpForm,
):
    service = AuthService()
    user = service.signup(form)
    refresh = RefreshToken.from_user(user)
    access = refresh.access_token
    return dict(refresh=refresh.encode(), access=access.encode())


@router.post("/signin", response=TokenResponse)
def signin(request: WSGIRequest, username: Form[str], password: Form[str]):
    service = AuthService()
    user = service.signin(username, password)
    refresh = RefreshToken.from_user(user)
    access = refresh.access_token
    return dict(refresh=refresh.encode(), access=access.encode())


@router.post("/refresh", response=TokenResponse)
def refresh(request: WSGIRequest, form: RefreshForm):
    token = RefreshToken.decode(form.refresh)

    return dict(refresh=token.encode(), access=token.access_token.encode())


@router.get(
    "/me",
    auth=JwtBearer(),
    response=UserSchema,
)
def me(request: AuthenticatedRequest[User]):
    return request.auth
