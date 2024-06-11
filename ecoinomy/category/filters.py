from django_filters import rest_framework as filters
from .models import Category


class CategoryFilter(filters.FilterSet):

    class Meta:
        model = Category
        fields = ["parent_category", "name", "is_active"]