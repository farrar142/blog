from typing import Any, Self
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class Builder[T]:

    def __init__(self, model: type[T]):
        self.model = model
        self.kwargs = dict()

    def set(self, key: str, value: Any):
        self.kwargs[key] = value
        return self

    def from_dict(self, dictionary: dict):
        for key, value in dictionary.items():
            self.set(key, value)
        return self

    def build(self):
        model = self.model()
        for key, value in self.kwargs.items():
            setattr(model, key, value)
        return model


class WithBuild:
    @classmethod
    def builder(cls):
        return Builder(cls)


# Create your models here.
class User(AbstractUser, WithBuild):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    REQUIRED_FIELDS = ["email"]
    USERNAME_FIELD = "username"
    pass
