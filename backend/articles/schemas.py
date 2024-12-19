from users.schemas import UserSchema
from .forms import ArticleForm


class ArticleSchema(ArticleForm):
    owner: UserSchema
