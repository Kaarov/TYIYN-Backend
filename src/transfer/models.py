from django.db import models

from card.models import CardModel
from config.models import TimestampedModel
from users.models import User


class TransferModel(TimestampedModel):
    from_card = models.ForeignKey(
        CardModel,
        on_delete=models.CASCADE,
        related_name="transfer_from",
        verbose_name="Card",
    )
    to_card = models.ForeignKey(CardModel, on_delete=models.CASCADE, related_name="transfer_to", verbose_name="Card")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transfer", verbose_name="User")

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transfers"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} - {} - {}".format(self.from_card, self.to_card, self.user.username)
