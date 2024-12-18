from ninja import Schema, Field


class SignUpForm(Schema):
    email: str
    username: str
    password: str
    check_password: str


class RefreshForm(Schema):
    refresh: str = Field(..., min_length=1)
