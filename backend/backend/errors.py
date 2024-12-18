from typing import Self
from ninja import NinjaAPI


class Error[T](Exception):
    def __init__(self, message: T, status: int):
        self.message, self.status = message, status

    status: int
    message: T

    @classmethod
    def register(cls, ninja: NinjaAPI):
        @ninja.exception_handler(cls)
        def error_handler(request, exc: Self):
            return ninja.create_response(
                request, dict(message=exc.message), status=exc.status
            )
