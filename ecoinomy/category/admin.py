from django.contrib import admin
from .models import Category, CarousalItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_active"]
    list_display_links = ["name"]


@admin.register(CarousalItem)
class CarousalItemAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "is_active"]
