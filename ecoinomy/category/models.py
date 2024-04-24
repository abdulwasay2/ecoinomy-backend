from django.db import models
from ecoinomy.models import BaseModel



# Create your models here.
class Cateogry(BaseModel):
    class Meta:
        db_table = "category"

    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    icon = models.FileField(upload_to="icon/", blank=True, null=True)
    created_datetime = models.DateTimeField(auto_created=True, auto_now_add=True)