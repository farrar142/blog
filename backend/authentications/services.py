from backend.errors import Error
from users.repositories import UserRepository, User
from .forms import *


class AuthService:
    user_repository = UserRepository(User)

    def signup(self, schema: SignUpForm):
        if self.user_repository.is_username_exists(schema.username):
            raise Error("username already exists", 400)
        if schema.password != schema.check_password:
            raise Error("password not matched", 400)
        user = User.builder().from_dict(schema.dict()).build()
        user.set_password(schema.password)
        user.save()
        return user

    def signin(self, username: str, password: str):
        user = self.user_repository.find_by_username(username)
        user = user.or_else_throw(Error("user not exists", 400))
        if not user.check_password(password):
            raise Error("password not matched", 401)
        return user
