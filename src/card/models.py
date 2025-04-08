from django.db import models

from config.models import TimestampedModel
from users.models import User


class CardModel(TimestampedModel):
    title = models.CharField("Title", max_length=255, null=False, blank=False)
    balance = models.DecimalField("Balance", max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="card", verbose_name="User")

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} - {}".format(self.title, self.user.username)
