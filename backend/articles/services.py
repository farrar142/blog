# from ninja import PatchDict
from commons.ninjas import PatchDict
from commons.repository import Repository
from commons.services import Service
from users.models import User

from .models import Article
from .forms import ArticleForm


class ArticleService(Service[Article]):
    repository = Repository[Article, int](Article)

    def create(self, form: ArticleForm, user: User):
        builder = self.model.builder().from_dict(form.dict())
        model = builder.build()
        model.owner = user
        model.save()
        return model

    def modify(self, article: Article, form: PatchDict[ArticleForm]):
        for key, value in form.items():
            setattr(article, key, value)
        article.save()
        return article

    def find_by_id(self, pk: int):
        return self.repository.find_by_id(pk)
