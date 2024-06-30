from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Group
from .serializers import Permission


class GroupFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Group
        fields = ["name", "created"]
    

class PermissionFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter(label='Created Date Range')
    name = filters.CharFilter(lookup_expr='icontains')
    codename = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Permission
        fields = ["name", "codename", "created"]
