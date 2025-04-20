from django.contrib import admin

from .models import GoalModel


@admin.register(GoalModel)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "goal", "current", "period", "created_at", "updated_at")
    search_fields = ("title", "user")
    list_filter = ("user", "goal")
    list_display_links = ("title",)
    list_per_page = 30
    ordering = ("-id",)
    search_help_text = "Search by title & user"
