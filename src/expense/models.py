from django.db import models

from card.models import CardModel
from category.models import CategoryModel
from config.models import TimestampedModel
from users.models import User


class ExpenseModel(TimestampedModel):
    card = models.ForeignKey(
        CardModel,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="Card",
    )
    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
        verbose_name="Category",
    )
    amount = models.DecimalField("Amount", max_digits=10, decimal_places=2)
    description = models.TextField("Description", null=True, blank=True)
    date = models.DateField("Date", null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses",
        verbose_name="User",
    )

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} - {} - {}".format(self.category, self.card, self.user)
