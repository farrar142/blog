import functools
from typing import Any, Callable, Generator, Generic, Iterable, TypeVar
from authentications.services import AuthService, SignUpForm
from commons.test import TestCase
from users.services import UserService


form = SignUpForm(
    email="test@test.com",
    username="testuser",
    password="1234",
    check_password="1234",
)

form2 = SignUpForm(
    email="test2@test.com",
    username="test2user",
    password="1234",
    check_password="1234",
)


class TestArticle(TestCase):
    authService = AuthService()
    userService = UserService()

    def setUp(self):
        self.user = self.authService.signup(form)
        self.user2 = self.authService.signup(form2)

    def test_post_article(self):
        self.client.login(self.user)
        resp = self.client.post("/articles/", dict(title="test", content="test"))
        self.assertEqual(resp.status_code, 201)

    def test_post_wrong_article(self):
        self.client.login(self.user)
        resp = self.client.post("/articles/", dict(title="", content=""))
        self.assertEqual(resp.status_code, 422)

    def test_patch_article(self):
        self.client.login(self.user)
        # resp = self.client.patch("/articles/1", dict())
        # self.pp(resp.json())
        # self.assertEqual(resp.status_code, 404)

        resp = self.client.post("/articles/", dict(title="test", content="test"))
        self.assertEqual(resp.status_code, 201)

        id = resp.json()["id"]

        self.client.login(self.user2)
        resp = self.client.patch(f"/articles/{id}", dict(title="hello", content="bye"))
        self.assertEqual(resp.status_code, 403)

        self.client.login(self.user)
        resp = self.client.patch(f"/articles/{id}", dict(title="hello"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["title"], "hello")


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class Stream[T]:
    @staticmethod
    def __generator(elements: Iterable[T]) -> Generator[T, Any, None]:
        for element in elements:
            yield element

    def __map(self, func: Callable[[T], U]) -> Generator[U, Any, None]:
        for element in self.value:
            yield func(element)

    def __filter(self, func: Callable[[T], bool]) -> Generator[T, Any, None]:
        for element in self.value:
            if func(element):
                yield element

    def __init__(self, value: Generator[T, Any, None]):
        self.value = value

    @classmethod
    def from_iter(cls, args: Iterable[T]):
        return cls(cls.__generator(args))

    def to_list(self):
        return list(self.value)

    def map(self, func: Callable[[T], U]):
        return Stream(self.__map(func))

    def filter(self, func: Callable[[T], bool]):
        return Stream(self.__filter(func))

    def reduce(self, func: Callable[[U, T], U], initial: U):
        return functools.reduce(func, self.value, initial)
