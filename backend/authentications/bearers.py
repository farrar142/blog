from django.contrib.auth import get_user_model
from ninja.security import HttpBearer
from ninja import errors
from .tokens import AccessToken


class JwtBearer(HttpBearer):
    def authenticate(self, request, token):
        if not token:
            return None
        token = AccessToken.decode(token)
        User = get_user_model()
        user = User.objects.filter(id=token.claims["id"]).first()
        if not user:
            raise errors.AuthenticationError
        return user
