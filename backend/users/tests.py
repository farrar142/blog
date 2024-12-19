from commons.test import TestCase


class TestNinja(TestCase):

    def test_signup_password_error(self):
        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1235",
            ),
        )
        self.assertEqual(resp.json()["message"], "password not matched")
        self.assertEqual(resp.status_code, 400)

    def test_signup_user_exists_error(self):
        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
        )
        self.assertEqual(resp.json()["message"], "username already exists")
        self.assertEqual(resp.status_code, 400)

    def test_signin(self):

        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
            # content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            "/auth/signin", dict(username="testuser", password="1234")
        )
        self.assertEqual(resp.status_code, 200)

    def test_refresh(self):
        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
            # content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        refresh = resp.json()["refresh"]
        resp = self.client.post("/auth/refresh", dict(refresh=refresh))
        self.assertEqual(resp.status_code, 200)

    def test_auth_bearer(self):

        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
            # content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.client._login(f"bearer {resp.json()['access']}")
        resp = self.client.get("/auth/me")
        self.assertEqual(resp.status_code, 200)
        print(resp.json())

    def test_json_content(self):
        resp = self.client.post(
            "/auth/signup",
            dict(
                email="test@test.com",
                username="testuser",
                password="1234",
                check_password="1234",
            ),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
