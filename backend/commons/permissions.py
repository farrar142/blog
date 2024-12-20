from typing import Generic, Protocol, TypeVar
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from backend.requests import AuthenticatedRequest

U = TypeVar("U", bound=AbstractBaseUser)


class OwnerProtocol(Protocol[U]):
    owner: models.ForeignKey[U]


def is_resource_owner(user: U):
    def wrapper(resource: OwnerProtocol):
        return True if user.pk == resource.owner.pk else None  # type:ignore

    return wrapper
