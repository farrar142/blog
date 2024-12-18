from ninja import NinjaAPI
from .errors import Error
from authentications.api import router

ninja = NinjaAPI()
Error.register(ninja)

ninja.add_router("auth/", router)
