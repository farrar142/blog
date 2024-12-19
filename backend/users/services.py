from backend.errors import Error
from authentications.forms import *
from .repositories import UserRepository
from .models import User


class UserService:
    user_repository = UserRepository(User)

    def find_by_id(self, id: int):
        return self.user_repository.find_by_id(id)
