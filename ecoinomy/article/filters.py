from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Article


class ArticleFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    heading = filters.CharFilter(lookup_expr='icontains')
    sub_category = filters.NumberFilter(method="filter_by_category_id")

    class Meta:
        model = Article
        fields = ["sub_category", "heading", "is_active", "article_type", "article_by", "created"]

    @staticmethod
    def filter_by_category_id(queryset, name, value):
        return queryset.filter(
            Q(sub_category_id=value) |
            Q(sub_category__parent_category_id=value)
            )