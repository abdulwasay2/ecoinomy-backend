from django.db import models
from django.contrib.auth.models import Group 
from django.utils.translation import gettext_lazy as _

 
#TODO: Make a new groups model and attach that to the user 
Group.add_to_class(
    'description', models.TextField(blank=True, null=True)
    )
Group.add_to_class(
    'created_at', models.DateTimeField(
            editable=False, auto_now_add=True, verbose_name=_("Created At")
        )
    )
Group.add_to_class(
    'updated_at', models.DateTimeField(
            editable=False, auto_now=True, verbose_name=_("Updated At")
        )
    )