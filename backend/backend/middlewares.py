import ast
from functools import partial, reduce
import json
from typing import Callable
from django.http import QueryDict
from django.http.request import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from monad import Result
from monad.monads.delay import Delay

is_target_method: Callable[[HttpRequest], bool] = lambda request: request.method in [
    "POST",
    "PUT",
    "PATCH",
]
is_json: Callable[[HttpRequest], bool] = (
    lambda request: request.content_type == "application/json"
)
is_files: Callable[[HttpRequest], bool] = (
    lambda request: len(list(request.FILES.items())) != 0
)


def reducer(x: QueryDict, y: tuple[str, str]):
    x[y[0]] = y[1]
    return x


def json_to_querydict(j: str):
    d: dict = json.loads(j)
    return reduce(reducer, list(d.items()), QueryDict(mutable=True))


json_formatter = Delay(bytes.decode).map(ast.literal_eval).map(json.dumps)
json_parser = json_formatter.map(json.loads)


class ApplicationJsonConvertMiddleware(MiddlewareMixin):
    @Result.wraps
    def parse_json(self, request: HttpRequest):
        jsoned = json_formatter.run(request.body)
        data = json_to_querydict(jsoned)
        body = jsoned.encode("utf-8")
        request.META["CONTENT_TYPE"] = "multipart/form-data"
        setattr(request, "POST", data)
        setattr(request, "_body", body)
        setattr(request, "_stream", body)
        setattr(request, "_read_started", False)

    @Result.wraps
    def fill_post(self, request: HttpRequest):
        if request.method == "POST":
            return
        if hasattr(request, "_post"):  # post 데이터 삭제
            del request._post  # type:ignore
            del request._files  # type:ignore
        initial_method = request.method
        request.method = "POST"
        request.META["REQUEST_METHOD"] = "POST"
        request._load_post_and_files()
        request.META["REQUEST_METHOD"] = initial_method
        request.method = initial_method

    def process_request(self, request: HttpRequest):
        if not is_target_method(request):
            return
        if is_json(request):
            self.parse_json(request)
        else:
            self.fill_post(request)

    def process_response(self, request, response):
        return response
