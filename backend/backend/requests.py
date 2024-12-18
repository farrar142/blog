from typing import TYPE_CHECKING, Generic, TypeVar
from django.core.handlers.wsgi import WSGIRequest

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser

U = TypeVar("U", bound="AbstractBaseUser")


class AnonymousRequest(WSGIRequest):
    auth: None


class AuthenticatedRequest(WSGIRequest, Generic[U]):
    auth: U
