from monad import Maybe
from commons.repository import Repository
from .models import User


class UserRepository(Repository[User, int]):
    def is_username_exists(self, username: str):
        return self.exists(username=username)

    def find_by_username(self, username: str):
        return self.find_by(username=username)
