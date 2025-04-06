from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(_("Created DateTime"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated DateTime"), auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = "updated_at"


class Language(models.TextChoices):
    ENGLISH = "en", _("English")
    RUSSIAN = "ru", _("Russian")
    KYRGYZ = "ky", _("Kyrgyz")
