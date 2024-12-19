from ninja import Router, Schema

from articles.models import Article
from articles.services import ArticleService
from authentications.bearers import JwtBearer
from backend.requests import AuthenticatedRequest
from users.models import User
from users.schemas import UserSchema

from .forms import ArticleForm
from .schemas import ArticleSchema

router = Router(tags=["articles"])


@router.post("/", response=ArticleSchema, auth=JwtBearer())
def post(request: AuthenticatedRequest[User], form: ArticleForm):
    service = ArticleService(Article)
    article = service.create(form, request.auth)
    article.owner
    return article
