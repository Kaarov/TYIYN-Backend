from django.contrib import admin

from .models import NotificationModel


@admin.register(NotificationModel)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "description", "created_at", "updated_at")
    search_fields = ("user", "title")
    list_filter = ("user", "title", "created_at", "updated_at")
    list_display_links = ("title",)
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by user & title"
