from django.db import models

from card.models import CardModel
from category.models import CategoryModel
from config.models import TimestampedModel
from users.models import User


class BudgetModel(TimestampedModel):
    title = models.CharField("Title", max_length=255, blank=False, null=False)
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE, related_name="budget", verbose_name="Card")
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, related_name="budget", verbose_name="Category"
    )
    period = models.DateField("Period", blank=False, null=False)
    limit = models.IntegerField("Limit")
    spent = models.IntegerField("Spent")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budget", verbose_name="User")

    class Meta:
        verbose_name = "Budget"
        verbose_name_plural = "Budgets"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} - {}".format(self.category, self.title)
