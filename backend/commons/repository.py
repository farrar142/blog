from typing import Callable, Generic, TypeVar
from monad import *
from django.db import models

M = TypeVar("M", bound=models.Model)
PK = TypeVar("PK")
GetQueryset = Callable[[type[M]], models.QuerySet[M]]


class RepositoryBase(Generic[M]):
    model: type[M]
    __get_queryset: GetQueryset[M]

    @property
    def get_queryset(self) -> models.QuerySet[M]:
        return self.__get_queryset(self.model)

    def __init__(self, model: type[M], get_queryset: GetQueryset[M] | None = None):
        self.model = model
        if not get_queryset:
            get_queryset = lambda x: x.objects.all()
        self.__get_queryset = get_queryset


class SingleItemRepository(RepositoryBase[M], Generic[M, PK]):
    @Maybe.wraps
    def find_by_id(self, pk: PK):
        return self.get_queryset.filter(pk=pk).first()

    @Maybe.wraps
    def find_by(self, **kwargs):
        return self.get_queryset.filter(**kwargs).first()


class MultiItemRepository(RepositoryBase[M]):
    def filter(self, **kwargs):
        return self.get_queryset.filter(**kwargs)

    def exists(self, **kwargs):
        return self.get_queryset.filter(**kwargs).exists()


class Repository(SingleItemRepository[M, PK], MultiItemRepository[M]):
    pass
