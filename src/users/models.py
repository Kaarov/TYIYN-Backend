from django.contrib.auth.models import AbstractUser
from django.db import models

from config.models import Language


class User(AbstractUser):
    """User model."""

    username = models.CharField("Username", max_length=100, unique=True)
    email = models.EmailField("Email address", blank=True, null=True)
    avatar = models.ImageField("Profile picture", upload_to="profile-picture/", blank=True, null=True)
    bio = models.TextField("Bio", blank=True, null=True)
    language = models.CharField("Language", max_length=10, choices=Language.choices, default=Language.ENGLISH)

    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return "{username}".format(username=self.get_username())
