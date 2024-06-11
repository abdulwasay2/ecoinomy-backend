from django_filters import rest_framework as filters
from .models import Article


class CategoryFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    heading = filters.CharField(lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ["sub_category", "heading", "is_active", "article_type", "article_by", "created"]
