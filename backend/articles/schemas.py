from users.schemas import UserSchema
from .forms import ArticleForm


class ArticleSchema(ArticleForm):
    id: int
    owner: UserSchema
