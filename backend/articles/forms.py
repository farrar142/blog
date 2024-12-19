from ninja import Schema


class ArticleForm(Schema):
    title: str
    content: str
