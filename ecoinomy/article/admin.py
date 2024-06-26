from django.contrib import admin
from .models import *


class ArticleViewsInline(admin.StackedInline):
    model = ArticleViews


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleViewsInline]
    list_display = ["id", "heading", "sub_category", "estimated_time_to_read", "article_type"]
    list_display_links = ["heading"]


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    list_display = ["id", "heading", "body", "country"]
    list_display_links = ["heading"]


@admin.register(ArticleAuthor)
class ArticleAuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "profession", "work_place"]
    list_display_links = ["name"]


@admin.register(ArticleViews)
class ArticleViewsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "article", "created_at"]
    list_editable = ["user", "article", "created_at"]
