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
    def parse(self, request: HttpRequest):
        if not (is_target_method(request)):
            return
        if not (is_json(request)):
            return
        jsoned = json_formatter.run(request.body)
        data = json_to_querydict(jsoned)
        body = jsoned.encode("utf-8")
        request.META["CONTENT_TYPE"] = "multipart/form-data"
        setattr(request, "POST", data)
        setattr(request, "_body", body)
        setattr(request, "_stream", body)
        setattr(request, "_read_started", False)

    def process_request(self, request: HttpRequest):
        self.parse(request)

    def process_response(self, request, response):
        return response


class PutPatchWithFileFormMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if (
            request.method in ("PUT", "PATCH")
            and request.content_type != "application/json"
        ):
            if hasattr(request, "_post"):  # post 데이터 삭제
                del request._post
                del request._files
            try:
                initial_method = request.method
                request.method = "POST"  # 리퀘스트 메서드를 POST로 임시 변경
                request.META["REQUEST_METHOD"] = "POST"
                request._load_post_and_files()  # 이 부분이 핵심
                request.META["REQUEST_METHOD"] = initial_method  # 원래 메서드로 되돌림
                request.method = initial_method  # 원래 메서드로 되돌림
            except Exception:
                pass
