from django.db import models

from card.models import CardModel
from config.models import TimestampedModel
from users.models import User


class GoalModel(TimestampedModel):
    title = models.CharField("Title", max_length=255, blank=False, null=False)
    card = models.ForeignKey(CardModel, on_delete=models.CASCADE, related_name="goal", verbose_name="Card")
    period = models.DateField("Period", blank=False, null=False)
    goal = models.IntegerField("Goal")
    current = models.IntegerField("Current Capacity", blank=True, null=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goal", verbose_name="User")

    class Meta:
        verbose_name = "Goal"
        verbose_name_plural = "Goals"
        ordering = ("-created_at",)

    def __str__(self):
        return "{} - {} - {}".format(self.goal, self.title, self.user)
