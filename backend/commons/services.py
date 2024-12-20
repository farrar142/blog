from typing import Callable, Generic, TypeVar
from ninja import Schema

from commons.repository import Repository
from .builders import WithBuild, Builder


M = TypeVar("M", bound=WithBuild)
S = TypeVar("S", bound=Schema)
PK = TypeVar("PK")


class Service(Generic[M]):
    def __init__(self, model: type[M]):
        self.model = model
