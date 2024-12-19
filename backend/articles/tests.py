from authentications.services import AuthService, SignUpForm
from commons.test import TestCase
from users.services import UserService


form = SignUpForm(
    email="test@test.com",
    username="testuser",
    password="1234",
    check_password="1234",
)


class TestArticle(TestCase):
    authService = AuthService()
    userService = UserService()

    def setUp(self):
        self.user = self.authService.signup(form)

    def test_post_article(self):
        self.client.login(self.user)
        resp = self.client.post("/articles/", dict(title="test", content="test"))
        self.assertEqual(resp.status_code, 200)

    def test_post_wrong_article(self):
        self.client.login(self.user)
        resp = self.client.post("/articles/", dict(title="", content=""))
        self.pp(resp.json)
        self.assertEqual(resp.status_code, 200)
