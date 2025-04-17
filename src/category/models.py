from django.db import models

from config.models import TimestampedModel
from users.models import User


class CategoryModel(TimestampedModel):
    title_en = models.CharField("Title in English", max_length=255, blank=False, null=False)
    title_ru = models.CharField("Title in Russian", max_length=255, blank=False, null=False)
    title_ky = models.CharField("Title in Kyrgyz", max_length=255, blank=False, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category", verbose_name="User")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)

    def get_name(self, lang_code: str) -> str:
        return getattr(self, f"title_{lang_code}", self.title_en)

    def __str__(self):
        return "{} - {}".format(self.get_name(self.user.language), self.user.username)
