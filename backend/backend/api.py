from ninja import NinjaAPI
from .errors import Error, PermissionDenied
from authentications.api import router as auth_router
from articles.api import router as article_router

ninja = NinjaAPI()
Error.register(ninja)
PermissionDenied.register(ninja)

ninja.add_router("auth/", auth_router)
ninja.add_router("articles/", article_router)
