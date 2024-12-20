from typing import Optional, Protocol
from django.http import Http404
from ninja import Form, PatchDict, Router, Schema, errors

from articles.models import Article
from articles.services import ArticleService
from authentications.bearers import JwtBearer
from backend.errors import PermissionDenied
from backend.requests import AuthenticatedRequest
from commons.permissions import is_resource_owner
from users.models import User, models
from users.schemas import UserSchema

from .forms import ArticleForm
from .schemas import ArticleSchema

router = Router(tags=["articles"])
service = ArticleService(Article)


@router.post("/", response={201: ArticleSchema}, auth=JwtBearer())
def post(request: AuthenticatedRequest[User], form: Form[ArticleForm]):
    article = service.create(form, request.auth)
    article.owner
    return 201, article


@router.patch("/{pk}", response=ArticleSchema, auth=JwtBearer())
def patch(request: AuthenticatedRequest[User], pk: int, form: ArticleForm):
    print("ehy?")
    article = service.find_by_id(pk).or_else_throw(Http404)
    if not is_resource_owner(request.auth)(article):
        raise PermissionDenied("permission denied")
    print(form)
    print("???")
    # try:
    #     service.modify(article, form)
    # except Exception as e:
    #     print(e)

    return article
