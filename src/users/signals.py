import json
import os

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from category.models import CategoryModel
from users.models import User


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        file_path = os.path.join(settings.BASE_DIR, "category", "migrations", "categories.json")
        with open(file_path, "r", encoding="utf-8") as file:
            categories = json.load(file)
            for category in categories:
                CategoryModel.objects.get_or_create(user=instance, **category)
