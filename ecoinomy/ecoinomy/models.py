from django.db import models
from django.utils.translation import gettext_lazy as _


class DeletedManager(models.Manager):
    pass


class CustomManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        s = super(CustomManager, self).bulk_create(objs, **kwargs)
        for i in objs:
            # sending post_save signal for individual object
            models.signals.post_save.send(i.__class__, instance=i, created=True)

        return s


class BaseModel(models.Model):
    class Meta:
        abstract = True

    all_objects = DeletedManager()
    # objects = models.Manager()
    objects = CustomManager()
    created_at = models.DateTimeField(
        editable=False, auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        editable=False, auto_now=True, verbose_name=_("Updated At")
    )

    def update(self, to_update):
        """
        updates self with the to_update dict
        """
        for attr, value in to_update.items():
            setattr(self, attr, value)
