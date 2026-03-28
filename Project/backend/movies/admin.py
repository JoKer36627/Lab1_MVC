from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "director", "rating", "updated_at")
    search_fields = ("title", "director")
    list_filter = ("rating",)
