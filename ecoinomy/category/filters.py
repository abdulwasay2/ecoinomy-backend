from django.db.models import Prefetch
from django_filters import rest_framework as filters
from .models import Category, CarousalItem


class CategoryFilter(filters.FilterSet):
    is_parent = filters.BooleanFilter(field_name='parent_category', lookup_expr='isnull')
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    name = filters.CharFilter(lookup_expr='icontains')
    is_active = filters.BooleanFilter(method="filter_by_is_active")

    class Meta:
        model = Category
        fields = ["parent_category", "name", "is_active", "created"]

    
    @staticmethod
    def filter_by_is_active(queryset, name, value):
        return queryset.filter(is_active=value).prefetch_related(
            Prefetch(
                "sub_categories",
                queryset=Category.objects.filter(is_active=value)
            )
        )


class CarousalItemFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CarousalItem
        fields = ["description", "is_active", "created", "article_id", "snippet_id"]
