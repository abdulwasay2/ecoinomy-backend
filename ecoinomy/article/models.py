from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from ecoinomy.models import BaseModel
from django.db.models import Q, CheckConstraint
from category.models import Category



class ArticleType(models.Choices):
    OPINION = 'opinion'
    ANALYSIS = 'analysis'
    ETC = 'etc'


# Create your models here.
class Article(BaseModel):
    class Meta:
        db_table = "article"

    image = models.FileField(upload_to="article_image/", blank=True, null=True)
    heading = models.CharField(max_length=128)
    body = models.CharField(max_length=128)
    body_in_second_language = models.CharField(max_length=128, null=True, blank=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    views = models.IntegerField(default=0)
    sub_category = models.ForeignKey('Category', on_delete=models.CASCADE)
    article_by = models.CharField(max_length=128, blank=True, null=True)
    views = models.IntegerField(default=0)
    estimated_time_taken_to_read_article = models.IntegerField(default=0)
    article_type = models.CharField(max_length=256, choices=ArticleType.choices)
    country_code = CountryField(max_length=255, null=True, blank=True, default="Australia")
