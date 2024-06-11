from django.contrib import admin
from .models import *


class StoreMediaItemInline(admin.StackedInline):
    model = ArticleViews


@admin.register(Article)
class StoreAdmin(admin.ModelAdmin):
    inlines = [StoreMediaItemInline]
    list_display = ["id", "heading", "sub_category", "estimated_time_to_read", "article_type"]
    list_display_links = ["heading"]


@admin.register(Snippet)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["id", "heading", "code", "description", "status"]
    list_display_links = ["heading"]