from commons.models import BaseModel, get_owner_model, models
from users.models import User


# Create your models here.
class Article(get_owner_model(User, related_name="articles")):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pass
