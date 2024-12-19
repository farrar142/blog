from typing import Any, Self
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from commons.builders import WithBuild


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
