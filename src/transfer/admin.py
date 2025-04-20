from django.contrib import admin

from .models import TransferModel


@admin.register(TransferModel)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("from_card", "to_card", "amount", "user", "created_at", "updated_at")
    search_fields = ("from_card", "to_card", "user")
    list_filter = ("user", "amount")
    list_display_links = ("from_card", "to_card")
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by amount & user"
