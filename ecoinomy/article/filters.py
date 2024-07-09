from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Article, Snippet


class ArticleFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    heading = filters.CharFilter(lookup_expr='icontains')
    sub_category = filters.NumberFilter(method="filter_by_category_id")
    # is_active = filters.BooleanFilter(method="filter_by_is_active")

    class Meta:
        model = Article
        fields = ["sub_category", "heading", "article_type", "article_by", "created", "is_active"]

    @staticmethod
    def filter_by_category_id(queryset, name, value):
        return queryset.filter(
            Q(sub_category_id=value) |
            Q(sub_category__parent_category_id=value)
            )
    
    # @staticmethod
    # def filter_by_is_active(queryset, name, value):
    #     return queryset.filter(
    #         Q(is_active=value) |
    #         Q(sub_category__parent_category_id=value)
    #         )
    

class SnippetFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    heading = filters.CharFilter(lookup_expr='icontains')
    sub_category = filters.NumberFilter(method="filter_by_category_id")

    class Meta:
        model = Snippet
        fields = ["sub_category", "heading", "created", "is_active"]

    @staticmethod
    def filter_by_category_id(queryset, name, value):
        return queryset.filter(
            Q(sub_category_id=value) |
            Q(sub_category__parent_category_id=value)
            )