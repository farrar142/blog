from typing import Any, Generic, TypeVar
from django.db import models

M = TypeVar("M", bound=models.Model)


class Builder(Generic[M]):

    def __init__(self, model: type[M]):
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


class WithBuild(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def builder(cls):
        return Builder(cls)
