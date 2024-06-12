from django.db import models
from django_countries.fields import CountryField
from ecoinomy.models import BaseModel


class ArticleType(models.Choices):
    OPINION = 'Opinion'
    ANALYSIS = 'Analysis'


class ArticleAuthor(BaseModel):
    name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255, blank=True, null=True)
    work_place = models.CharField(max_length=255, blank=True, null=True)


class Article(BaseModel):
    media = models.FileField(upload_to="article_image/", blank=True, null=True)
    heading = models.CharField(max_length=255)
    body = models.TextField()
    body_in_second_language = models.TextField(blank=True)
    sub_category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name="articles")
    article_by = models.ForeignKey(ArticleAuthor, on_delete=models.SET_NULL, blank=True,
                                   null=True, related_name="authored_articles")
    views = models.ManyToManyField('user.User', null=True, through="ArticleViews", related_name="articles_viewed")
    estimated_time_to_read = models.DurationField(null=True)
    article_type = models.CharField(max_length=256, choices=ArticleType.choices)
    country = CountryField(max_length=255, null=True, blank=True, default="CA")


class ArticleViews(BaseModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name="articles")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="articles")


class Snippet(BaseModel):
    heading = models.CharField(max_length=255)
    body = models.TextField()
    sub_category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name="snippets")
    country = CountryField(max_length=255, null=True, blank=True, default="CA")
