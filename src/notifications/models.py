from django.db import models

from config.models import TimestampedModel
from users.models import User


class NotificationModel(TimestampedModel):
    title = models.CharField("Title", max_length=255, blank=False, null=False)
    description = models.TextField("Description", null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="User",
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ("-id",)

    def __str__(self):
        return "{} - {} - {}".format(self.user, self.created_at, self.title)
