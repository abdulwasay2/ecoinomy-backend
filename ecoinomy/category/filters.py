from django_filters import rest_framework as filters
from .models import Category


class CategoryFilter(filters.FilterSet):
    is_parent = filters.CharFilter(method='is_parent')

    class Meta:
        model = Category
        fields = ["parent_category", "name", "is_active", "is_parent"]

    @staticmethod
    def is_parent(queryset, name, value):
        return queryset.filter(parent_category__isnull=value)