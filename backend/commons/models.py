from typing import Generic, TypeVar
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

User = get_user_model()


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


U = TypeVar("U", bound=AbstractBaseUser)


def get_owner_model(related_name: str):
    from users.models import User

    class OwnerModel(BaseModel):
        class Meta:
            abstract = True

        owner = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name=related_name
        )

    return OwnerModel
