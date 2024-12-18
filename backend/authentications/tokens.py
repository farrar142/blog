from typing import Generic, TypeVar
import jwt
from django.conf import settings
from django.utils.timezone import localtime, timedelta, datetime

# 비밀키 (서명에 사용)
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

T = TypeVar("T", bound=dict)


class Token(Generic[T]):
    type: str
    lifetime: timedelta
    currenttime: datetime
    _claims: T

    @property
    def claims(self):
        payload = dict()
        payload.update(self._claims)
        payload.update(iat=self.currenttime)
        payload.update(exp=self.currenttime + self.lifetime)
        return payload

    def __init__(self, claims: T):
        self._claims = claims
        self.currenttime = localtime()

    def encode(self, additional: dict | None = None):
        payload = self.claims
        if additional:
            payload.update(additional)
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @classmethod
    def decode(cls, token: str):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return cls(decoded)


class RefreshToken(Token[dict]):
    type = "refresh_token"
    lifetime = timedelta(days=7)

    @classmethod
    def from_user(cls, user, additional: dict | None = None):
        claims = dict()
        if additional:
            claims.update(additional)
        claims.update(id=user.pk)
        return cls(claims)

    @property
    def access_token(self):
        return AccessToken(self.claims)


class AccessToken(Token[dict]):
    type = "access_token"
    lifetime = timedelta(minutes=15)
