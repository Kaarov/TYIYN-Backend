from django.contrib import admin

from .models import CardModel


@admin.register(CardModel)
class CardAdmin(admin.ModelAdmin):
    list_display = ("title", "balance", "user", "created_at", "updated_at")
    search_fields = ("title", "user")
    list_filter = ("user",)
    list_display_links = ("title",)
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by title, user"
