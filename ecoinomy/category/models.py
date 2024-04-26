from django.db import models
from ecoinomy.models import BaseModel


class Category(BaseModel):
    parent_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True, related_name="sub_categories"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.FileField(upload_to="category/icon/", blank=True, null=True)
    is_active = models.BooleanField(default=True)


class CarousalItem(BaseModel):
    description = models.TextField(blank=True)
    media = models.FileField(upload_to="category/icon/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
