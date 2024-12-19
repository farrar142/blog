from functools import partial
from pprint import pprint
from typing import ParamSpec, TypeVar
from django.contrib.auth.models import AbstractBaseUser
from django.http.response import HttpResponse
from django.test import TestCase as TC, Client as Cl

from authentications.tokens import RefreshToken

# Create your tests here.
P = ParamSpec("P")
T = TypeVar("T")


class Client(Cl):

    def _login(self, token: str):
        if not self.headers:
            self.headers = dict()
        self.headers.update(Authorization=token)

    def login(self, user: AbstractBaseUser) -> bool:
        refresh = RefreshToken.from_user(user)
        access = refresh.access_token

        token = f"Bearer {access.encode()}"
        self._login(token)
        return True

    def get(self, *args, **kwargs) -> HttpResponse:
        return partial(super().get, headers=self.headers)(*args, **kwargs)

    def post(self, *args, **kwargs) -> HttpResponse:
        return partial(super().post, headers=self.headers)(*args, **kwargs)

    def patch(self, *args, **kwargs) -> HttpResponse:
        return partial(super().patch, headers=self.headers)(*args, **kwargs)

    def delete(self, *args, **kwargs) -> HttpResponse:
        return partial(super().delete, headers=self.headers)(*args, **kwargs)


class TestCase(TC):
    client: Client
    client_class = Client

    @property
    def pp(self):
        return pprint
