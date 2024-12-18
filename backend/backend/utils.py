from time import perf_counter
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


def perf(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} tooks {perf_counter()-start:3f} sec")
        return result

    return wrapper
