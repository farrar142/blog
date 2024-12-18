from monad import Maybe
from .models import User


class UserRepository:
    def is_username_exists(self, username: str):
        return User.objects.filter(username=username).exists()

    @Maybe.wraps
    def find_by_username(self, username: str):
        return User.objects.filter(username=username).first()

    @Maybe.wraps
    def find_by_id(self, id: int):
        return User.objects.filter(id=id).first()
