from typing import Generic, TypeVar
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

U = TypeVar("U", bound=AbstractBaseUser)
User = get_user_model()


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


def get_owner_model(user_cls: type[U], related_name: str):
    class OwnerModel(BaseModel):
        class Meta:
            abstract = True

        owner: "models.ForeignKey[user_cls]" = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name=related_name
        )  # type:ignore

    return OwnerModel
