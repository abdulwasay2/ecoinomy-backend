from django_filters import rest_framework as filters
from .models import Category, CarousalItem


class CategoryFilter(filters.FilterSet):
    is_parent = filters.BooleanFilter(field_name='parent_category', lookup_expr='isnull')
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ["parent_category", "name", "is_active", "created"]


class CarousalItemFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CarousalItem
        fields = ["description", "is_active", "created", "article_id", "snippet_id"]
