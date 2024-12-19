from commons.services import Service
from users.models import User

from .models import Article
from .forms import ArticleForm


class ArticleService(Service[Article]):
    def create(self, form: ArticleForm, user: User):
        builder = self.model.builder().from_dict(form.dict())
        model = builder.build()
        model.owner = user
        model.save()
        return model
