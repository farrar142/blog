from ninja import Schema, Field


class ArticleForm(Schema):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
