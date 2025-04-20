from django.contrib import admin

from .models import ExpenseModel


@admin.register(ExpenseModel)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("card", "user", "category", "amount", "description", "date", "created_at", "updated_at")
    search_fields = ("card", "user")
    list_filter = ("user", "category", "amount")
    list_display_links = ("card",)
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by card & user"
