from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from config.settings import ADMIN_PASSWORD


class Command(BaseCommand):
    help = "Creates a superuser admin automatically"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", ADMIN_PASSWORD)
            self.stdout.write(self.style.SUCCESS("admin superuser created"))
        else:
            self.stdout.write("The superuser already exists.")
