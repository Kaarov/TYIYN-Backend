from django.contrib import admin

from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title_en", "user", "created_at", "updated_at")
    search_fields = ("user",)
    list_filter = ("user",)
    list_display_links = ("title_en",)
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by user"
