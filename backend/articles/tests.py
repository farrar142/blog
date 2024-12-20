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
        self.pp(resp.json())
        self.assertEqual(resp.status_code, 403)

        self.client.login(self.user)
        resp = self.client.patch(f"/articles/{id}", dict(title="hello"))
        print(resp.json())
        self.assertEqual(resp.status_code, 200)
