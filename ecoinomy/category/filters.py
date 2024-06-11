from django_filters import rest_framework as filters
from .models import Category


class CategoryFilter(filters.FilterSet):
    is_parent = filters.BooleanFilter(field_name='parent_category', lookup_expr='isnull')

    class Meta:
        model = Category
        fields = ["parent_category", "name", "is_active"]
