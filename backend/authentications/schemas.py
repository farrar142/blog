from ninja import Schema


class UserInfo(Schema):
    id: int
    email: str
    username: str


class TokenResponse(Schema):
    refresh: str
    access: str
