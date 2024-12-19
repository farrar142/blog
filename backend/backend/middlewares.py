from functools import reduce
import json
from typing import Callable
from django.http import QueryDict
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from monad import Result

is_target_method: Callable[[HttpRequest], bool] = lambda request: request.method in [
    "POST",
    "PUT",
    "PATCH",
]
is_multipart: Callable[[HttpRequest], bool] = (
    lambda request: request.content_type == "multipart/form-data"
)
is_files: Callable[[HttpRequest], bool] = (
    lambda request: len(list(request.FILES.items())) != 0
)


def reducer(x: dict[str, str], y: tuple[str, str]):
    x[y[0]] = y[1]
    return x


class ApplicationJsonConvertMiddleware(MiddlewareMixin):
    @Result.wraps
    def parse(self, request: HttpRequest):
        if not (is_multipart(request) and is_target_method(request)):
            return
        if is_files(request):
            return
        data = reduce(reducer, request.POST.items(), dict())
        body = json.dumps(data).encode("utf-8")
        setattr(request, "_body", body)
        setattr(request, "_stream", json.dumps(data).encode("utf-8"))
        request.META["CONTENT_TYPE"] = "application/json"
        setattr(request, "_read_started", False)

    def process_request(self, request: HttpRequest):
        result = self.parse(request)

    def process_response(self, request, response):
        return response
