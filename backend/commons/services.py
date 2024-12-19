from typing import Callable, Generic, TypeVar
from ninja import Schema
from .builders import WithBuild, Builder


M = TypeVar("M", bound=WithBuild)
S = TypeVar("S", bound=Schema)


class Service(Generic[M]):
    def __init__(self, model: type[M]):
        self.model = model
